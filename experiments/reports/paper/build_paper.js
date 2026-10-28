// Builds FASTENER_experiments_report.docx, the summary paper of the
// experiments so far, from the committed reports and paper_data.json.
//
//   python experiments/reports/paper/make_paper_figures.py
//   node experiments/reports/paper/build_paper.js
//
// Needs the npm package docx (npm install docx); NODE_PATH may point at it.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType, LevelFormat,
  Footer, PageNumber, PageBreak,
} = require("docx");

const HERE = __dirname;
const REPORTS = path.dirname(HERE);
const DATA = JSON.parse(fs.readFileSync(path.join(HERE, "paper_data.json"), "utf8"));
const CONTENT_W = 9360; // A4 with 1.0" margins on a 6.5" text column, in DXA

// ------------------------------------------------------------------ helpers
function runs(text, opts = {}) {
  // **bold**, *italic* and `code` inline markup
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/).filter((s) => s.length);
  return parts.map((s) => {
    if (s.startsWith("`")) return new TextRun({ text: s.slice(1, -1), font: "Consolas", ...opts, size: Math.round((opts.size || 21) * 0.9) });
    if (s.startsWith("**")) return new TextRun({ text: s.slice(2, -2), bold: true, ...opts });
    if (s.startsWith("*")) return new TextRun({ text: s.slice(1, -1), italics: true, ...opts });
    return new TextRun({ text: s, ...opts });
  });
}
const P = (text, o = {}) => new Paragraph({ children: runs(text, o.run || {}), spacing: { after: 120 },
  alignment: o.align || AlignmentType.JUSTIFIED, ...(o.para || {}) });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(t)] });
const B = (text, level = 0) => new Paragraph({ numbering: { reference: "bullets", level },
  children: runs(text), spacing: { after: 60 } });
const N = (text, ref = "numbers") => new Paragraph({ numbering: { reference: ref, level: 0 },
  children: runs(text), spacing: { after: 60 } });

let figNo = 0, tabNo = 0;
function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}
function figure(rel, caption, widthIn = 6.5) {
  const file = path.join(REPORTS, rel);
  const { w, h, data } = pngSize(file);
  const wpx = Math.round(widthIn * 96), hpx = Math.round(wpx * h / w);
  figNo += 1;
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, keepNext: true,
      children: [new ImageRun({ type: "png", data, transformation: { width: wpx, height: hpx },
        altText: { title: `Figure ${figNo}`, description: caption, name: `fig${figNo}` } })] }),
    new Paragraph({ spacing: { after: 200 }, alignment: AlignmentType.JUSTIFIED,
      children: [new TextRun({ text: `Figure ${figNo}. `, bold: true, size: 18 }), ...runs(caption, { size: 18 })] }),
  ];
}
const border = { style: BorderStyle.SINGLE, size: 4, color: "B0B0B0" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(header, rows, widths, caption, o = {}) {
  const size = o.size || 18;
  const total = widths.reduce((a, b) => a + b, 0);
  // keepNext on every row but the last keeps a table on one page in Word.
  const cell = (t, w, i, head, bold, last) => new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: head ? { fill: "DCE6F0", type: ShadingType.CLEAR, color: "auto" }
      : (bold ? { fill: "E8F3E0", type: ShadingType.CLEAR, color: "auto" } : undefined),
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ keepNext: !last, alignment: (i > 0 && o.numeric && o.numeric.includes(i)) ? AlignmentType.RIGHT : AlignmentType.LEFT,
      children: runs(String(t), { size, bold: head || bold }) })],
  });
  tabNo += 1;
  const out = [];
  if (caption) out.push(new Paragraph({ spacing: { before: 120, after: 60 }, keepNext: true,
    children: [new TextRun({ text: `Table ${tabNo}. `, bold: true, size: 18 }), ...runs(caption, { size: 18 })] }));
  out.push(new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true, children: header.map((t, i) => cell(t, widths[i], i, true)) }),
      ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((t, i) => {
        const bold = o.boldCells && o.boldCells.has(`${ri},${i}`);
        return cell(t, widths[i], i, false, bold, ri === rows.length - 1);
      }) })),
    ],
  }));
  out.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
  return out;
}

const LABEL = {
  fastener: "FASTENER (stock)", fastener_swap_guided: "FASTENER, guided swap",
  fastener_swap_random: "FASTENER, random swap", nsga2_sparse: "NSGA-II, sparse start",
  nsga2: "NSGA-II, OBL start", nsgaii_miip: "NSGAII-MIIP", poss: "POSS", fs_sds: "FS-SDS",
  boruta: "Boruta", rfe_tree: "RFE", tree_importance: "tree-importance ranker", mrmr: "mRMR",
  hsic_lasso: "HSIC Lasso", relieff: "ReliefF", kbest_mutual_info: "MI ranker",
  kbest_anova_f: "ANOVA-F ranker", random: "random subsets", all_features: "all features",
};
const ORDER = ["fastener", "fastener_swap_guided", "fastener_swap_random", "nsga2_sparse", "nsga2",
  "nsgaii_miip", "poss", "fs_sds", "boruta", "rfe_tree", "tree_importance", "mrmr", "hsic_lasso",
  "relieff", "kbest_mutual_info", "kbest_anova_f", "random"];
const CL = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "EO", "all"];

function fmtS(s) {
  if (s < 10) return s.toFixed(1) + " s";
  if (s < 120) return Math.round(s) + " s";
  if (s < 7200) return (s / 60).toFixed(0) + " min";
  return (s / 3600).toFixed(1) + " h";
}
function timeTable() {
  const T = ["H5H6-E01", "H5H6-E02", "H5H6-E03"].map((e) =>
    Object.fromEntries(DATA[e].time.map((r) => [r.method, r])));
  const rows = [...ORDER, "all_features"].map((m) => [LABEL[m],
    ...T.flatMap((t) => [fmtS(t[m].median_s), t[m].total_h.toFixed(1)])]);
  return table(["method", "tree: median run", "tree: total h", "forest: median run",
    "forest: total h", "LightGBM: median run", "LightGBM: total h"], rows,
  [2460, 1150, 1150, 1150, 1150, 1150, 1150],
  "Wall clock per run, by method. Tree = H5H6-E01, one core per run on the workstation; forest = H5H6-E02 and LightGBM = H5H6-E03, 8 cores per run on HPC Vega. Totals sum the finished runs of a method (5 seeds × 39 datasets for the stochastic methods, one run per dataset for the deterministic ones); they leave out the runs that hit the 6-hour cap (47 under the tree, none under the forest, 71 under LightGBM) and the 12 skipped cells.",
  { numeric: [1, 2, 3, 4, 5, 6] });
}
function aufTable(exp, learner) {
  const a = Object.fromEntries(DATA[exp].auf.map((r) => [r.method, r]));
  const n = Object.fromEntries(DATA[exp].auf_n.map((r) => [r.method, r]));
  const size = DATA[exp].cluster_size;
  const bold = new Set();
  CL.forEach((c, j) => {
    let best = -1, bi = -1;
    ORDER.forEach((m, i) => { const v = a[m][c]; if (v != null && v > best && n[m][c] === size[c]) { best = v; bi = i; } });
    bold.add(`${bi},${j + 1}`);
  });
  const cell = (m, c) => (a[m][c] == null ? "--"
    : a[m][c].toFixed(3) + (n[m][c] < size[c] ? "†" : ""));
  const rows = ORDER.map((m) => [LABEL[m], ...CL.map((c) => cell(m, c))]);
  return table(["method", ...CL.map((c) => (c === "EO" ? "EOData" : c))], rows,
    [2160, 800, 800, 800, 800, 800, 800, 800, 800, 800],
    `Mean test AUF (K = 10) per cluster, ${learner} (${exp}). Each value averages the cluster's datasets (seeds averaged first); the best value per column among the methods with a result on every dataset of the cluster is shaded. † = the mean leaves out datasets where the method has no result; -- = no result in the cluster (skipped or timed out on every seed).`,
    { size: 16, numeric: [1, 2, 3, 4, 5, 6, 7, 8, 9], boldCells: bold });
}

