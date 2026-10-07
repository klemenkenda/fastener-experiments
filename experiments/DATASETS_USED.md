# Time series classification datasets

A selection of 39 datasets from the UCR/UEA archive at
[timeseriesclassification.com](https://timeseriesclassification.com), chosen
2026-10-07 to cover the range of dataset shapes (examples × features) that the
archive offers. None is downloaded yet, and no experiment uses them yet; an
experiment that does names them in its own design in
[`EXPERIMENTS.md`](EXPERIMENTS.md).

## How the archive was grouped

The archive lists 190 datasets: 150 univariate and 40 multivariate.

- **Examples (n)** = train + test.
- **Features (p)** = series length × channels, the size of the flattened
  input. Channel counts come from each multivariate dataset's own page on the
  site. For the 16 datasets with series of unequal length, the maximum (padded)
  length is used; those lengths were not taken from the site and should be
  checked before use. None of the 39 selected datasets has unequal lengths.
- **Clustering:** k-means, k = 7, 60 restarts, on log10(n) and log10(p).
  Silhouette scores were flat for every k from 3 to 9 (0.35-0.40), so the
  borders between clusters are soft. k = 7 was chosen because its clusters are
  the easiest to describe. Names come from each cluster's dominant domains and
  its n/p regime; every cluster is mixed.

| cluster | name | datasets | multivariate | n, median (range) | p, median (range) | median p/n |
|---|---|---:|---:|---|---|---:|
| C1 | Small lab datasets: food spectra, shape outlines, gestures | 49 | 6 | 200 (30-461) | 385 (128-2,844) | 2 |
| C2 | High-dimensional recordings: audio, EEG/MEG, traffic (p ≫ n) | 11 | 8 | 378 (27-1,380) | 40,800 (10,000-363,150) | 320 |
| C3 | Long physiological and device signals, mid-sized | 41 | 13 | 724 (135-2,111) | 1,882 (720-8,064) | 2.8 |
| C4 | Short series, mid-sized: bone/shape outlines and classic UCR | 40 | 2 | 780 (200-3,633) | 87 (15-348) | 0.13 |
| C5 | Larger sensor, motion and shape collections | 32 | 6 | 4,036 (1,000-10,299) | 500 (128-1,209) | 0.13 |
| C6 | Large audio and industrial sensor datasets | 10 | 3 | 13,640 (5,425-279,766) | 4,700 (1,500-44,100) | 0.33 |
| C7 | Very many, very short series: earth observation, digits, power, sleep | 7 | 2 | 24,000 (10,992-569,100) | 178 (16-600) | 0.0023 |

The full membership of every cluster, with each dataset's split, length,
channels, classes and domain, is in
[`tsc_dataset_clusters.md`](tsc_dataset_clusters.md), and as one sortable
table in [`tsc_dataset_clusters.csv`](tsc_dataset_clusters.csv).

## How the datasets were chosen

- **Seven per cluster from C1-C5, five from C2** (which has only 11), **three
  from each of C6 and C7**, whose datasets are large enough to make every run
  slow.
- **Datasets from feature-selection work where possible.** For univariate
  data, feature-selection studies on time series classification evaluate on
  the whole UCR archive (Detach-ROCKET does, and reports FordA as its largest
  binary case), so the univariate picks are standard, widely reported UCR
  datasets. The food spectra (Coffee, OliveOil, Ham, Strawberry) are classic
  wavelength-selection benchmarks. The multivariate picks come from the UEA
  benchmark used by the channel-selection papers (Dhariyal et al., ECS/ECP;
  TSelect). The papers' own dataset tables could not be read when the
  selection was made, so membership in each paper's table is not checked.
- **Equal-length series only**, so every dataset has a fixed feature count.
- **One dataset per near-duplicate family**: UWaveGestureLibrary stands for its
  X/Y/Z/All variants, ProximalPhalanxOutlineCorrect for the phalanx family.
- **A spread of shapes and problems inside each cluster**: binary and
  many-class, balanced and imbalanced, univariate and multivariate.

## The selection

Features are written length × channels for multivariate datasets.

### C1 -- Small lab datasets (p ≥ n)

| dataset | n | features | classes | why |
|---|---:|---|---:|---|
| Coffee | 56 | 286 | 2 | spectra; classic wavelength-selection set |
| OliveOil | 60 | 570 | 4 | spectra; p ≈ 10n |
| Ham | 214 | 431 | 2 | spectra; harder |
| BeetleFly | 40 | 512 | 2 | image outline |
| Earthquakes | 461 | 512 | 2 | sensor; imbalanced |
| BasicMotions | 80 | 100×6 | 4 | multivariate, UEA |
| Epilepsy | 275 | 207×3 | 4 | multivariate, UEA |

### C2 -- High-dimensional recordings (p ≫ n)

The hardest regime for feature selection, and the largest downloads per
dataset: DuckDuckGeese, MotorImagery and PEMS-SF run to hundreds of MB each.

| dataset | n | features | classes | why |
|---|---:|---|---:|---|
| MotorImagery | 378 | 3000×64 | 2 | EEG, 64 channels |
| PEMS-SF | 440 | 144×963 | 7 | traffic, 963 sensors |
| DuckDuckGeese | 100 | 270×1345 | 5 | audio; most features in the archive |
| Heartbeat | 409 | 405×61 | 2 | audio/spectral |
| EigenWorms | 259 | 17984×6 | 5 | few channels, very long series |

### C3 -- Long physiological and device signals

| dataset | n | features | classes | why |
|---|---:|---|---:|---|
| SelfRegulationSCP1 | 561 | 896×6 | 2 | EEG, UEA |
| FingerMovements | 416 | 50×28 | 2 | EEG; many channels, hard |
| NATOPS | 360 | 51×24 | 6 | motion, UEA |
| EthanolConcentration | 524 | 1751×3 | 4 | spectra, multivariate |
| Computers | 500 | 720 | 2 | household electricity |
| CinCECGTorso | 1,420 | 1,639 | 4 | ECG |
| HandOutlines | 1,370 | 2,709 | 2 | long image outline |

### C4 -- Short series, mid-sized (n ≫ p)

| dataset | n | features | classes | why |
|---|---:|---|---:|---|
| Adiac | 781 | 176 | 37 | many classes |
| Strawberry | 983 | 235 | 2 | spectra |
| MedicalImages | 1,141 | 99 | 10 | image |
| ProximalPhalanxOutlineCorrect | 891 | 80 | 2 | one from the phalanx family |
| TwoLeadECG | 1,162 | 82 | 2 | ECG |
| ItalyPowerDemand | 1,096 | 24 | 2 | very few features |
| Libras | 360 | 45×2 | 15 | multivariate, UEA |

### C5 -- Larger sensor, motion and shape collections

| dataset | n | features | classes | why |
|---|---:|---|---:|---|
| FordA | 4,921 | 500 | 2 | engine sensor; Detach-ROCKET's largest binary case |
| Wafer | 7,164 | 152 | 2 | industrial sensor; imbalanced |
| ECG5000 | 5,000 | 140 | 5 | ECG |
| ChlorineConcentration | 4,307 | 166 | 3 | simulated |
| StarLightCurves | 9,236 | 1,024 | 3 | longest series in the cluster |
| UWaveGestureLibrary | 4,479 | 315×3 | 8 | multivariate version; stands for X/Y/Z/All |
| LSST | 4,925 | 36×6 | 14 | astronomy; many classes |

### C6 -- Large audio and industrial sensor datasets

The three smallest suitable datasets in the cluster.

| dataset | n | features | classes | why |
|---|---:|---|---:|---|
| FaceDetection | 9,414 | 62×144 | 2 | 144 MEG channels; a standard channel-selection benchmark |
| PhonemeSpectra | 6,668 | 217×11 | 39 | spectral, many classes; smallest in C6 |
| FaultDetectionA | 13,640 | 5,120 | 3 | bearing vibration; long univariate series |

Reserve: RightWhaleCalls (12,896 × 4,000, 2 classes, audio).

### C7 -- Very many, very short series

| dataset | n | features | classes | why |
|---|---:|---|---:|---|
| Crop | 24,000 | 46 | 24 | satellite time series; the counterpart of eodata and crop_mapping |
| ElectricDevices | 16,637 | 96 | 7 | standard UCR; household power |
| PenDigits | 10,992 | 8×2 | 10 | UEA; extreme case with only 16 features |

Reserve: Tiselac (99,687 × 23×10, satellite), the multivariate partner to
Crop, about 4× larger.

### Left out of C6 and C7

| dataset | reason |
|---|---|
| Sleep, MosquitoSound | 569k and 280k examples |
| UrbanSound | 44,100 features per example |
| FaultDetectionB | 81 training examples against 13,559 test |
| InsectWingbeat | unequal-length series |
| FruitFlies, CardiacArrhythmia, InsectSound | large, and add no shape the picks above lack |

## Sources

- Dataset metadata: [timeseriesclassification.com](https://timeseriesclassification.com)
  dataset table (`JSON/datasetTable.json`) and per-dataset description pages,
  fetched 2026-09-30.
- Dhariyal et al., [Fast channel selection for scalable multivariate time series classification](https://link.springer.com/chapter/10.1007/978-3-030-91445-5_3), AALTD 2021;
  [Scalable classifier-agnostic channel selection for MTSC](https://link.springer.com/article/10.1007/s10618-022-00909-1), DMKD 2023;
  code at [mlgig/ChannelSelectionMTSC](https://github.com/mlgig/ChannelSelectionMTSC).
- [TSelect: selecting relevant and non-redundant channels for MTSC](https://link.springer.com/article/10.1007/s10618-025-01132-4), DMKD 2025.
- Uribarri et al., [Detach-ROCKET: sequential feature selection for time series classification](https://arxiv.org/abs/2309.14518).
