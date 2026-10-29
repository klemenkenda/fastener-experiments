"""LLM guidance for FASTENER through OpenRouter (H8).

FASTENER takes outside guidance through two hooks (fastener/guidance.py): a
feature prior, resolved once before the search, and a subset proposer, asked
every few generations. This module makes both from a chat model on
OpenRouter (https://openrouter.ai), any model it serves, chosen by its ID.

Every call goes through a `CallLog`: a JSON-lines file with the request and
the full response. In `record` mode a call that is not in the log is sent and
appended; in `replay` mode it must be in the log, so a run on the cluster --
whose compute nodes need no network and no key -- gets exactly the responses
recorded on the PI's machine. A request is matched by a hash of the model and
the messages, and FASTENER's search is deterministic for a seed, so a
replayed run asks the same questions in the same order.

A prior is also saved as one committed JSON file (`save_prior`), with the
model ID asked and served, the prompt, the raw response and the scores;
`load_prior` reads it back as the array FASTENER takes.

    # the key: OPENROUTER_API_KEY in the environment, or in the repository's
    # git-ignored .env (a placeholder is there; .env.example shows the form)
    python experiments/llm_guidance.py prior --dataset covertype \\
        --model anthropic/claude-sonnet-5.5 [--scrambled] [--dictionary <json>]
    python experiments/llm_guidance.py batch --datasets a,b --models m1,m2

Scrambled priors (H8's control) show the model neutral tokens instead of the
feature names and drop their descriptions; the task and class names stay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

import numpy as np

import _bootstrap  # noqa: F401  (puts the FASTENER clone on the path)
from guidance import GuidanceContext, ProposalContext

HERE = Path(__file__).resolve().parent
PRIORS_DIR = HERE / "priors"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
KEY_ENV = "OPENROUTER_API_KEY"

Transport = Callable[[str, Dict[str, str], Dict[str, Any], float], Dict[str, Any]]


ENV_FILE = HERE.parent / ".env"


def api_key_from_env_file(path: Path = ENV_FILE) -> Optional[str]:
    """OPENROUTER_API_KEY from the repository's git-ignored .env, if set."""
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() == KEY_ENV:
            return value.strip().strip('"').strip("'") or None
    return None


def _http_post(url: str, headers: Dict[str, str], body: Dict[str, Any],
               timeout: float) -> Dict[str, Any]:
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


class OpenRouterClient:
    """A minimal chat-completions client. `transport` replaces the HTTP call
    (tests); the key is read from OPENROUTER_API_KEY when not given."""

    def __init__(self, api_key: Optional[str] = None, url: str = API_URL,
                 timeout: float = 300.0, retries: int = 3,
                 transport: Optional[Transport] = None) -> None:
        # The argument, else the environment, else the repository's .env.
        self.api_key = (api_key if api_key is not None
                        else os.environ.get(KEY_ENV) or api_key_from_env_file())
        self.url, self.timeout, self.retries = url, timeout, retries
        self.transport = transport or _http_post

    def chat(self, body: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key and self.transport is _http_post:
            raise RuntimeError(f"no OpenRouter key: set {KEY_ENV} in the "
                               f"environment or in {ENV_FILE}")
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json",
                   "X-Title": "FASTENER experiments"}
        for attempt in range(self.retries):
            try:
                return self.transport(self.url, headers, body, self.timeout)
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt + 1 == self.retries:
                    raise RuntimeError(f"OpenRouter call failed: {exc}") from exc
                time.sleep(2 ** attempt)
        raise AssertionError("unreachable")


def request_key(body: Dict[str, Any]) -> str:
    """What identifies a request: the model, the messages and the sampling
    settings, not transport details."""
    core = {k: body.get(k) for k in ("model", "messages", "temperature", "seed",
                                     "max_tokens", "response_format")}
    return hashlib.sha256(json.dumps(core, sort_keys=True).encode("utf-8")).hexdigest()