// ------------------------------------------------------------------ content
const C = [];
// Title block
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 200 },
  children: [new TextRun({ text: "FASTENER under a clean protocol", bold: true, size: 40 })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
  children: [new TextRun({ text: "Seven pre-registered hypotheses on evolutionary feature selection: what holds, what does not, how long it takes, and where to go next", size: 26, italics: true })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "Klemen Kenda", size: 24 })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "Jožef Stefan Institute", size: 22 })] }));
C.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
  children: [new TextRun({ text: "Working paper, 28 October 2026. Covers experiments H0-E01 to H5H6-E03.", size: 20, color: "555555" })] }));

C.push(H1("Abstract"));
C.push(P("FASTENER is a genetic feature-selection algorithm built for Earth-observation data. It was published in 2020 with a lead over FS-SDS on 24 of 25 benchmarks. We re-examined it in a series of pre-registered experiments. One protocol held throughout: one classifier drives and scores every method; the fit budget is fixed per dataset; every subset is chosen on validation and read once on test; and the score is AUF (K = 10), the mean test F1 of the best subset with at most k features, over k = 1..10."));
C.push(P("Seven hypotheses (H0–H6) were tested in twelve completed experiments, on 74 datasets in total, and two of the seven held. Fixing the 2020 mating bugs does not change FASTENER's convergence (H0). NSGA-II's failure at small k is an initialisation artifact: a sparse start fixes it (H1). A random size-preserving swap does nothing (H2). A guided swap helps narrowly, and only on small datasets (H3). The published lead over FS-SDS disappears at equal CPU time, but returns at an equal number of model fits (H4). Neither stock nor guided FASTENER is the best selector across 17 methods and 39 datasets, under a decision tree, a random forest or LightGBM (H5, H6)."));
C.push(P("Across the field, the top is flat: the population searches (three FASTENER variants, sparse-start NSGA-II and, under LightGBM, POSS) are within 0.006 AUF of each other under both ensemble classifiers. Which method leads depends on the dataset cluster and on the classifier. FASTENER runs 4–8 times faster than the NSGA-II family at the same fit budget, but filters are 10–1,000 times cheaper again and win on small, wide datasets. We close with an outlook: the open statistical questions, an extension to regression, and two ways to upgrade FASTENER, with LLM reasoning as a prior and as a search operator, and with an LLM reasoning over a feature knowledge graph."));

// 1 Introduction
C.push(H1("1. Introduction"));
C.push(P("Feature selection for Earth observation (EO) has a specific shape. Thousands to millions of labelled pixels or parcels are described by a few hundred engineered features: spectral bands and vegetation indices, each summarised by temporal statistics over a season. The user wants a **small** subset, often ten features or fewer, because every feature has a cost in acquisition, storage and processing over continental areas. FASTENER (Koprivec, Kenda & Šircelj, *Entropy* 2020) was designed for this setting. It is a genetic algorithm that keeps one best subset per subset size (a Pareto front of size against accuracy). Its mating and pruning steps are guided by mutual information and by permutation importance."));
C.push(P("The original paper compared FASTENER with other selectors under per-method settings: different classifiers, different evaluation budgets and selection on the test split. This makes it hard to say which differences belong to the search. The work reported here re-asks the paper's questions under one protocol, and adds new ones. Every question was written down as a hypothesis with a falsification criterion **before** its experiment ran (`experiments/HYPOTHESES.md`), and every decision taken along the way was logged (`experiments/DECISIONS.md`, DEC-01 to DEC-44)."));
C.push(P("This paper collects the results so far. Section 2 describes the data, Section 3 the methods and the protocol, and Section 4 the changes made to FASTENER itself. Section 5 states the hypotheses, and Section 6 evaluates them one by one, with the additional findings each experiment produced. Section 7 reports how long each method took. Section 8 looks at which methods have potential in which data cluster. Section 9 discusses the results, and Section 10 gives the outlook."));

// 2 Data
C.push(H1("2. Data"));
C.push(P("Seventy-five classification datasets are on disk, each pinned by checksum in its download script. They form three groups, used by different hypotheses."));
C.push(H2("2.1 Earth-observation and development sets"));
C.push(P("**EOData** is the primary dataset, the benchmark FASTENER was built for (Šircelj, Kenda & Koprivec, PANGAEA 2020). It holds 480,000 Sentinel-2 land patches from Slovenia in 2017, in 24 balanced land-cover classes, with 182 features. Ten spectral signals (raw bands and vegetation indices) are each summarised by 18 temporal statistics over the season, and DEM height and inclination are added. **Crop mapping** (UCI 525) is a second EO set: 325,834 cropland pixels from Manitoba in 2012, 7 classes, 174 optical (RapidEye) and polarimetric radar (UAVSAR) features. **Madelon** (synthetic, 5 informative of 500) and **gina** (digit pixels, 970 features) are controls."));
C.push(P("Both EO sets are split at random (stratified), not spatially. The public tables carry no parcel identifier, so neighbouring pixels of one field can sit on both sides of the split. Absolute EO scores are therefore optimistic, as in the original paper. Comparisons between methods are not affected, since every method sees the same split."));
C.push(H2("2.2 Paper benchmarks and other tall sets"));
C.push(P("The **25 benchmarks of the 2020 paper's Table 3** (scikit-feature and similar: gene expression such as TOX_171 and Prostate_GE, text such as BASEHOCK, images such as USPS, COIL20 and ORL) are mostly wide and short. Seven **tall** sets (covertype, miniboone, higgs, gas_drift, volkert, satimage and har) fill the gap toward EOData's shape. Together with the four development sets these make the 36 datasets of H0, H1 and H4."));
C.push(H2("2.3 Time-series classification sets in seven clusters"));
C.push(P("For H2, H3, H5 and H6 we wanted the widest possible range of dataset shapes. All 190 datasets of the UCR/UEA time-series classification archive were clustered by k-means (k = 7) on log10(examples) and log10(features), the features being series length × channels. We then took 39 datasets: seven from each of C1, C3, C4 and C5, five from C2, and three from each of C6 and C7. The picks favour sets used in feature- or channel-selection studies. DuckDuckGeese (363,150 features) was later dropped as too expensive. With EOData this gives the **39 datasets** of the H2–H6 grids. Table 1 summarises the clusters."));
C.push(...table(["cluster", "description", "archive n, median", "archive p, median", "used"],
  [["C1", "small lab sets, p ≥ n: food spectra, outlines, gestures (Coffee, OliveOil, Ham, BeetleFly, Earthquakes, BasicMotions, Epilepsy)", "200", "385", "7"],
    ["C2", "high-dimensional recordings, p ≫ n: EEG, traffic, audio (MotorImagery, PEMS-SF, Heartbeat, EigenWorms)", "378", "40,800", "4"],
    ["C3", "long physiological and device signals (SelfRegulationSCP1, FingerMovements, NATOPS, EthanolConcentration, Computers, CinCECGTorso, HandOutlines)", "724", "1,882", "7"],
    ["C4", "short series, mid-sized, n ≫ p (Adiac, Strawberry, MedicalImages, ProximalPhalanxOutlineCorrect, TwoLeadECG, ItalyPowerDemand, Libras)", "780", "87", "7"],
    ["C5", "larger sensor, motion and shape collections (FordA, Wafer, ECG5000, ChlorineConcentration, StarLightCurves, UWaveGestureLibraryAll, LSST)", "4,036", "500", "7"],
    ["C6", "large audio and industrial sensor sets (FaceDetection, PhonemeSpectra, FaultDetectionA)", "13,640", "4,700", "3"],
    ["C7", "very many, very short series: EO, digits, power (Crop, ElectricDevices, PenDigits)", "24,000", "178", "3"],
    ["EO", "EOData, Sentinel-2 land cover", "480,000 (50,000 used)", "182", "1"]],
  [700, 5260, 1200, 1200, 1000],
  "The dataset clusters of the H2–H6 grids. n and p are archive-wide medians per cluster; 'used' counts the datasets in the grid. The full membership is in experiments/DATASETS_USED.md.",
  { numeric: [2, 3, 4] }));
C.push(P("Two properties of these data shape everything that follows. First, the smallest sets have test splits of only 8–12 rows, so one row moves F1 by 0.06–0.13. Second, the UCR/UEA features are anonymous time points, so no method can use what a feature means. This matters for the LLM ideas in Section 10."));

