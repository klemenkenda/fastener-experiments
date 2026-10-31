"""H12: do LLMs know the H8 datasets, and the relevance of their features?

Six probes per model and dataset, none of which shows the data
(HYPOTHESES.md, H12; the design of H12-E01 in EXPERIMENTS.md):

  P1a  identify   from an anonymous card: rows, features, class names
  P1b  identify   from the feature names alone
  P2   schema     given the dataset's name, list its features in order
  P3   position   given the dataset's name, score features 0..p-1 by
                  position in the original column order -- no names
  P3f  position   the same with a fictitious dataset name (the control)
  P4   named      the dataset's name, the class names and the feature names
  P5   named      the class names and the feature names, no dataset name

and the relevance the probes are judged against, from the data alone
(`truth`): LightGBM's permutation importance on the validation split
(primary; the drop in weighted F1, mean of five permutations), and mutual
information of each variable with the class on the training split
(secondary; mean over seeds 2020-2024). Variables are the dataset's original
columns: adult's and diabetes130's one-hot columns are grouped back into the
variable they came from ('workclass=Private' -> 'workclass').

    python experiments/h12_probes.py truth                  # -> h12/truth/
    python experiments/h12_probes.py probe --experiment H12-E01 --workers 8
    python experiments/h12_probes.py score                  # -> reports/H12-E01/

Every call goes through `llm_guidance.CallLog` (h12/calls.jsonl, committed),
so `score` and any rerun of `probe` replay it without the network.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

import _bootstrap  # noqa: F401  (puts the FASTENER clone on the path)
import llm_guidance as lg
from guidance import GuidanceContext

HERE = Path(__file__).resolve().parent
H12_DIR = HERE / "h12"
TRUTH_DIR = H12_DIR / "truth"
PROBE_DIR = H12_DIR / "probes"
CALL_LOG = H12_DIR / "calls.jsonl"
REPORT_DIR = HERE / "reports" / "H12-E01"

SEED = 20200
TRUTH_SEEDS = (2020, 2021, 2022, 2023, 2024)
MAX_COST = 10.0         # US$, this experiment's calls (DEC-53)
PROBES = ("P1a", "P1b", "P2", "P3", "P3f", "P4", "P5")

MODELS = ("anthropic/claude-opus-5.5", "anthropic/claude-sonnet-5.5",
          "anthropic/claude-haiku-5.5", "meta-llama/llama-3.3-70b-instruct",
          "google/gemma-3-4b-it", "google/gemma-3-27b-it",
          "mistralai/ministral-8b-2512", "qwen/qwen3-14b", "microsoft/phi-4",
          "deepseek/deepseek-v4-flash", "openai/gpt-6-luna",
          "google/gemini-2.5-flash-lite")

# Each dataset as it is named to the model (P2, P3, P4), its rows before the
# 50,000-row cap (P1a), the columns of the distributed file our variables
# leave out (P3 only: they shift the positions), and the patterns that count
# as identifying it (P1a, P1b; case-insensitive, matched in name + source).
IDENTITY: Dict[str, Dict[str, Any]] = {
    "adult": {"name": "Adult (UCI 'Census Income', 1994 US census; OpenML 1590)",
              "rows": 48842, "left_out": ["native-country"],
              "aliases": [r"\badult\b", r"census[ -]?income"]},
    "covertype": {"name": "Covertype (UCI 'Covertype', Blackard and Dean; OpenML 1596)",
                  "rows": 581012, "left_out": [],
                  "aliases": [r"cover ?type", r"forest cover"]},
    "crop_mapping": {"name": "UCI 'Crop mapping using fused optical-radar data set' (UCI 525)",
                     "rows": 325834, "left_out": [],
                     "aliases": [r"crop mapping", r"optical[- ]radar", r"winnipeg"]},
    "diabetes130": {"name": "UCI 'Diabetes 130-US hospitals for years 1999-2008' "
                            "(Strack et al. 2014; OpenML 4541)",
                    "rows": 101766,
                    "left_out": ["encounter_id", "patient_nbr", "medical_specialty",
                                 "diag_1", "diag_2", "diag_3"],
                    "aliases": [r"130[- ]us", r"diabetes ?130", r"diabetes.{0,40}readmi"]},
    "eodata": {"name": "'Land Patch Samples' (Sircelj, Kenda and Koprivec, PANGAEA 2020, "
                       "doi:10.1594/PANGAEA.914271), Slovenian Sentinel-2 crop parcels",
               "rows": 480000, "left_out": [],
               "aliases": [r"land patch", r"914271", r"sloven"]},
    "eye_movements": {"name": "Eye movements (PASCAL 'Inferring relevance from eye "
                              "movements' challenge 2005; OpenML 1044, 44130)",
                      "rows": 7608, "left_out": [],
                      "aliases": [r"eye[ _-]?movement", r"inferring relevance"]},
    "gas_drift": {"name": "UCI 'Gas Sensor Array Drift Dataset' (Vergara et al. 2012; "
                          "OpenML 1476)",
                  "rows": 13910, "left_out": [],
                  "aliases": [r"gas[ _-]?(sensor )?(array )?drift"]},
    "har": {"name": "UCI 'Human Activity Recognition Using Smartphones' (Anguita et al. "
                    "2013; OpenML 1478)",
            "rows": 10299, "left_out": [],
            "aliases": [r"human activity recognition", r"\buci[ -]har\b", r"\bhar\b"]},
    "heloc": {"name": "FICO HELOC (FICO Explainable Machine Learning Challenge 2018; "
                      "OpenML 45026)",
              "rows": 10000, "left_out": [],
              "aliases": [r"heloc", r"home equity line", r"fico"]},
    "higgs": {"name": "HIGGS (Baldi, Sadowski and Whiteson 2014; UCI 280; OpenML 23512)",
              "rows": 98049, "left_out": [], "aliases": [r"higgs"]},
    "mice_protein": {"name": "UCI 'Mice Protein Expression' (Higuera et al. 2015; "
                             "OpenML 40966)",
                     "rows": 1080, "left_out": ["MouseID", "Genotype", "Treatment",
                                                "Behavior"],
                     "aliases": [r"mice ?protein"]},
    "ozone_8hr": {"name": "UCI 'Ozone Level Detection', the eight-hour peak set (Zhang and "
                          "Fan 2008; OpenML 1487)",
                  "rows": 2534, "left_out": [], "aliases": [r"ozone"]},
    "pc4": {"name": "NASA MDP PC4 software defect data (PROMISE repository; OpenML 1049)",
            "rows": 1458, "left_out": [], "aliases": [r"\bpc[- ]?4\b"]},
    "phishing": {"name": "UCI 'Phishing Websites' (Mohammad, Thabtah and McCluskey 2012; "
                         "OpenML 4534)",
                 "rows": 11055, "left_out": [], "aliases": [r"phishing"]},
    "qsar_biodeg": {"name": "UCI 'QSAR biodegradation' (Mansouri et al. 2013; OpenML 1494)",
                    "rows": 1055, "left_out": [],
                    "aliases": [r"qsar[ _-]?bio", r"biodeg"]},
    "spambase": {"name": "UCI 'Spambase' (Hopkins et al., Hewlett-Packard Labs 1999; "
                         "OpenML 44)",
                 "rows": 4601, "left_out": [], "aliases": [r"spam ?base"]},
}
DATASETS = tuple(IDENTITY)
# The control's identity: a name no model can know.
FAKE_NAME = "'Brenner field survey 2019' (an internal, unpublished data set)"

SCORE_SYSTEM = (
    "You are helping a feature-selection study of a classification data set. "
    "Rate how useful each feature is likely to be for predicting the class, "
    "on its own or together with a few others, from 0 (useless) to 1 (most "
    "useful). You do not see the data. Reply with a JSON object only: "
    '{"scores": {"<feature index>": <score>, ...}} with one entry for every '
    "feature index listed.")
IDENTIFY_SYSTEM = (
    "You are an expert on public machine-learning benchmark data sets. Name the "
    "published data set described below, if you recognise it. Reply with a JSON "
    'object only: {"name": "<data set name>", "source": "<repository or paper>", '
    '"confidence": <0 to 1>}; use "unknown" as the name if you do not recognise it.')
SCHEMA_SYSTEM = (
    "You are an expert on public machine-learning benchmark data sets. List the "
    "input features (columns other than the class) of the data set named below, "
    "in their original column order, with the names used in its distributed "
    'file. Reply with a JSON object only: {"features": ["<name>", ...]}.')


# ------------------------------------------------------------- variables
def variables(dataset: str):
    """The dataset loaded (cap applied), its variables' names, and for each
    variable the columns it occupies. One-hot 'column=value' columns are one
    variable (adult, diabetes130); every other column is its own."""
    import protocol
    from datasets import load
    data = load(dataset, max_rows=protocol.ROW_CAP)
    dpath = lg.PRIORS_DIR / "dictionaries" / f"{dataset}.json"
    dic = json.loads(dpath.read_text(encoding="utf-8"))
    cols = dic.get("feature_names") or [str(n) for n in data.feature_names]
    names: List[str] = []
    groups: List[List[int]] = []
    for j, c in enumerate(cols):
        base = c.split("=", 1)[0] if "=" in c else c
        if names and names[-1] == base and "=" in c:
            groups[-1].append(j)
        else:
            names.append(base)
            groups.append([j])
    return data, dic, names, groups


def variable_matrix(X: np.ndarray, groups: List[List[int]]) -> Tuple[np.ndarray, np.ndarray]:
    """One column per variable: the column itself, or for a one-hot group the
    code of its set column (0 when none is set). And which are discrete."""
    out = np.empty((X.shape[0], len(groups)))
    discrete = np.zeros(len(groups), dtype=bool)
    for v, g in enumerate(groups):
        if len(g) == 1:
            out[:, v] = X[:, g[0]]
        else:
            block = X[:, g]
            out[:, v] = np.where(block.max(axis=1) > 0, block.argmax(axis=1) + 1, 0)
            discrete[v] = True
    return out, discrete


# ------------------------------------------------------------------ truth
def mutual_information(V: np.ndarray, discrete: np.ndarray, y: np.ndarray,
                       seed: int) -> np.ndarray:
    import fast_mi
    from sklearn.metrics import mutual_info_score
    mi = np.zeros(V.shape[1])
    cont = np.flatnonzero(~discrete)
    if len(cont):
        mi[cont] = fast_mi.mutual_info_classif(V[:, cont], y, random_state=seed)
    for v in np.flatnonzero(discrete):
        mi[v] = mutual_info_score(V[:, v].astype(int), y)
    return mi


def permutation_importance(data, groups: List[List[int]]) -> np.ndarray:
    """Drop in validation weighted F1 when a variable's columns are permuted
    together, LightGBM fitted once on the training split (all columns); the
    mean over the five permutations of TRUTH_SEEDS."""
    import protocol
    protocol.set_model("lgbm", n_jobs=8)
    protocol.set_train_rows(data.X_train.shape[0])
    model = protocol.make_model().fit(data.X_train, data.y_train)
    base = protocol.weighted_f1(data.y_val, model.predict(data.X_val))
    drops = np.zeros((len(TRUTH_SEEDS), len(groups)))
    for r, seed in enumerate(TRUTH_SEEDS):
        rng = np.random.RandomState(seed)
        for v, g in enumerate(groups):
            X = data.X_val.copy()
            X[:, g] = X[rng.permutation(X.shape[0])][:, g]
            drops[r, v] = base - protocol.weighted_f1(data.y_val, model.predict(X))
    return drops.mean(axis=0), float(base)


def make_truth(dataset: str) -> Path:
    from scipy.stats import spearmanr
    data, _, names, groups = variables(dataset)
    V, discrete = variable_matrix(data.X_train, groups)
    mis = np.array([mutual_information(V, discrete, data.y_train, s) for s in TRUTH_SEEDS])
    perm, base = permutation_importance(data, groups)
    seed_rho = [spearmanr(mis[a], mis[b])[0] for a in range(len(mis))
                for b in range(a + 1, len(mis))]
    doc = {"dataset": dataset, "variables": names, "groups": groups,
           "mi": mis.mean(axis=0).tolist(), "mi_by_seed": mis.tolist(),
           "mi_seed_spearman_min": float(np.nanmin(seed_rho)),
           "perm_importance": perm.tolist(), "lgbm_val_weighted_f1": base,
           "n_train": int(data.X_train.shape[0]), "n_val": int(data.X_val.shape[0])}
    TRUTH_DIR.mkdir(parents=True, exist_ok=True)
    out = TRUTH_DIR / f"{dataset}.json"
    out.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    return out


# ----------------------------------------------------------------- probes
class ScoreProbe(lg.LLMFeaturePrior):
    """A score probe (P3, P3f, P4, P5): `header` lines, then the features by
    index, with their names (P4, P5) or as bare positions (P3, P3f). Chunks
    of 300 and one retry for a chunk missing over 20%, as H8's priors."""

    def __init__(self, log, model, header: List[str], show_names: bool) -> None:
        super().__init__(log, model, scrambled=not show_names, seed=SEED)
        self.header, self.show_names = header, show_names

    def messages(self, ctx, indices):
        lines = list(self.header) + ["", f"Features ({len(indices)} of {ctx.n_features}):"]
        lines += [f"{i}: {ctx.feature_names[i]}" if self.show_names else f"{i}"
                  for i in indices]
        return [{"role": "system", "content": SCORE_SYSTEM},
                {"role": "user", "content": "\n".join(lines)}]