class CallLog:
    """Record-or-replay log of model calls, one JSON object per line."""

    def __init__(self, path: Path, mode: str = "record",
                 client: Optional[OpenRouterClient] = None) -> None:
        if mode not in ("record", "replay"):
            raise ValueError("mode is 'record' or 'replay'")
        self.path, self.mode = Path(path), mode
        self.client = client
        self.entries: Dict[str, Dict[str, Any]] = {}
        if self.path.is_file():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    e = json.loads(line)
                    self.entries[e["key"]] = e
        self.sent = 0
        self.replayed = 0

    def call(self, body: Dict[str, Any]) -> Dict[str, Any]:
        key = request_key(body)
        if key in self.entries:
            self.replayed += 1
            return self.entries[key]["response"]
        if self.mode == "replay":
            raise KeyError(f"{self.path}: no recorded response for request {key[:12]} "
                           f"(model {body.get('model')}); record it first")
        if self.client is None:
            raise RuntimeError("record mode needs a client")
        t0 = time.time()
        response = self.client.chat(body)
        entry = {"key": key, "utc": datetime.now(timezone.utc).isoformat(),
                 "seconds": round(time.time() - t0, 2), "request": body,
                 "response": response}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
        self.entries[key] = entry
        self.sent += 1
        return response


def content_of(response: Dict[str, Any]) -> str:
    try:
        return response["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"unexpected response: {str(response)[:300]}") from exc


def parse_json(text: str) -> Any:
    """The JSON object in a reply, with or without a code fence around it."""
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if fence:
        text = fence.group(1)
    start = min([i for i in (text.find("{"), text.find("[")) if i >= 0], default=-1)
    if start < 0:
        raise ValueError(f"no JSON in reply: {text[:200]!r}")
    return json.JSONDecoder().raw_decode(text[start:])[0]


def neutral_names(n: int) -> List[str]:
    width = len(str(max(n - 1, 0)))
    return [f"feature_{i:0{width}d}" for i in range(n)]


def _feature_lines(ctx: GuidanceContext, scrambled: bool,
                   indices: Sequence[int]) -> List[str]:
    names = neutral_names(ctx.n_features) if scrambled else ctx.feature_names
    desc = {} if scrambled else (ctx.metadata.get("feature_descriptions") or {})
    out = []
    for i in indices:
        d = desc.get(ctx.feature_names[i]) or desc.get(str(i))
        out.append(f"{i}: {names[i]}" + (f" -- {d}" if d else ""))
    return out


def _task_lines(ctx: GuidanceContext) -> List[str]:
    lines = []
    if ctx.task:
        lines.append(f"Task: {ctx.task}")
    if ctx.class_names:
        lines.append("Classes: " + ", ".join(map(str, ctx.class_names)))
    if ctx.metadata.get("dataset_description"):
        lines.append(f"Data: {ctx.metadata['dataset_description']}")
    return lines


PRIOR_INSTRUCTIONS = (
    "You are helping a feature-selection search for a classification task. "
    "Rate how useful each feature is likely to be for predicting the class, "
    "on its own or together with a few others, from 0 (useless) to 1 (most "
    "useful). Use only your knowledge of the domain and the descriptions "
    "given; you do not see the data. Reply with a JSON object only: "
    '{"scores": {"<feature index>": <score>, ...}} with one entry for every '
    "feature index listed.")

PROPOSER_INSTRUCTIONS = (
    "You are helping a feature-selection search for a classification task. "
    "Below is the search's current best subset for each size, with its "
    "validation score (weighted F1, higher is better). Propose new feature "
    "subsets of at most {max_k} features that you expect to score higher than "
    "the current subsets of the same size. Use feature indices. Reply with a "
    'JSON object only: {{"subsets": [[<index>, ...], ...]}}, at most '
    "{max_subsets} subsets.")


class LLMFeaturePrior:
    """A FASTENER feature prior from one (or a few, for wide data) calls."""

    def __init__(self, log: CallLog, model: str, scrambled: bool = False,
                 temperature: float = 0.0, seed: int = 20200,
                 chunk: int = 300, max_tokens: int = 16000) -> None:
        self.log, self.model, self.scrambled = log, model, scrambled
        self.temperature, self.seed, self.chunk = temperature, seed, chunk
        self.max_tokens = max_tokens
        self.record: Dict[str, Any] = {}

    def messages(self, ctx: GuidanceContext, indices: Sequence[int]) -> List[Dict[str, str]]:
        user = "\n".join(_task_lines(ctx) + ["", f"Features ({len(indices)} of "
                                             f"{ctx.n_features}):"]
                         + _feature_lines(ctx, self.scrambled, indices))
        return [{"role": "system", "content": PRIOR_INSTRUCTIONS},
                {"role": "user", "content": user}]

    def __call__(self, ctx: GuidanceContext) -> np.ndarray:
        scores = np.full(ctx.n_features, np.nan)
        calls = []
        for start in range(0, ctx.n_features, self.chunk):
            idx = list(range(start, min(start + self.chunk, ctx.n_features)))
            body = {"model": self.model, "messages": self.messages(ctx, idx),
                    "temperature": self.temperature, "seed": self.seed,
                    "max_tokens": self.max_tokens}
            response = self.log.call(body)
            text = content_of(response)
            parsed = parse_json(text).get("scores", {})
            for k, v in parsed.items():
                try:
                    i, x = int(k), float(v)
                except (TypeError, ValueError):
                    continue
                if i in idx and np.isfinite(x):
                    scores[i] = min(max(x, 0.0), 1.0)
            calls.append({"key": request_key(body), "served_model": response.get("model"),
                          "usage": response.get("usage"), "reply": text})
        missing = [int(i) for i in np.flatnonzero(np.isnan(scores))]
        # A feature the model left out gets the lowest score it gave any.
        fill = np.nanmin(scores) if len(missing) < ctx.n_features else 0.0
        scores[np.isnan(scores)] = fill
        self.record = {"model": self.model, "scrambled": self.scrambled,
                       "temperature": self.temperature, "seed": self.seed,
                       "instructions": PRIOR_INSTRUCTIONS, "calls": calls,
                       "missing": missing, "fill": float(fill)}
        return scores


class LLMSubsetProposer:
    """A FASTENER subset proposer: shows the front, asks for new subsets."""

    def __init__(self, log: CallLog, model: str, max_subsets: int = 5,
                 max_k: int = 10, temperature: float = 0.0, seed: int = 20200,
                 max_tokens: int = 4000, scrambled: bool = False,
                 show_weights: bool = False) -> None:
        self.log, self.model = log, model
        self.max_subsets, self.max_k = max_subsets, max_k
        self.temperature, self.seed, self.max_tokens = temperature, seed, max_tokens
        self.scrambled, self.show_weights = scrambled, show_weights
        self.calls: List[Dict[str, Any]] = []

    def messages(self, ctx: ProposalContext) -> List[Dict[str, str]]:
        g = ctx.guidance
        names = neutral_names(g.n_features) if self.scrambled else g.feature_names
        front = [f"size {e['size']}: {e['features']} "
                 f"({', '.join(names[i] for i in e['features'])}) -> {e['score']:.4f}"
                 for e in ctx.front if e["size"] <= self.max_k]
        budget = (f"{ctx.model_fits} of {ctx.max_model_fits} model fits spent"
                  if ctx.max_model_fits else f"{ctx.model_fits} model fits spent")
        lines = _task_lines(g) + ["", f"Features ({g.n_features}):"] + \
            _feature_lines(g, self.scrambled, range(g.n_features))
        if self.show_weights and ctx.feature_weights is not None:
            lines += ["", "Current feature weights (higher = more relevant so far): "
                      + json.dumps({i: round(w, 3) for i, w in enumerate(ctx.feature_weights)})]
        lines += ["", f"Generation {ctx.generation}; {budget}.", "Current front:"] + front
        system = PROPOSER_INSTRUCTIONS.format(max_k=self.max_k,
                                              max_subsets=self.max_subsets)
        return [{"role": "system", "content": system},
                {"role": "user", "content": "\n".join(lines)}]

    def __call__(self, ctx: ProposalContext) -> List[List[int]]:
        body = {"model": self.model, "messages": self.messages(ctx),
                "temperature": self.temperature, "seed": self.seed,
                "max_tokens": self.max_tokens}
        response = self.log.call(body)
        text = content_of(response)
        try:
            subsets = parse_json(text).get("subsets", [])
        except (ValueError, AttributeError):
            subsets = []
        out = []
        for s in subsets[: self.max_subsets]:
            try:
                idx = [int(i) for i in s][: self.max_k]
            except (TypeError, ValueError):
                continue
            out.append(idx)
        self.calls.append({"generation": ctx.generation, "key": request_key(body),
                           "served_model": response.get("model"), "subsets": out})
        return out


# ------------------------------------------------------------------ files
def prior_path(dataset: str, model: str, scrambled: bool) -> Path:
    slug = re.sub(r"[^A-Za-z0-9.-]+", "-", model)
    return PRIORS_DIR / f"{dataset}__{slug}{'__scrambled' if scrambled else ''}.json"


def save_prior(path: Path, dataset: str, ctx: GuidanceContext,
               prior: LLMFeaturePrior, scores: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {"dataset": dataset, "created_utc": datetime.now(timezone.utc).isoformat(),
           "n_features": ctx.n_features, "feature_names": list(ctx.feature_names),
           "task": ctx.task, "class_names": ctx.class_names,
           **prior.record, "scores": [float(x) for x in scores]}
    path.write_text(json.dumps(doc, indent=1), encoding="utf-8")


def load_prior(path: Path, n_features: Optional[int] = None) -> np.ndarray:
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    scores = np.asarray(doc["scores"], dtype=float)
    if n_features is not None and len(scores) != n_features:
        raise ValueError(f"{path}: {len(scores)} scores for {n_features} features")
    return scores


def context_for(ds, dictionary: Optional[Dict[str, Any]] = None) -> GuidanceContext:
    """A guidance context from a loaded dataset and its data dictionary
    (task, class_names, dataset_description, feature_descriptions)."""
    d = dictionary or {}
    # A dictionary may restore documented names for a set stored with
    # generic ones (har's V1..V561, ozone_8hr's V1..V72), column for column.
    names = d.get("feature_names") or [str(n) for n in ds.feature_names]
    if len(names) != ds.n_features:
        raise ValueError(f"dictionary has {len(names)} feature names for "
                         f"{ds.n_features} features")
    return GuidanceContext(
        n_features=ds.n_features,
        feature_names=[str(n) for n in names],
        task=d.get("task"), class_names=d.get("class_names"),
        metadata={k: d[k] for k in ("dataset_description", "feature_descriptions")
                  if k in d})


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prior", help="make and save a feature prior")
    p.add_argument("--dataset", required=True)
    p.add_argument("--model", required=True, help="OpenRouter model ID")
    p.add_argument("--scrambled", action="store_true")
    p.add_argument("--dictionary", type=Path,
                   help="data dictionary JSON (default priors/dictionaries/<dataset>.json)")
    p.add_argument("--log", type=Path, help="call log (default priors/calls.jsonl)")
    p.add_argument("--out", type=Path)
    b = sub.add_parser("batch", help="every prior an experiment needs, skipping "
                                     "those already made")
    b.add_argument("--datasets", required=True, help="comma list")
    b.add_argument("--models", required=True, help="comma list of OpenRouter IDs")
    b.add_argument("--log", type=Path)
    args = ap.parse_args(argv)

    if args.cmd == "batch":
        log = CallLog(args.log or PRIORS_DIR / "calls.jsonl", "record", OpenRouterClient())
        todo = [(d, m, s) for d in args.datasets.split(",") for m in args.models.split(",")
                for s in (False, True)]
        for i, (d, m, s) in enumerate(todo, 1):
            out = prior_path(d, m, s)
            if out.is_file():
                print(f"[{i}/{len(todo)}] {out.name}: exists")
                continue
            make_one(d, m, s, log, out, None)
            print(f"[{i}/{len(todo)}] {out.name}: made", flush=True)
        print(f"{log.sent} calls sent, {log.replayed} replayed")
        return 0
    log = CallLog(args.log or PRIORS_DIR / "calls.jsonl", "record", OpenRouterClient())
    out = args.out or prior_path(args.dataset, args.model, args.scrambled)
    prior, ctx = make_one(args.dataset, args.model, args.scrambled, log, out,
                          args.dictionary)
    print(f"{out}: {ctx.n_features} scores, {len(prior.record['missing'])} missing, "
          f"{log.sent} calls sent, {log.replayed} replayed")
    return 0


def make_one(dataset: str, model: str, scrambled: bool, log: CallLog, out: Path,
             dictionary_path: Optional[Path] = None):
    """Make, save and return one prior (and its context)."""
    from datasets import load
    import protocol
    ds = load(dataset, max_rows=protocol.ROW_CAP)
    dpath = dictionary_path or PRIORS_DIR / "dictionaries" / f"{dataset}.json"
    dictionary = json.loads(dpath.read_text(encoding="utf-8")) if dpath.is_file() else None
    ctx = context_for(ds, dictionary)
    prior = LLMFeaturePrior(log, model, scrambled=scrambled)
    scores = prior(ctx)
    save_prior(out, dataset, ctx, prior, scores)
    return prior, ctx


if __name__ == "__main__":
    sys.exit(main())