// 3 Methods
C.push(H1("3. Methods and protocol"));
C.push(H2("3.1 The selectors"));
C.push(P("The full field (H5, H6) has 17 selectors and one reference (Table 2). All of them are implemented or ported in the repository and run through one harness (`run_sota.py`, `run_fastener.py`)."));
C.push(...table(["family", "method", "what it does"],
  [["FASTENER", "stock", "Genetic search over subsets; mating by intersection plus genes sampled by mutual information; pruning by permutation importance; one front entry per size."],
    ["", "guided swap", "Adds a size-preserving swap to pruning: drop the permutation-weakest feature, insert one sampled by mutual information."],
    ["", "random swap", "The same swap with both ends random: the ablation for the guidance."],
    ["NSGA-II", "OBL start", "Multi-objective GA (Deb et al. 2002) with opposition-based initialisation, about p/2 features per individual."],
    ["", "sparse start", "Same search started from random subsets of 1–30 features (a departure from the source, added for H1)."],
    ["", "NSGAII-MIIP", "NSGA-II with mutual-information-based initialisation and operators (port of Li et al.'s MATLAB code)."],
    ["other search", "POSS", "Pareto optimisation for subset selection (Qian, Yu & Zhou 2015)."],
    ["", "FS-SDS", "Stochastic diffusion search, run per k = 1..20 (Alhakbani & al-Rifaie 2017)."],
    ["wrapper / ranker", "Boruta", "All-relevant selection with shadow features (Kursa & Rudnicki 2010), on the protocol model's importances."],
    ["", "RFE", "Recursive feature elimination with the protocol model."],
    ["", "tree importance", "Ranking by the protocol model's impurity importance."],
    ["filter", "mRMR, HSIC Lasso, ReliefF", "Redundancy-aware and kernel filters (Peng et al. 2005; Yamada et al. 2014; Kononenko 1994)."],
    ["", "MI, ANOVA-F rankers", "Univariate rankings (scikit-learn SelectKBest)."],
    ["baseline", "random subsets", "Random subsets at every size, the floor."],
    ["reference", "all features", "No selection; has no subset of size ≤ 10, so it takes no part in the tests."]],
  [1500, 1900, 5960], "The selectors in the full grid."));
C.push(H2("3.2 Protocol"));
C.push(P("Every experiment followed one protocol table (`HYPOTHESES.md`, *Protocol*):"));
C.push(B("**Split.** 60/20/20 stratified train/validation/test, drawn once with `SPLIT_SEED` 20200. Datasets with more than 50,000 rows use a fixed stratified 50,000-row subsample."));
C.push(B("**Classifier.** One classifier drives every search and scores every subset. This was a decision tree in H0–H5H6-E01, the paper's ELM on both sides in H4-E02, a 100-tree random forest in H5H6-E02 and LightGBM in H5H6-E03. Scores are weighted F1."));
C.push(B("**Budget.** A fixed number of unique model fits per run: 6,000, or 12,000 on long-budget datasets; for H2–H6, per-dataset budgets of 2,000–12,000 from a calibration run on a seed outside the experiment. H4-E01 and H4-E02 used equal CPU time instead. Five seeds (2020–2024) per stochastic method."));
C.push(B("**Selection and score.** For each k = 1..K, the best subset of at most k features is chosen on validation and its test F1 is read once. **AUF (K)** is the mean over k. A size a run never reached counts as zero, so AUF rewards both reaching small subsets and quality at those sizes."));
C.push(B("**Tests.** Datasets are the unit. The per-dataset effect is averaged over seeds, and significance comes from a two-sided Wilcoxon signed-rank test (Demšar 2006), with Holm correction over the 16 pairwise comparisons in H5 and H6."));
C.push(B("**Provenance.** Every run records its code commits, configuration hash, seed, timings and fit count. A run counts as evidence only from a clean, committed tree (since DEC-43, a commit verified at submission on the cluster)."));
C.push(H2("3.3 Computing"));
C.push(P("H0 to H5H6-E01 ran on a workstation, single-threaded per run (DEC-37), several runs in parallel. H5H6-E02 and H5H6-E03 ran on **HPC Vega** (IZUM, allocation S26T11-01) as SLURM job arrays: one job per run, 8 cores, 8–128 GB, and a 6-hour cap per run. The workflow is to write and commit code on the workstation, push, pull on Vega, submit there, and fetch the result folders back over ssh."));

// 4 FASTENER updates
C.push(H1("4. Updates to FASTENER"));
C.push(P("The FASTENER code used here is a clone of the published repository, moved off the 2020 pinned software stack and given unit tests. Table 3 lists every change that affects behaviour or cost. Each change is behind a flag or verified to leave the search unchanged, so the published algorithm can still be run exactly."));
C.push(...table(["change", "commit", "what and why", "effect on results"],
  [["Mating bug fixes", "564eb8a", "(1) Weighted-MI mating always added the top-k genes, so children got up to 2k genes back and the weighted sample rarely added anything; (2) an item could be mated with itself (about 13% of pairs); (3) pool_size=None crashed.", "Fixes 1+2 together: faster convergence on 31 sets, narrowly (H0-E02). Fix 2 alone: none (H0-E03)."],
    ["Top genes kept by default", "08e6acd", "Fix 1 reverted to the 2020 behaviour by default (include_top_genes=True). Only the self-mating fix is left; this is stock FASTENER in H2–H6.", "H0-E03 shows that the speed-up came from dropping the top genes, not from fix 2."],
    ["Swap operator (opt-in)", "71281c0", "SwapStrategy in the pruning step: InformationGainSwapStrategy (guided) and RandomSwapStrategy (ablation). It is the first size-preserving move in FASTENER.", "H2 null; H3 narrowly positive, on small data."],
    ["Fit-capped stopping (opt-in)", "71281c0", "Config.max_model_fits stops a run exactly at the budget of unique fits (cache hits are free).", "Makes equal-budget comparisons exact."],
    ["Pruning counters", "b7e724d", "Counts deletions and swaps proposed, fitted and kept.", "Diagnostics: about 1 swap in 100 wins its slot."],
    ["Vectorised bookkeeping", "3877a1a", "Gene bookkeeping in NumPy; identical fronts.", "Lower CPU per fit (used in H4-E03)."],
    ["Fast mutual information", "3be5697", "MI computed by sorting each feature; the same values, 5–11× faster.", "Lower start-up cost on wide sets."],
    ["Bounded model store (harness)", "DEC-42", "The harness kept every fitted model; random-forest models grew runs to 3.4 GB and filled the cluster quota. Only front models are now kept.", "Memory flat; no result changes."]],
  [1700, 900, 4160, 2600], "Changes to FASTENER since the 2020 version (fastener clone, now at 3be5697)."));
C.push(P("Two harness changes concern the competitors. NSGA-II and NSGAII-MIIP now **stop on stagnation**, after a set number of generations that produce no new subset (DEC-41). FS-SDS already had such a stop. Under the tree, NSGA-II runs that had converged spun for up to a million generations of cached offspring until the 6-hour cap. The second change is provenance: the cluster's compute nodes have no git, so jobs read their commit from `.git` and compare it with the commit verified clean at submission (DEC-43)."));

