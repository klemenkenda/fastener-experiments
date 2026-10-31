"""H12-E01's figures and extra tables, from `h12_probes.py score`'s tables.

    python experiments/h12_probes.py score      # tables/probes.csv, criterion.csv
    python experiments/h12_report.py            # figures/, tables/readings.csv

Figures are wide, datasets along x and models along y (heatmaps), or models
along x where the model is the unit. Every number in a cell is the one in
tables/probes.csv.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import wilcoxon  # noqa: E402

import h12_probes as h  # noqa: E402

OUT = h.REPORT_DIR
MODELS = [h.model_label(m) for m in h.MODELS]
SHORT = {"claude-opus-5.5": "Opus 5.5", "claude-sonnet-5.5": "Sonnet 5.5",
         "claude-haiku-5.5": "Haiku 5.5", "llama-3.3-70b-instruct": "Llama 3.3 70B",
         "gemma-3-4b-it": "Gemma 3 4B", "gemma-3-27b-it": "Gemma 3 27B",
         "mistralai/ministral-8b-2512": "Ministral 8B", "ministral-8b-2512": "Ministral 8B",
         "qwen3-14b": "Qwen3 14B", "phi-4": "Phi-4", "deepseek-v4-flash": "DeepSeek V4 Flash",
         "gpt-6-luna": "GPT-6 Luna", "gemini-2.5-flash-lite": "Gemini 2.5 Flash-Lite"}
# The distributed files that name their columns generically (OpenML's V1..,
# UCI crop mapping's f1..): a generic list there is the file's real header.
GENERIC_FILES = ("har", "qsar_biodeg", "gas_drift", "ozone_8hr", "crop_mapping")


def holm(ps):
    ps = np.asarray(ps, float)
    order, out, running = np.argsort(ps), np.empty(len(ps)), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        out[i] = running
    return out


def test(v):
    v = np.asarray(v, float)
    return (int((v > 0).sum()), int((v < 0).sum()),
            float(wilcoxon(v)[1]) if np.any(v != 0) else 1.0)


def heatmap(ax, d, value, vmin, vmax, cmap, fmt="{:.2f}", order=None):
    piv = d.pivot(index="model", columns="dataset", values=value).reindex(MODELS)
    piv = piv[order or list(h.DATASETS)]
    im = ax.imshow(piv.values.astype(float), cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(piv.shape[1]), piv.columns, rotation=40, ha="right", fontsize=8)
    ax.set_yticks(range(piv.shape[0]), [SHORT[m] for m in piv.index], fontsize=8)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            x = piv.values[i, j]
            if isinstance(x, (bool, np.bool_)):
                x = float(x)
            ax.text(j, i, fmt.format(x), ha="center", va="center", fontsize=6.5,
                    color="white" if abs(x - (vmin + vmax) / 2) > 0.35 * (vmax - vmin) else "black")
    return im


def main() -> int:
    d = pd.read_csv(OUT / "tables" / "probes.csv")
    c = pd.read_csv(OUT / "tables" / "criterion.csv").set_index("model").reindex(MODELS)
    figs = OUT / "figures"
    figs.mkdir(parents=True, exist_ok=True)

    # Readings beside the criterion: B and C against mutual information
    # (secondary truth), B on the datasets each model identified from the
    # card vs not, and A with a generic header counted where the file has one.
    rows = []
    for m in MODELS:
        r = d[d.model == m]
        bp, bn, b_p = test(r.B_effect_mi)
        cp, cn, c_p = test(r.C_effect_mi)
        ident = r[r.id_card]
        row = {"model": m, "B_mi_pos": bp, "B_mi_neg": bn, "B_mi_p": b_p,
               "B_mi_median": float(r.B_effect_mi.median()),
               "C_mi_pos": cp, "C_mi_neg": cn, "C_mi_p": c_p,
               "B_median_identified": float(ident.B_effect.median()) if len(ident) else np.nan,
               "B_median_not_identified": float(r[~r.id_card].B_effect.median())
               if (~r.id_card).any() else np.nan,
               "n_identified_card": int(r.id_card.sum()),
               "P3_flat": int(r.P3_flat.sum()), "P3f_flat": int(r.P3f_flat.sum())}
        rows.append(row)
    rd = pd.DataFrame(rows)
    rd["B_mi_p_holm"], rd["C_mi_p_holm"] = holm(rd.B_mi_p), holm(rd.C_mi_p)
    rd["B_mi_holds"] = (rd.B_mi_pos > rd.B_mi_neg) & (rd.B_mi_p_holm < 0.05)
    rd["A_holds"] = c.A_holds.values
    rd["A_and_B_mi"] = rd.A_holds & rd.B_mi_holds
    rd.to_csv(OUT / "tables" / "readings.csv", index=False)
    print(rd[["model", "B_mi_pos", "B_mi_neg", "B_mi_p_holm", "B_mi_holds", "A_and_B_mi",
              "B_median_identified", "B_median_not_identified"]].round(4).to_string())

    # F1: the criterion, B per dataset and model, the model's test on the right.
    fig, ax = plt.subplots(figsize=(15, 6))
    im = heatmap(ax, d, "B_effect", -0.9, 0.9, "RdBu")
    for i, m in enumerate(MODELS):
        s = c.loc[m]
        ax.text(len(h.DATASETS) - 0.3, i, f"{int(s.B_pos)}-{int(s.B_neg)}  Holm p {s.B_p_holm:.3f}"
                f"   A {int(s['A_datasets_recall_ge_0.5'])}/16", va="center", fontsize=8)
    ax.set_xlim(-0.5, len(h.DATASETS) + 3.6)
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01,
                 label="B = rho(P3, perm. imp.) - rho(P3f, perm. imp.)")
    ax.set_title("F1 -- B per dataset: positional scores with the real name minus with a fictitious "
                 "name, Spearman with LightGBM permutation importance (validation split)", fontsize=10)
    fig.tight_layout()
    fig.savefig(figs / "F1_criterion.png", dpi=130)
    plt.close(fig)

    # F2: recognition -- schema recall, with identification marks.
    fig, ax = plt.subplots(figsize=(15, 6))
    im = heatmap(ax, d, "schema_recall", 0, 1, "Greens")
    piv_c = d.pivot(index="model", columns="dataset", values="id_card").reindex(MODELS)[list(h.DATASETS)]
    piv_n = d.pivot(index="model", columns="dataset", values="id_names").reindex(MODELS)[list(h.DATASETS)]
    for i in range(len(MODELS)):
        for j in range(len(h.DATASETS)):
            mark = ("C" if piv_c.values[i, j] else "") + ("N" if piv_n.values[i, j] else "")
            if mark:
                ax.text(j + 0.42, i - 0.3, mark, ha="right", va="top", fontsize=5.5, color="#444")
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01, label="P2 schema recall")
    ax.set_title("F2 -- P2: share of each dataset's variables a model lists given its name; corner "
                 "marks: identified from the card (C), from the names (N)", fontsize=10)
    fig.tight_layout()
    fig.savefig(figs / "F2_recognition.png", dpi=130)
    plt.close(fig)

    # F3: layout recall, rho(P3 by position, P4 by column).
    fig, ax = plt.subplots(figsize=(15, 6))
    im = heatmap(ax, d, "rho_P3_P4", -1, 1, "RdBu")
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01, label="rho(P3, P4)")
    ax.set_title("F3 -- Layout recall: Spearman of the positional scores (P3, no names) with the "
                 "named scores (P4) of the same columns", fontsize=10)
    fig.tight_layout()
    fig.savefig(figs / "F3_layout.png", dpi=130)
    plt.close(fig)

    # F4: B under both truths, per model (the unit), with the per-dataset spread.
    fig, ax = plt.subplots(figsize=(15, 5))
    x = np.arange(len(MODELS))
    for k, (col, lab, colr, p) in enumerate((("B_effect", "permutation importance (primary)",
                                               "#2b6cb0", c.B_p_holm.values),
                                              ("B_effect_mi", "mutual information (secondary)",
                                               "#c05621", rd.B_mi_p_holm.values))):
        off = -0.18 if k == 0 else 0.18
        for i, m in enumerate(MODELS):
            v = d[d.model == m][col].values
            ax.scatter(np.full(len(v), i + off) + np.random.RandomState(i).uniform(-0.06, 0.06, len(v)),
                       v, s=9, color=colr, alpha=0.45)
            ax.plot([i + off - 0.12, i + off + 0.12], [np.median(v)] * 2, color=colr, lw=2.5)
            ax.text(i + off, 0.98, f"{p[i]:.3f}", ha="center", fontsize=6.5, color=colr)
        ax.plot([], [], color=colr, lw=2.5, label=f"{lab}: datasets (dots), median (bar), Holm p (top)")
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks(x, [SHORT[m] for m in MODELS], rotation=20, ha="right", fontsize=8)
    ax.set_ylim(-0.7, 1.05)
    ax.set_ylabel("B per dataset")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("F4 -- B against the two truths: the 16 datasets per model", fontsize=10)
    fig.tight_layout()
    fig.savefig(figs / "F4_truths.png", dpi=130)
    plt.close(fig)

    # F5: C, the dataset's name on top of the feature names.
    fig, ax = plt.subplots(figsize=(15, 6))
    im = heatmap(ax, d, "C_effect", -0.9, 0.9, "RdBu")
    for i, m in enumerate(MODELS):
        s = c.loc[m]
        ax.text(len(h.DATASETS) - 0.3, i, f"{int(s.C_pos)}-{int(s.C_neg)}  Holm p {s.C_p_holm:.3f}",
                va="center", fontsize=8)
    ax.set_xlim(-0.5, len(h.DATASETS) + 2.6)
    fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01,
                 label="C = partial rho(P4, perm. imp. | P5)")
    ax.set_title("F5 -- C per dataset: what the named scores with the dataset's name (P4) know of "
                 "permutation importance beyond the same names without it (P5)", fontsize=10)
    fig.tight_layout()
    fig.savefig(figs / "F5_names.png", dpi=130)
    plt.close(fig)
    return 0


if __name__ == "__main__":
    sys.exit(main())