def score_headers(dataset: str, names: List[str], class_names: Sequence[str]
                  ) -> Dict[str, Tuple[List[str], bool]]:
    ident = IDENTITY[dataset]
    p = len(names)
    note = ""
    if ident["left_out"]:
        note = (" (the distributed file's columns " + ", ".join(ident["left_out"])
                + " are left out and not counted)")
    pos = ("Its {p} input features are numbered 0 to {last} in the data set's "
           "original column order{note}; the class is not counted. You are not "
           "told their names.")
    classes = "Classes: " + ", ".join(map(str, class_names))
    return {
        "P3": ([f"Data set: {ident['name']}.",
                pos.format(p=p, last=p - 1, note=note)], False),
        "P3f": ([f"Data set: {FAKE_NAME}.", pos.format(p=p, last=p - 1, note="")], False),
        "P4": ([f"Data set: {ident['name']}.", classes], True),
        "P5": ([classes], True),
    }


def text_messages(probe: str, dataset: str, names: List[str],
                  class_names: Sequence[str]) -> List[Dict[str, str]]:
    ident = IDENTITY[dataset]
    if probe == "P1a":
        user = (f"A classification data set with {ident['rows']:,} rows and {len(names)} "
                f"input features. Classes: " + ", ".join(map(str, class_names)) + ".")
        system = IDENTIFY_SYSTEM
    elif probe == "P1b":
        user = (f"A classification data set whose {len(names)} input features are, in "
                "order:\n" + "\n".join(names))
        system = IDENTIFY_SYSTEM
    elif probe == "P2":
        user = f"Data set: {ident['name']}."
        system = SCHEMA_SYSTEM
    else:
        raise ValueError(probe)
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def probe_path(dataset: str, model: str) -> Path:
    slug = re.sub(r"[^A-Za-z0-9.-]+", "-", model)
    return PROBE_DIR / f"{dataset}__{slug}.json"