// 5 Hypotheses
C.push(H1("5. Hypotheses"));
C.push(P("The hypotheses were ordered so that each one shakes out the harness for the next. H0 measures the bug fixes before anything uses the fixed code. H1 is cheap and repairs a baseline. H2 is the control for H3, H4 revisits the published comparison, and H5 and H6 run the full grid. Table 4 states each claim, its criterion and its verdict."));
C.push(...table(["", "claim", "criterion (registered)", "verdict"],
  [["H0", "The bug-fixed FASTENER converges faster than the 2020 code.", "Fits to a common validation target; datasets as the unit, Wilcoxon p < 0.05.", "Not confirmed (H0-E03, 36 datasets; p = 0.52)"],
    ["H1", "NSGA-II's weakness at small k is an initialisation artifact.", "Sparse start beats OBL start on AUF (K = 10) in ≥ 4 of 5 seeds on EOData and ≥ 1 other dataset.", "Confirmed (H1-E02; 5 of 5 seeds on EOData and every dataset with p ≥ 182)"],
    ["H2", "Any size-preserving swap improves FASTENER at low k.", "Random swap − stock: more positive datasets and Wilcoxon p < 0.05 over 39.", "Not confirmed (19 vs 20, p = 0.83)"],
    ["H3", "The guided swap improves FASTENER at low k.", "As H2, guided swap − stock.", "Confirmed, narrowly (25 vs 14, p = 0.040; median +0.003)"],
    ["H4", "The published FASTENER > FS-SDS ordering does not survive a clean protocol.", "FS-SDS ahead on more of the 25 benchmarks and Wilcoxon p < 0.05 in its favour (AUF, K = 20).", "Not confirmed: comparable at equal CPU (E01, E02); refuted, FASTENER ahead, at equal fits (E03)"],
    ["H5", "Stock FASTENER is the best selector at low k.", "More wins than losses and Holm-significant against every one of 16 opponents.", "Not confirmed (significant against tree: 5, forest: 9, LightGBM: 12 of 16)"],
    ["H6", "Guided FASTENER is the best selector at low k.", "As H5, focal arm guided FASTENER.", "Not confirmed (significant against tree: 7, forest: 12, LightGBM: 12 of 16)"]],
  [500, 2700, 3260, 2900], "The hypotheses, their criteria and their verdicts."));

// 6 Results
C.push(H1("6. Results, hypothesis by hypothesis"));

C.push(H2("6.1 H0: do the bug fixes change convergence?"));
C.push(P("**Setup.** Stock FASTENER against the 2020 code (both flags restored), 5 seeds, on all 36 datasets. The measure is the number of unique fits each arm needs to reach the lower of the two arms' final validation AUF (K = 10). The per-dataset effect is log2(2020 fits / fixed fits)."));
C.push(P("**Verdict: not confirmed.** In H0-E03, which tests the current code (self-mating removed, top genes kept), the fixed code was faster on 14 datasets and slower on 22, Wilcoxon p = 0.519. The median effect was −0.080: about 6% *more* fits at the median dataset. Seeds split 91 to 89, and the final results are level as well: the best final F1 is higher for the fixed code on 18 datasets and lower on 18."));
C.push(...figure("H0-E03/figures/F3_effect_vs_earlier.png", "H0: each dataset's convergence effect in H0-E03 (self-mating fix only) against its effect in H0-E01/E02 (both fixes). The H0-E02 speed-up does not survive once the top genes are kept.", 4.6));
C.push(P("**Additional findings.** The earlier experiments tested the code with both fixes. H0-E01 (5 datasets) was not supported. H0-E02 (31 datasets) was supported, narrowly. H0-E03 shows that H0-E02's speed-up came from **dropping the always-added top genes**, not from removing self-mating. The 2020 greedy bias toward high-MI genes is therefore not a bug in effect: removing it changes the search, and keeping it is the conservative default. Self-mating wastes crossover slots but no fits, so under a fit budget it costs almost nothing."));

C.push(H2("6.2 H1: is NSGA-II's weakness at small k an initialisation artifact?"));
C.push(P("**Setup.** NSGA-II with its opposition-based (OBL) start against a sparse start (1–30 features). Eight datasets spread p over three orders of magnitude (satimage 36, EOData 182, USPS 256, har 561, COIL20 1,024, gisette 5,000, Prostate_GE 5,966, arcene 10,000), with 5 seeds and equal fits."));
C.push(P("**Verdict: confirmed.** The sparse start scored higher in 5 of 5 seeds on EOData and on all six other datasets with 182 features or more. With the OBL start, NSGA-II never found a subset of 10 or fewer features on those datasets (34 of 35 runs), so it scored zero. On EOData the sparse start reached AUF 0.50 against at most 0.05. Only on satimage (36 features), where both starts are already small, was the OBL start slightly ahead."));
C.push(...figure("H1-E02/figures/F1_H1_criterion_auf10.png", "H1: test AUF (K = 10) of the OBL and sparse starts, one point per seed, lines joining runs with the same seed; datasets ordered by feature count."));
C.push(P("**Additional findings.** (i) Where both starts reach the same sizes, the OBL start is not worse, so the search operators are fine. (ii) Neither start's front moves far from where it began (Figure 3). NSGA-II's balanced mutation makes subset size a zero-drift random walk, so the start fixes the range of sizes explored. (iii) Equal fits did not mean equal run time: wall clock differed by up to 90× between the arms, in both directions, because fit cost scales with subset size. The sparse start became a standard arm of H5 and H6."));
C.push(...figure("H1-E02/figures/F3_front_size_range.png", "H1: smallest to largest subset on each final front, against the dataset's feature count (both log). The OBL start stays near p/2; the sparse start stays near its 1–30 features.", 5.0));

C.push(H2("6.3 H2 and H3: does a size-preserving swap help FASTENER?"));
C.push(P("**Setup.** None of FASTENER's operators keeps a subset's size while changing its content. A swap does. Both arms add one swap candidate per pruned subset, paid for from the same fit budget, on the 39-dataset grid with 5 seeds and calibrated budgets."));
C.push(P("**Verdicts.** **H2 not confirmed:** the random swap was ahead on 19 datasets and behind on 20, p = 0.83, median effect zero. **H3 confirmed, narrowly:** the guided swap was ahead on 25 and behind on 14, p = 0.040, median gain +0.003 AUF. Guided against random was 23 to 16, p = 0.28, so the registered reading does not credit the *guidance* itself."));
C.push(...figure("H2H3-E01/figures/F2_H3_effect_per_dataset.png", "H3: guided swap minus stock FASTENER, test AUF (K = 10), per dataset (clusters C1–C7, then EOData); one point per seed, bar at the mean."));
C.push(P("**Additional findings.** The gain shrinks with dataset size. On the 19 datasets with at least 1,000 rows the record is 10 to 9. Removing the three largest gains, all on sets with 8–16 test rows, takes p to 0.16. By cluster, the guided swap leads only in C1 and C2, the two clusters with the fewest rows. At the operator level the guidance is real: guided swaps win their size slot more often than random ones and leave more entries on the final front. But only about one swap in a hundred wins its slot, and the swap costs about a tenth of each run's fits. EOData leans the guided way (4 of 5 seeds, +0.005), but it is a single dataset."));
C.push(...figure("H2H3-E01/figures/F3_effect_vs_size.png", "H2/H3: per-dataset effect against the number of rows (log). The guided swap's advantage is concentrated in the smallest datasets."));

C.push(H2("6.4 H4: does the published FASTENER > FS-SDS ordering survive?"));
C.push(P("**Setup.** The 2020 Table 3 compared a decision-tree FASTENER with an ELM-driven FS-SDS, at about 30,000 evaluations per k for FS-SDS against 11,000–16,000 in total for FASTENER. That is two confounds at once. We reran both methods on the 25 paper benchmarks with the same classifier, and judged them on AUF (K = 20), the aggregate of Table 3, with 5 seeds. Three experiments separate the confounds:"));
C.push(B("**H4-E01, tree, equal CPU time.** FS-SDS ahead on 10, FASTENER on 15, p = 0.51: **comparable**. FS-SDS made about five times FASTENER's fits in the same CPU time. The paper's ordering holds on 14 of 25 datasets."));
C.push(B("**H4-E02, ELM on both sides, equal CPU time.** 10 to 15 again, mean difference −0.024, p = 0.096: **comparable**. The paper's ordering holds on 16 of 25. Which method leads on a dataset is the same with either classifier on 21 of 25, so the classifier was **not** the confound that mattered."));
C.push(B("**H4-E03, tree, equal model fits.** FASTENER ahead on 18, FS-SDS on 7, mean −0.051, p = 0.0034: **refuted**, FASTENER ahead. Held to FASTENER's number of fits, FS-SDS loses 0.043 while FASTENER scores the same."));
C.push(...figure("H4-E03/figures/F5_budget_compare.png", "H4: FS-SDS's AUF (K = 20) at equal CPU time (H4-E01) and at equal model fits (H4-E03), with FASTENER for reference. The budget unit, not the classifier, decides the ordering."));
C.push(P("**Additional findings.** The published direction holds **per evaluation**: FASTENER uses each model fit better. It does not hold **per unit of compute**: FS-SDS is a lighter search that converts CPU time into many cheap fits of small subsets. Which budget is right depends on what is expensive. When fits are expensive (large training sets, slow learners) FASTENER's efficiency per fit counts; when they are cheap, FS-SDS catches up. Both methods score above the values in the paper's table. This is consistent with D1 (deferred): the gap to the published numbers is largely a grading artifact."));

