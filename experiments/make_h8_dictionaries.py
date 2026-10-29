"""Write H8's data dictionaries: what an LLM is told about each dataset.

One JSON file per dataset in experiments/priors/dictionaries/, read by
`llm_guidance.context_for`: the task, the class names, a short description
of the data and of how its feature names are built, and -- for sets stored
with generic names -- the documented name of every column, in column order.
Where the repository's documentation gives per-feature descriptions (QSAR),
they are included.

Sources, kept in experiments/priors/sources/: UCI's dataset metadata
(uci_<id>.json: ozone 172, gas drift 224, HAR 240, QSAR 254, crop mapping
525) and HAR's features.txt. Column order was checked against the data:
HAR's first training row matches row 0 of the pinned file to 5e-7; ozone's
and QSAR's columns have the documented ranges (wind 0-8 m/s, temperatures,
humidity 0-1, sea-level pressure ~10,160; integer atom counts).

Nothing here names which features matter: a dictionary describes what the
features are, as the dataset's documentation does, not their relevance.

    python experiments/make_h8_dictionaries.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE / "priors" / "sources"
OUT = HERE / "priors" / "dictionaries"
DATA = HERE.parent / "data"

H8_DATASETS = ("eodata", "covertype", "higgs", "har", "crop_mapping", "gas_drift",
               "spambase", "heloc", "mice_protein", "ozone_8hr", "qsar_biodeg",
               "eye_movements", "phishing", "pc4", "diabetes130", "adult")


def uci(i):
    return json.loads((SRC / f"uci_{i}.json").read_text(encoding="utf-8"))["data"]


def ozone_names():
    names = [v["name"] for v in uci(172)["variables"]]
    return [n for n in names if n not in ("Dataset", "Date", "Class")]


def qsar_names_and_descriptions():
    text = uci(254)["additional_info"]["variable_info"]
    rows = re.findall(r"^\s*(\d+)\)\s*([^:]+):\s*(.+?)\s*$", text, re.M)
    rows = [(int(i), n.strip(), d.strip()) for i, n, d in rows if int(i) <= 41]
    assert [i for i, _, _ in rows] == list(range(1, 42)), rows
    return [n for _, n, _ in rows], {n: d for _, n, d in rows}


def crop_names():
    text = uci(525)["additional_info"]["variable_info"]
    found = dict((int(i), n) for i, n in re.findall(r"^\s*f(\d+):(\S+)\s*$", text, re.M))
    assert sorted(found) == list(range(1, 175)), len(found)
    return [found[i] for i in range(1, 175)]


def har_names():
    lines = (SRC / "uci_240_features.txt").read_text(encoding="utf-8").splitlines()
    names = [ln.split(" ", 1)[1].strip() for ln in lines if ln.strip()]
    assert len(names) == 561
    return names


def gas_names():
    feats = ["dR", "dR_norm", "EMAi0.001", "EMAi0.01", "EMAi0.1",
             "EMAd0.001", "EMAd0.01", "EMAd0.1"]
    return [f"{f}_sensor{s}" for s in range(1, 17) for f in feats]


def stored_names(name):
    return [str(x) for x in np.load(DATA / name / f"{name}.npz")["feature_names"]]


def dictionaries():
    qsar, qsar_desc = qsar_names_and_descriptions()
    return {
        "eodata": {
            "task": "Classify the crop type of an agricultural land parcel in Slovenia "
                    "(or that it is not farmland) from Sentinel-2 satellite observations "
                    "over the 2017 growing season.",
            "class_names": ["Not_Farmland", "Beans", "Beets", "Buckwheat", "Fallow_land",
                            "Grass", "Hop", "Legumes_or_grass", "Maize", "Meadows",
                            "Orchards", "Other", "Peas", "Poppy", "Potatoes", "Pumpkins",
                            "Soft_fruits", "Soybean", "Summer_cereals", "Sun_flower",
                            "Vegetables", "Vineyards", "Winter_cereals", "Winter_rape"],
            "dataset_description":
                "Each parcel's time series of four Sentinel-2 bands (BLUE, GREEN, RED, NIR) "
                "and six vegetation indices (NDVI, ARVI, EVI, SAVI, NDWI, SIPI) over the "
                "season, summarised by statistics; plus terrain elevation (DEM) and slope "
                "(INCLINATION). Names are <band or index>_<statistic>: max_val, min_val, "
                "mean_val, sd_val of the series; diff_max, diff_min, diff_diff of its "
                "differences; max_mean_feature, max_mean_len, max_mean_surf of the "
                "interval with the highest mean; pos_* and neg_* (len, rate, surf, tran) of "
                "its rising and falling segments: length, rate, area and transitions.",
        },
        "covertype": {
            "task": "Predict the forest cover type of a 30 m x 30 m cell in the Roosevelt "
                    "National Forest, Colorado, from cartographic variables.",
            "class_names": ["Spruce/Fir", "Lodgepole Pine", "Ponderosa Pine",
                            "Cottonwood/Willow", "Aspen", "Douglas-fir", "Krummholz"],
            "dataset_description":
                "Elevation (m), aspect (degrees azimuth), slope (degrees), horizontal and "
                "vertical distances to surface water, horizontal distances to roads and to "
                "wildfire ignition points, hillshade indices at 9am, noon and 3pm, four "
                "binary wilderness-area indicators (1 Rawah, 2 Neota, 3 Comanche Peak, "
                "4 Cache la Poudre) and 40 binary soil-type indicators (USFS ecological "
                "landtype units).",
        },
        "higgs": {
            "task": "Distinguish simulated proton-proton collision events in which a Higgs "
                    "boson is produced (signal) from background events.",
            "class_names": ["background", "signal"],
            "dataset_description":
                "21 low-level detector features: transverse momentum (pT), pseudorapidity "
                "(eta) and azimuth (phi) of one lepton and four jets, each jet's b-tag, and "
                "the missing transverse energy's magnitude and azimuth; and 7 high-level "
                "invariant masses physicists derive from them (m_jj, m_jjj, m_lv, m_jlv, "
                "m_bb, m_wbb, m_wwbb).",
        },
        "har": {
            "task": "Recognise the activity a person performs from the accelerometer and "
                    "gyroscope of a smartphone worn on the waist, from a 2.56 s window.",
            "class_names": ["WALKING", "WALKING_UPSTAIRS", "WALKING_DOWNSTAIRS",
                            "SITTING", "STANDING", "LAYING"],
            "feature_names": har_names(),
            "dataset_description":
                "Prefix t = time domain, f = frequency domain (FFT). BodyAcc and GravityAcc "
                "are the body and gravity parts of acceleration, BodyGyro angular velocity; "
                "Jerk = time derivative, Mag = Euclidean magnitude; -X/-Y/-Z the axis. "
                "Statistics: mean, std, mad, max, min, sma (signal magnitude area), energy, "
                "iqr, entropy, arCoeff (autoregression coefficients), correlation, "
                "maxInds, meanFreq, skewness, kurtosis, bandsEnergy (energy in FFT bins), "
                "and angle() between vectors.",
        },
        "crop_mapping": {
            "task": "Classify the crop type of a field near Winnipeg, Manitoba from fused "
                    "radar and optical satellite observations on 5 and 14 July 2012.",
            "class_names": ["Corn", "Peas", "Canola", "Soybeans", "Oats", "Wheat", "Broadleaf"],
            "feature_names": crop_names(),
            "dataset_description":
                "49 polarimetric radar features (UAVSAR) per date: backscatter coefficients "
                "(sig) in linear HH/HV/VV and circular RR/RL/LL polarisations, their ratios "
                "(R) and correlation coefficients (Ro), coherency eigenvalues (l1-l3), "
                "entropy H, anisotropy A, alpha angle and their combinations, the radar "
                "vegetation index (rvi), and Pauli, Krogager, Freeman and Yamaguchi "
                "decompositions; and 38 optical features (RapidEye) per date: bands "
                "B, G, R, Redge, NIR, vegetation indices (NDVI, EVI, SAVI, ...), and GLCM "
                "texture measures of the first two principal components. Suffix _Rad / _Opt "
                "and the date say which sensor and date.",
        },
        "gas_drift": {
            "task": "Identify which of six gases an array of 16 metal-oxide chemical sensors "
                    "is exposed to, from the sensors' responses (measured over three years).",
            "class_names": ["Ethanol", "Ethylene", "Ammonia", "Acetaldehyde", "Acetone",
                            "Toluene"],
            "feature_names": gas_names(),
            "dataset_description":
                "Eight features for each of 16 sensors (four each of the types TGS2600, "
                "TGS2602, TGS2610 and TGS2620): dR, the steady-state resistance change "
                "from baseline, and dR_norm, its ratio to the baseline; EMAi and EMAd, the "
                "extreme of an exponential moving average of the rising (i) and decaying "
                "(d) part of the response, with smoothing alpha 0.001, 0.01 and 0.1.",
        },
        "spambase": {
            "task": "Decide whether an e-mail is unsolicited commercial e-mail (spam).",
            "class_names": ["not spam", "spam"],
            "dataset_description":
                "E-mails collected at Hewlett-Packard Labs. word_freq_WORD is the "
                "percentage of words in the e-mail that are WORD; char_freq_CHAR the "
                "percentage of characters that are CHAR; capital_run_length_average, "
                "_longest and _total describe runs of consecutive capital letters.",
        },
        "heloc": {
            "task": "Predict the repayment risk of a home-equity line of credit applicant "
                    "(FICO's HELOC data: risk performance Good or Bad, encoded 0/1).",
            "class_names": ["risk performance class 0", "risk performance class 1"],
            "dataset_description":
                "Credit-bureau variables of the applicant. M = months, Num = number of, "
                "Percent = percentage of trades (credit accounts); Delq = delinquency, "
                "Derog = derogatory, Inq = credit inquiries, Revolving/Install = revolving "
                "and instalment trades, Burden = balance relative to credit limit; "
                "ExternalRiskEstimate is a consolidated external risk score.",
        },
        "mice_protein": {
            "task": "Classify mice by genotype (control c or trisomic t, the Ts65Dn model of "
                    "Down syndrome), learning protocol (context-shock CS or shock-context SC) "
                    "and treatment (memantine m or saline s) from protein expression in the "
                    "cerebral cortex.",
            "class_names": ["c-CS-m", "c-CS-s", "c-SC-m", "c-SC-s", "t-CS-m", "t-CS-s",
                            "t-SC-m", "t-SC-s"],
            "dataset_description":
                "Expression levels of 77 proteins and protein modifications measured by "
                "reverse phase protein arrays in the nuclear fraction of cortex samples. "
                "Names are protein symbols with suffix _N; a leading p means a "
                "phosphorylated form (e.g. pERK_N).",
        },
        "ozone_8hr": {
            "task": "Predict whether a day is an 8-hour peak ozone day in the Houston, "
                    "Galveston and Brazoria area of Texas (1998-2004).",
            "class_names": ["normal day", "ozone day"],
            "feature_names": ozone_names(),
            "dataset_description":
                "WSR0-WSR23: wind speed at each hour, WSR_PK and WSR_AV its peak and "
                "average; T0-T23, T_PK, T_AV: the same for temperature. At the 850, 700 and "
                "500 hPa pressure levels: temperature (T85, T70, T50), relative humidity "
                "(RH), east-west wind (U), north-south wind (V) and geopotential height "
                "(HT). KI = K-index, TT = T-totals (atmospheric stability), SLP = sea-level "
                "pressure, SLP_ = its change from the day before, Precp = precipitation.",
        },
        "qsar_biodeg": {
            "task": "Predict whether a chemical is ready biodegradable, from molecular "
                    "descriptors of its structure.",
            "class_names": ["not ready biodegradable", "ready biodegradable"],
            "feature_names": qsar,
            "feature_descriptions": qsar_desc,
            "dataset_description": "41 molecular descriptors of 1,055 chemicals (NITE, Japan).",
        },
        "eye_movements": {
            "task": "From a reader's eye movements on a word of a news-article title, tell "
                    "two kinds of titles apart: the titles follow a question, and are "
                    "irrelevant to it, relevant, or its correct answer (two of these three "
                    "classes, as the tabular benchmark keeps them).",
            "class_names": ["class 0", "class 1"],
            "dataset_description":
                "Per-word features of the eye-movement trajectory: fixation durations "
                "(Fix...Dur: previous, first, first-pass, next, total, mean), saccade lengths "
                "(Sacc...Len), fixation positions within the word, regression length and "
                "duration, pupil diameter (maximum, lag) and the share of time spent; "
                "lineNo, assgNo, titleNo and wordNo are the line, assignment, title and "
                "word numbers.",
        },
        "phishing": {
            "task": "Decide whether a website is a phishing site.",
            "class_names": ["phishing", "legitimate"],
            "dataset_description":
                "Rule-based indicators from the page's URL, source code, domain registration "
                "and DNS, and its traffic and ranking, each coded -1 (phishing-like), "
                "0 (suspicious) or 1 (legitimate-like).",
        },
        "pc4": {
            "task": "Predict whether a module of NASA flight software for an earth-orbiting "
                    "satellite has reported defects.",
            "class_names": ["no defects", "defects"],
            "dataset_description":
                "Static code metrics of each module: lines of code (LOC_*), McCabe "
                "complexities (cyclomatic, essential, design) and their densities, graph "
                "counts (nodes, edges, branches, conditions, decisions), and Halstead "
                "metrics (operators, operands, length, volume, difficulty, effort, error "
                "estimate, programming time).",
        },
        "diabetes130": {
            "task": "Predict whether a diabetic patient's hospital stay is followed by "
                    "readmission within 30 days, after more than 30 days, or not at all "
                    "(130 US hospitals, 1999-2008).",
            "class_names": ["readmitted within 30 days", "readmitted after 30 days",
                            "not readmitted"],
            "dataset_description":
                "Demographics (race, gender, age bracket, weight); admission type, "
                "discharge disposition and admission source as numeric codes; payer code; "
                "days in hospital; numbers of lab procedures, other procedures, medications, "
                "outpatient, emergency and inpatient visits in the preceding year, and of "
                "diagnoses; glucose serum and A1C test results; 23 diabetes medications "
                "(No, Steady, Up, Down); whether medication was changed; whether any "
                "diabetes medication was prescribed. 'column=value' columns are one-hot "
                "categories; a two-valued column is 1 for its second value.",
        },
        "adult": {
            "task": "Predict whether a person's annual income exceeds $50,000, from the 1994 "
                    "US census.",
            "class_names": ["income <= 50K", "income > 50K"],
            "dataset_description":
                "Age, work class, fnlwgt (the census sampling weight), education and years "
                "of education, marital status, occupation, relationship in the household, "
                "race, sex, capital gain and loss, hours worked per week. 'column=value' "
                "columns are one-hot categories; sex is 1 for its second value.",
        },
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, d in dictionaries().items():
        assert name in H8_DATASETS
        n = len(stored_names(name)) if name != "eodata" else 182
        if "feature_names" in d and len(d["feature_names"]) != n:
            raise SystemExit(f"{name}: {len(d['feature_names'])} names for {n} columns")
        d = {"dataset": name, **d}
        (OUT / f"{name}.json").write_text(json.dumps(d, indent=1, ensure_ascii=False),
                                          encoding="utf-8")
        print(f"{name:15} {n:4} features"
              + (" (names restored)" if "feature_names" in d else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