def run_probes(dataset: str, model: str, log: lg.CallLog, names: List[str],
               class_names: Sequence[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"dataset": dataset, "model": model, "variables": names}
    for probe in ("P1a", "P1b", "P2"):
        body = {"model": model, "messages": text_messages(probe, dataset, names, class_names),
                "temperature": 0.0, "seed": SEED,
                "max_tokens": lg.max_tokens_for(model, 16000)}
        response = log.call(body)
        out[probe] = {"key": lg.request_key(body), "served_model": response.get("model"),
                      "usage": response.get("usage"), "reply": lg.content_of(response)}
    ctx = GuidanceContext(n_features=len(names), feature_names=list(names))
    for probe, (header, show) in score_headers(dataset, names, class_names).items():
        sp = ScoreProbe(log, model, header, show)
        scores = sp(ctx)
        rec = dict(sp.record)
        rec.pop("instructions", None)
        out[probe] = {**rec, "header": header, "system": SCORE_SYSTEM,
                      "scores": [float(x) for x in scores]}
    return out


# ---------------------------------------------------------------- grading
def identified(dataset: str, reply: str) -> bool:
    """Whether an identification reply names the dataset: its "name" and
    "source" (the whole reply, if it is not JSON) match an alias."""
    try:
        obj = lg._loose_json(reply)
        text = f"{obj.get('name', '')} {obj.get('source', '')}" if isinstance(obj, dict) else reply
    except ValueError:
        text = reply
    return any(re.search(a, str(text), re.I) for a in IDENTITY[dataset]["aliases"])


def listed_names(reply: str) -> List[str]:
    try:
        obj = lg._loose_json(reply)
        if isinstance(obj, dict) and isinstance(obj.get("features"), list):
            return [str(x) for x in obj["features"]]
        if isinstance(obj, list):
            return [str(x) for x in obj]
    except ValueError:
        pass
    # Not JSON (e.g. cut off): every quoted string after "features".
    return re.findall(r'"([^"]+)"', reply.split("features", 1)[-1])


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def schema_match(true: Sequence[str], listed: Sequence[str], fuzzy: float = 0.85
                 ) -> Dict[int, int]:
    """One-to-one match of true variable i -> listed position j: exact
    matches (after lower-casing and dropping all but letters and digits)
    first, then, among what is left, pairs with difflib ratio >= `fuzzy`,
    best first. fuzzy=1.0 is exact only."""
    tn, ln = [_norm(t) for t in true], [_norm(x) for x in listed]
    match: Dict[int, int] = {}
    used = set()
    first: Dict[str, List[int]] = {}
    for j, x in enumerate(ln):
        first.setdefault(x, []).append(j)
    for i, t in enumerate(tn):
        for j in first.get(t, []):
            if j not in used:
                match[i] = j
                used.add(j)
                break
    if fuzzy < 1.0:
        cand = []
        for i, t in enumerate(tn):
            if i in match or not t:
                continue
            for j, x in enumerate(ln):
                if j not in used and x:
                    r = difflib.SequenceMatcher(None, t, x).ratio()
                    if r >= fuzzy:
                        cand.append((r, i, j))
        for r, i, j in sorted(cand, reverse=True):
            if i not in match and j not in used:
                match[i] = j
                used.add(j)
    return match


def spearman0(a, b) -> float:
    """Spearman's rho, 0 when either side is constant (a flat score carries
    no ranking: registered for H12)."""
    from scipy.stats import spearmanr
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.ptp(a) == 0 or np.ptp(b) == 0:
        return 0.0
    return float(spearmanr(a, b)[0])


def partial_spearman0(a, truth, control) -> float:
    """Spearman's rho of `a` with `truth` with `control` partialled out (the
    partial correlation of the ranks): what `a` knows of `truth` that
    `control` does not. 0 when `a` is flat; plain rho when `control` is."""
    r_at, r_ac, r_ct = (spearman0(a, truth), spearman0(a, control),
                        spearman0(control, truth))
    if np.ptp(np.asarray(a, float)) == 0:
        return 0.0
    den = (1 - r_ac ** 2) * (1 - r_ct ** 2)
    return 0.0 if den <= 1e-12 else float((r_at - r_ac * r_ct) / np.sqrt(den))


# ------------------------------------------------------------------ score
def model_label(model: str) -> str:
    return model.split("/", 1)[1]


def score(out_dir: Path = REPORT_DIR) -> int:
    from scipy.stats import wilcoxon
    rows = []
    for d in DATASETS:
        truth = json.loads((TRUTH_DIR / f"{d}.json").read_text(encoding="utf-8"))
        mi, pi = np.asarray(truth["mi"]), np.asarray(truth["perm_importance"])
        for m in MODELS:
            path = probe_path(d, m)
            if not path.is_file():
                continue
            doc = json.loads(path.read_text(encoding="utf-8"))
            names = doc["variables"]
            listed = listed_names(doc["P2"]["reply"])
            match = schema_match(names, listed)
            exact = schema_match(names, listed, fuzzy=1.0)
            in_place = sum(1 for i, j in match.items() if i == j)
            s = {p: np.asarray(doc[p]["scores"]) for p in ("P3", "P3f", "P4", "P5")}
            row = {"dataset": d, "model": model_label(m), "n_variables": len(names),
                   "id_card": identified(d, doc["P1a"]["reply"]),
                   "id_names": identified(d, doc["P1b"]["reply"]),
                   "schema_listed": len(listed),
                   "schema_recall": len(match) / len(names),
                   "schema_recall_exact": len(exact) / len(names),
                   "schema_in_place": in_place / len(names)}
            for p in s:
                row[f"rho_{p}_mi"] = spearman0(s[p], mi)
                row[f"rho_{p}_perm"] = spearman0(s[p], pi)
                row[f"{p}_flat"] = bool(np.ptp(s[p]) == 0)
            row["rho_P3_P4"] = spearman0(s["P3"], s["P4"])
            # The criterion reads permutation importance (primary truth);
            # the _mi columns are the same with mutual information.
            row["B_effect"] = row["rho_P3_perm"] - row["rho_P3f_perm"]
            row["C_effect"] = partial_spearman0(s["P4"], pi, s["P5"])
            row["B_effect_mi"] = row["rho_P3_mi"] - row["rho_P3f_mi"]
            row["C_effect_mi"] = partial_spearman0(s["P4"], mi, s["P5"])
            row["P4_minus_P5_perm"] = row["rho_P4_perm"] - row["rho_P5_perm"]
            rows.append(row)
    if not rows:
        print("no probes to score")
        return 1
    tables = out_dir / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    _write_csv(tables / "probes.csv", rows)

    def test(vals):
        vals = np.asarray(vals, float)
        pos, neg = int((vals > 0).sum()), int((vals < 0).sum())
        p = float(wilcoxon(vals)[1]) if np.any(vals != 0) else 1.0
        return pos, neg, p

    summary = []
    for m in MODELS:
        r = [x for x in rows if x["model"] == model_label(m)]
        if not r:
            continue
        a_count = sum(x["schema_recall"] >= 0.5 for x in r)
        bp, bn, b_p = test([x["B_effect"] for x in r])
        cp, cn, c_p = test([x["C_effect"] for x in r])
        summary.append({
            "model": model_label(m), "datasets": len(r),
            "identified_card": sum(x["id_card"] for x in r),
            "identified_names": sum(x["id_names"] for x in r),
            "schema_recall_median": float(np.median([x["schema_recall"] for x in r])),
            "A_datasets_recall_ge_0.5": a_count, "A_holds": a_count >= 8,
            "rho_P3_perm_median": float(np.median([x["rho_P3_perm"] for x in r])),
            "rho_P3f_perm_median": float(np.median([x["rho_P3f_perm"] for x in r])),
            "B_pos": bp, "B_neg": bn, "B_p": b_p,
            "B_effect_median": float(np.median([x["B_effect"] for x in r])),
            "rho_P4_perm_median": float(np.median([x["rho_P4_perm"] for x in r])),
            "rho_P5_perm_median": float(np.median([x["rho_P5_perm"] for x in r])),
            "C_pos": cp, "C_neg": cn, "C_p": c_p,
            "C_effect_median": float(np.median([x["C_effect"] for x in r])),
            "layout_recall_median": float(np.median([x["rho_P3_P4"] for x in r]))})
    # Holm over the models, for B and C.
    for key in ("B", "C"):
        order = np.argsort([s[f"{key}_p"] for s in summary])
        running = 0.0
        for rank, i in enumerate(order):
            running = max(running, min(1.0, (len(summary) - rank) * summary[i][f"{key}_p"]))
            summary[i][f"{key}_p_holm"] = running
    for s in summary:
        s["B_holds"] = s["B_pos"] > s["B_neg"] and s["B_p_holm"] < 0.05
        s["C_holds"] = s["C_pos"] > s["C_neg"] and s["C_p_holm"] < 0.05
        s["H12_holds"] = s["A_holds"] and s["B_holds"]
    _write_csv(tables / "criterion.csv", summary)
    n_hold = sum(s["H12_holds"] for s in summary)
    for s in summary:
        print(f"{s['model']:28s} A {s['A_datasets_recall_ge_0.5']:2d}/16 {'Y' if s['A_holds'] else 'n'}"
              f"  B {s['B_pos']}-{s['B_neg']} p_holm {s['B_p_holm']:.4f} "
              f"{'Y' if s['B_holds'] else 'n'}  C {s['C_pos']}-{s['C_neg']} p_holm "
              f"{s['C_p_holm']:.4f} {'Y' if s['C_holds'] else 'n'}"
              f"  -> {'holds' if s['H12_holds'] else '--'}")
    n_c = sum(s["H12_holds"] and s["C_holds"] for s in summary)
    print(f"H12 (A and B) holds for {n_hold} of {len(summary)} models "
          f"({'supported' if n_hold >= 7 else 'not supported'} at >= 7); "
          f"with C as well for {n_c} ({'dataset-specific' if n_c >= 7 else 'not dataset-specific'})")
    return 0


def _write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------- main
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("truth", help="mutual information and permutation importance")
    t.add_argument("--datasets", default=",".join(DATASETS))
    p = sub.add_parser("probe", help="the six probes, every model and dataset")
    p.add_argument("--datasets", default=",".join(DATASETS))
    p.add_argument("--models", default=",".join(MODELS))
    p.add_argument("--experiment", help="experiment ID (evidence); omit for a pilot")
    p.add_argument("--log", type=Path, default=CALL_LOG)
    p.add_argument("--out", type=Path, default=PROBE_DIR)
    p.add_argument("--workers", type=int, default=16)
    p.add_argument("--max-cost", type=float, default=MAX_COST)
    s = sub.add_parser("score", help="tables and the criterion")
    s.add_argument("--out", type=Path, default=REPORT_DIR)
    args = ap.parse_args(argv)

    if args.cmd == "truth":
        for d in args.datasets.split(","):
            print(make_truth(d), flush=True)
        return 0
    if args.cmd == "score":
        return score(args.out)

    import provenance
    datasets, models = args.datasets.split(","), args.models.split(",")
    config = {"datasets": datasets, "models": models, "seed": SEED,
              "probes": PROBES, "max_cost": args.max_cost, "fake_name": FAKE_NAME,
              "systems": [SCORE_SYSTEM, IDENTIFY_SYSTEM, SCHEMA_SYSTEM]}
    name = "h12e01_probes" if args.experiment else "h12_pilot"
    with provenance.Run(name, params=config, experiment_id=args.experiment) as run:
        log = lg.CallLog(args.log, "record", lg.OpenRouterClient(), max_cost=args.max_cost)
        failures = []
        info = {}
        for d in datasets:        # names and classes only; each set loaded once
            _, dic, names, _ = variables(d)
            info[d] = (names, dic["class_names"])
        # Every (dataset, model) pair in parallel, the widest datasets first.
        todo = [(d, m) for d in sorted(datasets, key=lambda d: -len(info[d][0]))
                for m in models if not (args.out / probe_path(d, m).name).is_file()]

        def one(t):
            d, m = t
            try:
                doc = run_probes(d, m, log, *info[d])
                args.out.mkdir(parents=True, exist_ok=True)
                (args.out / probe_path(d, m).name).write_text(
                    json.dumps(doc, indent=1), encoding="utf-8")
                return f"{d} {m}: done"
            except Exception as exc:  # noqa: BLE001  record it, go on
                failures.append({"dataset": d, "model": m, "error": str(exc)[:300]})
                return f"{d} {m}: FAILED {type(exc).__name__}: {str(exc)[:200]}"
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            for i, msg in enumerate(pool.map(one, todo), 1):
                print(f"[{i}/{len(todo)}] {msg}", flush=True)
        run.record("calls_sent", log.sent)
        run.record("calls_replayed", log.replayed)
        run.record("spent_usd", log.spent())
        run.record("failures", failures)
        run.record("algorithm_id", run.algorithm_id("h12_probes", config))
        print(f"{log.sent} calls sent, {log.replayed} replayed, ${log.spent():.2f} in the log; "
              f"{len(failures)} failed; run {run.run_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