C.push(H2("6.5 H5 and H6: is (guided) FASTENER the best selector?"));
C.push(P("**Setup.** The full grid: 17 selectors, 39 datasets and 5 seeds, with AUF (K = 10) and a 6-hour cap per run. Each focal FASTENER arm had to beat all 16 opponents on wins and be Holm-significant against each. The grid was run three times, with three classifiers: a decision tree (H5H6-E01, about 2,200 runs over 3 days 8 hours on the workstation), a 100-tree random forest (H5H6-E02, 2,202 runs over 23.5 hours on Vega) and LightGBM (H5H6-E03, 2,202 runs over 17 hours on Vega). LightGBM ran at its defaults except that the smallest leaf scales with the training split, min_child_samples = min(20, max(1, n_train/20)): at the default of 20 the smallest training splits (24–34 rows) barely split at all."));
C.push(P("**Verdicts: neither H5 nor H6, under any of the three classifiers.** Table 5 counts the opponents each focal arm was significantly ahead of."));
C.push(...table(["", "decision tree (E01)", "random forest (E02)", "LightGBM (E03)"],
  [["stock FASTENER (H5)", "5 of 16: ANOVA-F, random subsets, ReliefF, NSGA-II, NSGAII-MIIP", "9 of 16: + FS-SDS, RFE, tree importance, Boruta", "12 of 16: every filter and ranker, Boruta, FS-SDS, random subsets, NSGA-II, NSGAII-MIIP"],
    ["guided FASTENER (H6)", "7 of 16: + FS-SDS, MI ranker; ahead of all 16 on wins", "12 of 16: + POSS, mRMR, MI ranker; behind random swap (15-0-24) and sparse NSGA-II (14-0-25) on wins", "the same 12; ahead of stock on wins (22-0-17), behind random swap, sparse NSGA-II and POSS"],
    ["not separated from the focal arm", "sparse NSGA-II, the other FASTENER arms, POSS, Boruta, RFE, tree importance, mRMR, HSIC Lasso", "stock/guided/random FASTENER and sparse NSGA-II (within 0.004 AUF, Holm p ≈ 1), HSIC Lasso", "stock/guided/random FASTENER, sparse NSGA-II and POSS (within 0.006 AUF, Holm p = 1)"]],
  [1800, 2520, 2520, 2520], "H5/H6: Holm-significant pairwise leads of the focal arms, under each classifier."));
C.push(...figure("H5H6-E03/figures/F1_H5_criterion_auf10.png", "H5 under LightGBM: stock FASTENER's AUF (K = 10) minus each opponent's, one point per dataset; filled points mark the 12 Holm-significant pairs."));
C.push(P("**Additional findings.**"));
C.push(B("**The top is flat.** Under all three classifiers the population searches hold the top: stock, guided and random-swap FASTENER and sparse NSGA-II, joined under LightGBM by POSS. Under the tree, guided FASTENER has the highest mean AUF (0.655 against 0.648 for each of the next three). Under the forest the four are within 0.004 of each other (0.690–0.694), under LightGBM the five within 0.006 (0.690–0.695). Guided FASTENER is never separable from stock FASTENER (Holm p 0.28, 1 and 1)."));
C.push(B("**No selector dominates datasets.** 12–14 of the 17 selectors are best on at least one dataset under each classifier. The most any selector wins is 7 datasets under the tree and the forest, and 10 under LightGBM (sparse NSGA-II, EOData among them). On the median dataset the best selector is 0.011–0.014 AUF ahead of the fourth."));
C.push(B("**Reach explains the OBL searches' losses.** The smallest subset on the final front has more than 10 features in 70% of NSGA-II runs and 63% of NSGAII-MIIP runs under the tree (64% and 54% under the forest, 52% and 44% of the finished runs under LightGBM), so their mean AUF is 0.17–0.39. This confirms H1 at full scale. In the short-series clusters C4 and C7 they reach k ≤ 10 and compete: NSGAII-MIIP is best on Libras and MedicalImages under the tree and leads C4 under LightGBM."));
C.push(B("**The classifier moves the middle of the table (D2).** The forest raises AUF over the tree in 78% of cells, by +0.037 on average, and LightGBM scores at the forest's level (higher in 51% of cells, +0.0007). Under the forest the tree-based rankers fall most (Boruta, tree importance, RFE: 1.9–2.8 places in mean rank); under LightGBM the MI ranker and HSIC Lasso drop and FS-SDS, POSS and Boruta rise. The method order is largely kept (Spearman 0.88–0.92 between classifiers) but much less per dataset (median 0.60–0.79). The cluster leader is the same under all three classifiers only on EOData."));
C.push(B("**Timeouts: stalls under the tree, slowness under LightGBM.** Under the tree, 42 of the 47 runs that hit the 6-hour cap were NSGA-II searches stalled on cached offspring (48,670 to 1.1 million generations). Under the forest, with the stagnation stop, no run timed out. Under LightGBM 71 runs did, 63 of them OBL-started NSGA-II searches that were still finding new subsets but had run only 9–95% of the generations their budget needs; 15 cells (NSGA-II, NSGAII-MIIP and RFE on the longest or widest sets, HSIC Lasso on EOData) have no result."));
C.push(...figure("H5H6-E03/figures/F5_model_compare.png", "The grid under the three classifiers: each method's mean AUF (K = 10) over the datasets all three have (left) and its mean rank among the 17 selectors (right), under the decision tree, the random forest and LightGBM."));

// 7 Running time
C.push(H1("7. How long it took"));
C.push(H2("7.1 Experiments"));
C.push(...table(["experiment", "hypothesis", "wall clock", "where"],
  [["H0-E01 / E02 / E03", "H0", "1 h 42 min / 7 h 40 min / 8 h 22 min", "workstation"],
    ["H1-E01 (stopped) / H1-E02", "H1", "13 min / 14 h 47 min", "workstation"],
    ["H2H3-E01", "H2, H3", "20 h 45 min", "workstation"],
    ["H4-E01 / E02 / E03", "H4", "2 h 13 min / 2 h 20 min / 51 min", "workstation"],
    ["H5H6-E01 (tree)", "H5, H6", "3 d 7 h 46 min", "workstation"],
    ["H5H6-E02 (forest)", "H5, H6", "23 h 28 min (967 job-hours × 8 cores)", "HPC Vega"],
    ["H5H6-E03 (LightGBM)", "H5, H6", "16 h 59 min (1,032 job-hours × 8 cores, finished runs)", "HPC Vega"]],
  [2700, 1300, 3560, 1800], "Duration of each experiment, from the first run's start to the last run's end."));
C.push(H2("7.2 Methods"));
C.push(P("Table 7 gives the wall clock per run for every method on the full grid, and Figure 9 sets it against the score. Three groups appear."));
C.push(B("**Filters and rankers take seconds.** The ANOVA-F, MI and tree-importance rankers have a median run of under 10 s. mRMR, HSIC Lasso and ReliefF are fast on most data but take minutes to hours on the widest sets: in C2 and C6, HSIC Lasso's kernels and ReliefF's distances dominate (C6 medians of 50–57 min under the tree). Boruta and RFE follow the classifier's cost; under the tree, RFE's longest run was 2.8 h."));
C.push(B("**FASTENER is the fastest search per fit.** Under the tree, a FASTENER run had a median of 90–97 s and the slowest took 31 min, for about 14 CPU-hours per arm over the whole grid. At the same fit budget, POSS and FS-SDS cost about the same (median 53–82 s). The NSGA-II family is 4–8 times slower: medians of 409–682 s and totals of 62–132 h, plus 282 h lost in the 47 timed-out runs. FASTENER's own overhead per fit (mutual information, permutation scoring, the archive) is real, but small next to model fitting."));
C.push(B("**The classifier sets the scale.** Under the 100-tree forest, all eight searches have medians of 27–35 min per run on 8 cores, about 20× the tree's cost. FASTENER's three arms take about 105 h each over the grid and the other searches 109–143 h. The filters barely change. FASTENER's slowest forest run took 1.7 h, while the slowest sparse NSGA-II run (HandOutlines) took 5.8 h. LightGBM halves the cost of a search run (medians 9–15 min, NSGA-II 22 min). With the fit cheaper, FASTENER's own work weighs more: it is now 30–50% slower per run than POSS and FS-SDS at the same fit budget, while under the forest it was level with them."));
C.push(...timeTable());
C.push(...figure("paper/figures/P1_cost_vs_score.png", "Cost against score. Median wall clock per run (log) against mean AUF (K = 10) over the datasets, per method; left to right the decision tree (single core), the random forest and LightGBM (8 cores, Vega). The OBL-started NSGA-II and NSGAII-MIIP (mean AUF 0.17–0.39) are drawn at the lower edge."));
C.push(P("Two further observations on cost come from the targeted experiments. **Equal fits are not equal time.** In H1-E02, run times at the same fit budget differed by up to 90× between NSGA-II starts, because fit cost scales with subset size. **Equal time is not equal fits.** In H4-E01, FS-SDS made about five times FASTENER's fits in the same CPU time (about four times with the ELM). The budget unit decided H4 (Section 6.4). Every later comparison therefore reports fits and wall clock side by side."));

// 8 Clusters
C.push(H1("8. Potential of the methods by data cluster"));
C.push(P("No per-cluster test was registered, and with 1–7 datasets per cluster none could carry one, so this section is descriptive. Still, the clusters differ consistently enough to give practical guidance. Tables 8–10 give each method's mean AUF per cluster under the three classifiers, and Figure 10 compares the best search with the best filter or ranker in each cluster."));
C.push(...aufTable("H5H6-E01", "decision tree"));
C.push(...aufTable("H5H6-E02", "random forest"));
C.push(...aufTable("H5H6-E03", "LightGBM"));
C.push(...figure("paper/figures/P2_search_vs_filter_by_cluster.png", "Best search method minus best filter/ranker (Boruta, RFE, tree importance, mRMR, HSIC Lasso, ReliefF, MI and ANOVA-F rankers), mean AUF (K = 10) per cluster, under the tree, the forest and LightGBM, among the methods with a result on every dataset of the cluster; labels name the winning method of each bar."));
C.push(P("Reading the tables per cluster:"));
C.push(B("**C1, small lab sets (p ≥ n, 40–461 rows).** Filters win here under the tree and the forest: HSIC Lasso leads (0.718, 0.744), with the MI ranker and ReliefF close, and guided FASTENER is the best search (0.690, 0.730). Under LightGBM it is a tie: random-swap FASTENER 0.734, ReliefF 0.731, HSIC Lasso 0.729, and POSS leads on mean rank. The guided swap's gain over stock FASTENER is largest here under the tree and the forest (+0.034, +0.028) but gone under LightGBM (−0.003), and test splits of 8–12 rows make every margin fragile. **Potential: a cheap kernel filter first; a population search if it is affordable.**"));
C.push(B("**C2, high-dimensional recordings (p ≫ n).** The population searches lead or tie: stock and guided FASTENER tied first under the tree, the random swap first under the forest (0.690, with HSIC Lasso and the MI ranker within 0.003–0.011), POSS first under LightGBM (0.668, 0.020 ahead of the best filter with full coverage). RFE timed out on three of the four C2 sets under LightGBM. The OBL-started NSGA-II arms never reach k ≤ 10, and under the tree sparse NSGA-II stalled. **Potential: the population searches that start small (FASTENER, POSS, sparse NSGA-II) cope with 10^4–10^5 features within budget; they are the natural target for priors that shrink the candidate pool (Section 10).**"));
C.push(B("**C3, long physiological signals.** The searches lead: narrowly under the tree and the forest (random swap, then sparse NSGA-II, 0.674; the best filter within 0.009–0.011), clearly under LightGBM (stock FASTENER 0.687, 0.025 ahead of HSIC Lasso). **Potential: moderate; any population search, FASTENER the cheapest.**"));
C.push(B("**C4, short series, mid-sized (n ≫ p).** Under the tree, everything from the FASTENER arms to mRMR and sparse NSGA-II lies within 0.004 (about 0.72–0.73). Under the forest, stock FASTENER leads clearly (0.791, mean rank 2.6). Under LightGBM NSGAII-MIIP leads (0.776, mean rank 5.3), with the FASTENER swaps within 0.003; this is the cluster where the OBL-started searches reach small subsets. **Potential: a population search with an ensemble learner.**"));
C.push(B("**C5, larger sensor collections (thousands of rows).** Sparse NSGA-II and the FASTENER arms lead (0.764–0.768 under the forest, 0.766–0.771 under LightGBM), and the best filter (mRMR) is 0.021–0.025 behind. **Potential: population searches clearly pay off once there are enough rows to trust validation scores.**"));
C.push(B("**C6, large audio and industrial sets.** Every method scores low (AUF 0.34–0.39), since ten features out of thousands of time points are far from enough for these tasks. Rankers lead by small margins under all three classifiers (RFE under the tree, Boruta under the forest, tree importance and HSIC Lasso under LightGBM). **Potential: low for selection at K = 10. These tasks need larger K or engineered (e.g. frequency or shapelet) features before selection.**"));
C.push(B("**C7, very many short series, and EOData.** These are the cases closest to FASTENER's design: tall, with few features relative to rows. Searches beat the best filter by 0.016–0.034 under all three classifiers. Sparse NSGA-II has the best mean AUF and the FASTENER arms are within 0.01 (EOData: 0.585 against 0.577–0.579 under the forest, 0.566 against 0.559–0.563 under LightGBM). **Potential: high. This is where search-based selection earns its cost and where FASTENER, at 4–8× lower cost than NSGA-II under the tree, is the practical choice.**"));
C.push(P("Across clusters and classifiers the picture is consistent: the advantage of search over filtering **tends to grow with the number of rows**. On the small C1 sets it is negative under the tree and the forest and +0.004 under LightGBM; in C2–C4 it lies between 0 and +0.025; it is largest on C5, C7 and EOData (+0.016 to +0.034). C6 is the exception: its sets are large, but at K = 10 every method fails there, so the comparison says little. This matches H3, whose guided swap helped only on small data, and both point to the same limit: on tiny validation splits a search overfits its selection, whereas a filter's ranking is more stable."));

// 9 Discussion
C.push(H1("9. Discussion"));
C.push(P("**What the experiments establish.** (1) FASTENER's 2020 mating bugs were real but immaterial to convergence (H0), and the conservative default now keeps the 2020 behaviour except for self-mating. (2) Where a population search starts decides which subset sizes it explores. NSGA-II's OBL start makes it useless at small k, and a sparse start fixes this completely (H1, confirmed again at full scale in H5/H6). (3) FASTENER lacks a size-preserving move, but adding one hardly matters: random swaps do nothing, and guided swaps help a little on small data (H2, H3). (4) The published FASTENER > FS-SDS ordering is a statement about efficiency per evaluation, not per unit of compute (H4). (5) Under one protocol no selector is best everywhere. Under three classifiers FASTENER belongs to a flat top of four or five population searches. Under the tree that top is significantly ahead only of the weak filters and the OBL-started searches; under the ensembles it is ahead of most filters (forest) or all of them (LightGBM) (H5, H6)."));
C.push(P("**What changes with the classifier.** The verdicts, the flat top and the reach failure of the OBL searches are the same under the tree, the forest and LightGBM. The middle of the table and the cluster leaders are not: the leader of a cluster is the same under all three only on EOData. The two ensembles score at the same level and order the methods a little more alike than either does the tree. The step from a single tree to an ensemble therefore matters more than the choice between the two, and a practitioner should choose a method per cluster only together with the learner."));
C.push(P("**Limits.** Every score is one classifier's weighted F1 on one split per dataset. The smallest test splits hold 8–12 rows, and AUF stops at K = 10. Budgets are 2,000–12,000 fits, with five seeds per search and one run per deterministic filter. Datasets are the unit of every test, so 39 datasets give the H5/H6 tests reasonable power, but the per-cluster readings rest on 1–7 datasets each. The EO splits are random, not spatial. The forest runs' commits were reconstructed from the clone's history, since provenance only became fail-closed in H5H6-E03."));

// 10 Outlook
C.push(H1("10. Outlook"));
C.push(H2("10.1 Completing the current line"));
C.push(N("**The 15 empty LightGBM cells.** H5H6-E03 reports them as timed out, as registered. If NSGA-II's, NSGAII-MIIP's and RFE's results under LightGBM are wanted, a separately registered follow-up with a longer cap (12–24 h) for those cells only."));
C.push(N("**Replace H6 with a claim the data can carry.** Either a group claim (\"population searches as a group beat the filters\"), which the three grids point to, or a **non-inferiority test** for guided FASTENER against the best opponent with a pre-set margin (e.g. 0.005 AUF), datasets as the unit."));
C.push(N("**A registered per-cluster test.** The cluster dependence is the most practically useful finding and the least established. It needs more datasets in C2, C6 and C7 (at least 7–10 each, available in the archive) and a test per cluster under the protocol learner."));
C.push(N("**Beyond K = 10 and beyond one split.** AUF at K = 20 and K = 50 (C6 shows that ten features are too few for some tasks), and repeated or cross-validated splits for the smallest sets, so that one test row no longer moves a verdict."));
C.push(N("**A spatial split for EO.** EOData's public table has no parcel identifier; a version with field IDs or coordinates (or a new EO set built with eo-learn) would allow a blocked split and honest absolute EO scores."));
C.push(N("**The protocol learner.** Whether to adopt an ensemble for later hypotheses: the forest and LightGBM score at the same level, well above the tree; LightGBM costs about half the forest per run, but its OBL-started searches need more than 6 hours on the long-series sets. This is the PI's choice."));

C.push(H2("10.2 Regression problems"));
C.push(P("Many EO use cases are regression rather than classification: crop yield, biomass, soil moisture and soil organic carbon, leaf area index, air quality. FASTENER and the whole harness currently assume classification: the mutual information is computed with the class, the splits are stratified and the score is F1. A regression round would ask whether the picture of Sections 6–8 carries over. It needs:"));
C.push(B("**Protocol.** Regressors in `protocol.make_model` (decision tree, random forest and LightGBM regressors). The score is R² on test, clipped at 0 so that AUF stays in [0, 1]; normalised RMSE is reported beside it. Splits are stratified on quantile bins of the target."));
C.push(B("**FASTENER.** Mutual information with a continuous target (k-NN estimator, or the sorting-based fast MI adapted to binned targets) in mating and in the guided swap; permutation importance works unchanged. A flag `task=\"regression\"` in the clone, with unit tests that classification runs stay bit-identical."));
C.push(B("**Competitors.** NSGA-II, POSS and FS-SDS are model-agnostic. The filters have standard regression forms: F-regression for ANOVA-F, RReliefF (Robnik-Šikonja & Kononenko 2003), mRMR with F-statistics or correlation, HSIC Lasso (natively regression), and Boruta and RFE with regressors."));
C.push(B("**Data.** The Monash/UEA **time-series extrinsic regression** archive (Tan et al. 2021) mirrors the UCR/UEA design, so the cluster methodology carries over. It can be complemented by a curated tabular regression suite (e.g. OpenML-CTR23) and by EO regression sets (yield and soil-property data with Sentinel-2 features), ideally with spatial identifiers."));
C.push(B("**Hypothesis (H7, to be registered).** Under the regression protocol, the population searches again form the top group and are significantly ahead of the univariate filters, and the advantage of search over filtering grows with the number of rows. A smoke test on three datasets and a budget calibration come first, as for H2/H3; the grid runs on Vega with the existing `submit.sh` workflow."));

C.push(H2("10.3 Upgrading FASTENER (a): LLM reasoning guiding the selection"));
C.push(P("Every guided step in FASTENER uses one per-feature weight vector, the mutual information with the target. It is used in the initial population, in the weighted mating sample and in the guided swap's choice of insertion. That vector is the natural place to bring in prior knowledge. Large language models can supply knowledge that the data cannot: what a feature measures, which features are physically redundant, and which are plausible for a given target. We see three levels of integration, from cheap to ambitious."));
C.push(H3("Level 1: the LLM as a prior (one call per dataset)"));
C.push(P("Given the data dictionary (feature names, units, sensor, band, temporal statistic), the task description and the class names, the LLM returns a relevance score per feature, groups of features it considers redundant, and a short rationale. FASTENER then uses **w_i = MI_i^(1−λ) · prior_i^λ** wherever it now uses MI_i, and samples its initial population from the same weights. λ = 0 recovers stock FASTENER. λ is fixed in advance or annealed toward 0 over the run, so that data evidence takes over as fits accumulate. This costs no model fits and one batched LLM call per dataset, cached. Related work shows that LLMs can rank features from names alone with useful accuracy (e.g. LLM-Select, Jeong et al. 2024). Here the LLM ranking becomes a prior inside a search that the data then correct, rather than the final answer."));
C.push(H3("Level 2: the LLM as a search operator (one call per generation)"));
C.push(P("Every G generations, FASTENER summarises its state in text: the current front (subset, size and validation F1 per entry), the permutation importances, features that are frequent or absent on the front, and the swaps that failed. It asks the LLM for M new candidate subsets at sizes where the front is weak, each with a reason. The candidates are parsed into valid index sets, deduplicated against the cache, and scored **from the same fit budget**, so comparisons with the other arms stay fair. This puts LLM-generated variation into an evolutionary loop, as in language-model crossover (Meyerson et al. 2024) and FunSearch (Romera-Paredes et al. 2024), but with a cheap and exact fitness. Tokens and LLM wall clock are recorded beside fits, so that the H4 lesson (the budget unit decides) is applied from the start."));
C.push(H3("Level 3: the LLM as critic and explainer (after the search)"));
C.push(P("The LLM reviews the final front. It flags likely target leakage (features derived from the label or recorded after it), points out implausible selections, and proposes equal-size alternatives that are cheaper to acquire (e.g. one sensor instead of two). It also writes a plain-language explanation for each front entry. This does not change the score. It is the part that end users in EO projects ask for most."));
C.push(H3("Implementation in the clone"));
C.push(B("`fastener/priors.py`: a FeaturePrior interface with MIPrior (current behaviour), LLMPrior, KGPrior (Section 10.4) and their mixtures. The mating strategy and InformationGainSwapStrategy take a prior instead of computing MI themselves."));
C.push(B("`LLMProposalStrategy`, called by EntropyOptimizer between generations, with a cap on proposals per generation and a hard ceiling on fits."));
C.push(B("Provenance: model ID, temperature 0, the prompt hash and the full response stored in the run folder, and responses replayed from the cache on reruns, so that a run stays reproducible like every run in this project."));
C.push(H3("What has to be controlled"));
C.push(B("**Meaningless names.** The UCR/UEA features are anonymous time points, so an LLM prior carries no information there. LLM arms must be tested on datasets with meaningful feature names: EOData (signal × statistic), crop mapping, har, gas_drift, covertype and higgs, plus new EO and regression sets."));
C.push(B("**Memorisation.** An LLM may know published results on public benchmarks. Every LLM arm needs a **name-scrambled control** (same data, feature names replaced by neutral but consistent descriptions or random tokens), and, where possible, data released after the model's training cutoff or held privately."));
C.push(B("**Where the gain should show.** Since the top is flat at the end of a budget (Section 6.5), the realistic gain from a prior is **speed**: fewer fits to reach a target. The right primary metric is H0's fits-to-target, at small budgets (500–2,000 fits) and on expensive learners, where a fit is costly."));

C.push(H2("10.4 Upgrading FASTENER (b): a knowledge graph with LLM reasoning"));
C.push(P("A pure LLM prior is ungrounded: it can be confidently wrong and cannot be audited. A **feature knowledge graph (KG)** makes the prior knowledge explicit, checkable and reusable across datasets, and the LLM then reasons over that graph instead of over its own memory."));
C.push(H3("What the KG holds"));
C.push(B("**Nodes:** features; raw signals (Sentinel-2 bands B02–B12, radar polarisations); derived indices (NDVI, NDWI, ...); temporal statistics and windows; sensors and their acquisition cost; physical quantities (chlorophyll, water content, roughness); target classes (crop types, land-cover classes) and phenological stages."));
C.push(B("**Edges:** derived_from (NDVI → B04, B08), same_signal and same_statistic, correlated_with (computed from the training split, with a threshold), measures (index → quantity), relevant_to (quantity → class, e.g. red-edge → chlorophyll → crop vigour), observed_by (feature → sensor), and selected_in (feature → dataset, with the score of the front entry that used it)."));
C.push(B("**Sources:** the dataset's data dictionary; existing sensor and observation ontologies (W3C SOSA/SSN) and spectral-index catalogues; and relations the LLM extracts from the literature, each with a citation and a human check before it enters the graph."));
C.push(H3("How FASTENER uses it"));
C.push(B("**Structured operators.** A KG-aware swap replaces a weak feature with a KG neighbour (same signal, different statistic) for local refinement, or with a distant node (another sensor or quantity) for diversity. A KG-aware mutation adds or removes whole groups."));
C.push(B("**Redundancy and cost.** A penalty for subsets with many features sharing a derived_from parent, and an optional third objective, acquisition cost (number of distinct sensors or bands), which turns FASTENER's front into size × accuracy × cost. This is directly useful for operational EO."));
C.push(B("**Surrogates.** KG embeddings (e.g. node2vec over the graph) give every feature a descriptor, so that a cheap surrogate model can predict a subset's score and screen candidates before a real fit. This saves fits where they are expensive (forest, LightGBM, large EO sets)."));
C.push(B("**Grounded LLM reasoning (GraphRAG).** The LLM of Section 10.3 gets tool access to the KG (graph queries). Each proposal must cite the KG paths that justify it (e.g. \"replace B11_max with NDWI_mean: same quantity, water content; lower correlation with B08_mean already in the subset\"). Proposals without a supporting path are rejected or down-weighted. This makes the LLM operator auditable and reduces hallucinated relations."));
C.push(B("**Memory across datasets.** Writing every experiment's fronts back into the KG as selected_in edges turns the graph into a record of what worked, where. A new EO dataset with the same bands can warm-start from it. This is meta-learning of feature relevance, transparent by construction."));
C.push(H3("A proposed evaluation"));
C.push(P("All arms are scored under the existing protocol with fits, tokens and wall clock recorded, on datasets with meaningful names (Section 10.3), and pre-registered as before:"));
C.push(B("**H8:** an LLM prior (Level 1) reaches a common validation target in fewer fits than stock FASTENER, and the gain disappears under scrambled names. Fits-to-target as in H0, datasets as the unit."));
C.push(B("**H9:** at an equal fit budget, an LLM proposal operator (Level 2) improves AUF (K = 10) over the guided swap. The guided swap is the right control, since both add informed size-preserving candidates."));
C.push(B("**H10:** KG-grounded LLM reasoning matches the ungrounded LLM on AUF, makes fewer invalid or implausible proposals (rated blind by a domain expert), and reaches lower acquisition cost at equal AUF."));
C.push(P("A cheap first step is H8 on EOData, crop mapping and har alone, with one LLM call per dataset. It needs no change to the search loop beyond the prior hook, and it would tell within days whether prior knowledge is worth the larger investment in Levels 2 and 3 and in the KG."));

// References
C.push(H1("References"));
[
  "Alhakbani, H. A., al-Rifaie, M. M. (2017). Feature selection using stochastic diffusion search. GECCO 2017.",
  "Bagnall, A. et al. (2018). The UEA multivariate time series classification archive. arXiv:1811.00075.",
  "Dau, H. A. et al. (2019). The UCR time series archive. IEEE/CAA Journal of Automatica Sinica 6(6).",
  "Deb, K., Pratap, A., Agarwal, S., Meyarivan, T. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II. IEEE Trans. Evol. Comput. 6(2).",
  "Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. JMLR 7.",
  "Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scand. J. Statist. 6(2).",
  "Jeong, D. P., Lipton, Z. C., Ravikumar, P. (2024). LLM-Select: feature selection with large language models. arXiv:2407.02694.",
  "Ke, G. et al. (2017). LightGBM: a highly efficient gradient boosting decision tree. NeurIPS 2017.",
  "Koprivec, F., Kenda, K., Šircelj, B. (2020). FASTENER feature selection for inference from Earth observation data. Entropy 22(11), 1198.",
  "Kursa, M. B., Rudnicki, W. R. (2010). Feature selection with the Boruta package. J. Stat. Softw. 36(11).",
  "Li, A.-D. et al. NSGAII-MIIP, source code, github.com/andali89/NSGAII-MIIP (MIT licence).",
  "Meyerson, E. et al. (2024). Language model crossover: variation through few-shot prompting. ACM TELO.",
  "Peng, H., Long, F., Ding, C. (2005). Feature selection based on mutual information: criteria of max-dependency, max-relevance, and min-redundancy. IEEE TPAMI 27(8).",
  "Qian, C., Yu, Y., Zhou, Z.-H. (2015). Subset selection by Pareto optimization. NeurIPS 2015.",
  "Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. Machine Learning 53.",
  "Romera-Paredes, B. et al. (2024). Mathematical discoveries from program search with large language models. Nature 625.",
  "Šircelj, B., Kenda, K., Koprivec, F. (2020). EOData: Sentinel-2 land-cover samples, Slovenia 2017. PANGAEA, doi:10.1594/PANGAEA.914271.",
  "Tan, C. W., Bergmeir, C., Petitjean, F., Webb, G. I. (2021). Time series extrinsic regression. Data Mining and Knowledge Discovery 35.",
  "Yamada, M. et al. (2014). High-dimensional feature selection by feature-wise kernelized Lasso. Neural Computation 26(1).",
].forEach((r) => C.push(new Paragraph({ children: runs(r, { size: 18 }), spacing: { after: 60 },
  indent: { left: 360, hanging: 360 } })));

// Appendix
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(H1("Appendix A. Where everything is"));
C.push(B("Hypotheses, protocol and revisions: `experiments/HYPOTHESES.md`; decisions: `experiments/DECISIONS.md`; experiment designs and ledger: `experiments/EXPERIMENTS.md`."));
C.push(B("One report per experiment, with figures and tables: `experiments/reports/<ID>/REPORT.md` (the reading) and `SUPPORT.md` (the record); the index is `experiments/reports/LIST.md`."));
C.push(B("This paper: `experiments/reports/paper/` (the figure script `make_paper_figures.py` and the builder `build_paper.js`); it reads only the committed report tables."));
C.push(B("FASTENER clone: `fastener/`, at commit 3be5697, with CHANGELOG.md; cluster scripts: `hpc/vega/`."));
C.push(P("Superseded and failed experiments, kept for the record: H0-E01 (not confirmed; extended by H0-E02), H0-E02 (confirmed, narrowly; the code changed after it, redone in H0-E03), and H1-E01 (stopped after 13 minutes to restart with monitoring; replaced by H1-E02)."));

// ------------------------------------------------------------------ document
const doc = new Document({
  creator: "Klemen Kenda",
  title: "FASTENER under a clean protocol",
  styles: {
    default: { document: { run: { font: "Calibri", size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Calibri", color: "1F3864" },
        paragraph: { spacing: { before: 360, after: 140 }, outlineLevel: 0, keepNext: true } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 25, bold: true, font: "Calibri", color: "2E5496" },
        paragraph: { spacing: { before: 240, after: 100 }, outlineLevel: 1, keepNext: true } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, italics: true, font: "Calibri", color: "2E5496" },
        paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2, keepNext: true } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 },
      margin: { top: 1300, bottom: 1300, left: 1273, right: 1273 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "777777" })] })] }) },
    children: C,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(REPORTS, "FASTENER_experiments_report.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out, `(${figNo} figures, ${tabNo} tables)`);
});
