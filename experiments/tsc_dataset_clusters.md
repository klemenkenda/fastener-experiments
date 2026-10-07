# timeseriesclassification.com datasets clustered by examples × features

Source: https://timeseriesclassification.com (dataset table + per-dataset pages for channel counts), fetched 2026-09-30. 190 datasets: 150 univariate, 40 multivariate.

- **Examples (n)** = train + test.
- **Features (p)** = series length × channels (the flattened input size). For the 16 unequal-length datasets, the maximum (padded) length is used, marked with †.
- **Clustering:** k-means (k=7, 60 restarts) on log10(n) and log10(p). Silhouette scores were flat for k=3–9 (0.35–0.40), so the edges between clusters are soft; k=7 was chosen because its clusters are the easiest to describe.
- Cluster names come from the dominant domains and the n/p regime; each cluster is mixed.

| Cluster | Name | Datasets | MV | n (median, range) | p (median, range) | median p/n |
|---|---|---|---|---|---|---|
| C1 | Small lab datasets: food spectra, shape outlines, gestures | 49 | 6 | 200 (30–461) | 385 (128–2,844) | 2 |
| C2 | High-dimensional recordings: audio, EEG/MEG, traffic (p >> n) | 11 | 8 | 378 (27–1,380) | 40,800 (10,000–363,150) | 320 |
| C3 | Long physiological & device signals, mid-sized | 41 | 13 | 724 (135–2,111) | 1,882 (720–8,064) | 2.8 |
| C4 | Short series, mid-sized: bone/shape outlines & classic UCR | 40 | 2 | 780 (200–3,633) | 87 (15–348) | 0.13 |
| C5 | Larger sensor, motion & shape collections | 32 | 6 | 4,036 (1,000–10,299) | 500 (128–1,209) | 0.13 |
| C6 | Large audio & industrial sensor datasets | 10 | 3 | 13,640 (5,425–279,766) | 4,700 (1,500–44,100) | 0.33 |
| C7 | Very many, very short series: earth observation, digits, power, sleep | 7 | 2 | 24,000 (10,992–569,100) | 178 (16–600) | 0.0023 |

## C1: Small lab datasets: food spectra, shape outlines, gestures (49)

Tens to a few hundred examples with a few hundred features each, so features often outnumber examples. Mostly food spectrograms (Coffee, Beef, OliveOil, Wine, Meat, Ham), image outlines (BeetleFly, Fish, OSULeaf) and small gesture/HAR sets.

| Dataset | n | p | Length × Ch | Classes | Type |
|---|---|---|---|---|---|
| AtrialFibrillation | 30 | 1,280 | 640 × 2 | 3 | ECG |
| BeetleFly | 40 | 512 | 512 × 1 | 2 | IMAGE |
| BirdChicken | 40 | 512 | 512 × 1 | 2 | IMAGE |
| Coffee | 56 | 286 | 286 × 1 | 2 | SPECTRO |
| Beef | 60 | 470 | 470 × 1 | 5 | SPECTRO |
| OliveOil | 60 | 570 | 570 × 1 | 4 | SPECTRO |
| Rock | 70 | 2,844 | 2844 × 1 | 4 | SPECTRO |
| BasicMotions | 80 | 600 | 100 × 6 | 4 | HAR |
| EyesOpenShut | 98 | 1,792 | 128 × 14 | 2 | EEG |
| PickupGestureWiimoteZ | 100 | 361 | 361† × 1 | 10 | HAR |
| ShakeGestureWiimoteZ | 100 | 385 | 385† × 1 | 10 | HAR |
| Wine | 111 | 234 | 234 × 1 | 2 | SPECTRO |
| FaceFour | 112 | 350 | 350 × 1 | 4 | IMAGE |
| Car | 120 | 577 | 577 × 1 | 4 | SENSOR |
| Meat | 120 | 448 | 448 × 1 | 3 | SPECTRO |
| Lightning2 | 121 | 637 | 637 × 1 | 2 | SENSOR |
| Herring | 128 | 512 | 512 × 1 | 2 | IMAGE |
| Lightning7 | 143 | 319 | 319 × 1 | 7 | SENSOR |
| DodgerLoopDay | 158 | 288 | 288 × 1 | 7 | SENSOR |
| DodgerLoopGame | 158 | 288 | 288 × 1 | 2 | SENSOR |
| DodgerLoopWeekend | 158 | 288 | 288 × 1 | 2 | SENSOR |
| ToeSegmentation2 | 166 | 343 | 343 × 1 | 2 | MOTION |
| BME | 180 | 128 | 128 × 1 | 3 | SIMULATED |
| UMD | 180 | 150 | 150 × 1 | 3 | SIMULATED |
| Colposcopy | 200 | 180 | 180 × 1 | 6 | IMAGE |
| GunPoint | 200 | 150 | 150 × 1 | 2 | HAR |
| ShapeletSim | 200 | 500 | 500 × 1 | 2 | SIMULATED |
| Trace | 200 | 275 | 275 × 1 | 4 | SENSOR |
| Fungi | 204 | 201 | 201 × 1 | 18 | OTHER |
| Plane | 210 | 144 | 144 × 1 | 7 | SENSOR |
| ArrowHead | 211 | 251 | 251 × 1 | 3 | IMAGE |
| Ham | 214 | 431 | 431 × 1 | 2 | SPECTRO |
| Worms | 258 | 900 | 900 × 1 | 5 | MOTION |
| WormsTwoClass | 258 | 900 | 900 × 1 | 2 | MOTION |
| InsectEPGSmallTrain | 266 | 601 | 601 × 1 | 3 | EPG |
| ToeSegmentation1 | 268 | 277 | 277 × 1 | 2 | MOTION |
| Epilepsy | 275 | 621 | 207 × 3 | 4 | HAR |
| ERing | 300 | 260 | 65 × 4 | 6 | HAR |
| RacketSports | 303 | 180 | 30 × 6 | 4 | HAR |
| GesturePebbleZ1 | 304 | 455 | 455† × 1 | 6 | HAR |
| GesturePebbleZ2 | 304 | 455 | 455† × 1 | 6 | HAR |
| InsectEPGRegularTrain | 311 | 601 | 601 × 1 | 3 | EPG |
| DiatomSizeReduction | 322 | 345 | 345 × 1 | 4 | IMAGE |
| GestureMidAirD1 | 338 | 360 | 360 × 1 | 26 | HAR |
| GestureMidAirD2 | 338 | 360 | 360 × 1 | 26 | HAR |
| GestureMidAirD3 | 338 | 360 | 360 × 1 | 26 | HAR |
| Fish | 350 | 463 | 463 × 1 | 7 | IMAGE |
| OSULeaf | 442 | 427 | 427 × 1 | 6 | IMAGE |
| Earthquakes | 461 | 512 | 512 × 1 | 2 | SENSOR |

## C2: High-dimensional recordings: audio, EEG/MEG, traffic (p >> n) (11)

Few examples but 10k–360k features, from long or many-channel recordings (MotorImagery 64 ch × 3000, PEMS-SF 963 sensors, DuckDuckGeese 1345 × 270). The hardest p ≫ n regime.

| Dataset | n | p | Length × Ch | Classes | Type |
|---|---|---|---|---|---|
| StandWalkJump | 27 | 10,000 | 2500 × 4 | 3 | ECG |
| DuckDuckGeese | 100 | 363,150 | 270 × 1345 | 5 | AUDIO |
| DucksAndGeese | 100 | 236,784 | 236784 × 1 | 5 | AUDIO |
| EigenWorms | 259 | 107,904 | 17984 × 6 | 5 | MOTION |
| CatsDogs | 275 | 14,773 | 14773 × 1 | 2 | AUDIO |
| MotorImagery | 378 | 192,000 | 3000 × 64 | 2 | EEG |
| BinaryHeartbeat | 409 | 18,530 | 18530 × 1 | 2 | AUDIO |
| Heartbeat | 409 | 24,705 | 405 × 61 | 2 | AUDIO |
| PEMS-SF | 440 | 138,672 | 144 × 963 | 7 | OTHER |
| CounterMovementJump | 598 | 12,750 | 4250 × 3 | 3 | HAR |
| MindReading | 1,380 | 40,800 | 200 × 204 | 5 | MEG |

## C3: Long physiological & device signals, mid-sized (41)

Hundreds to ~2k examples with long series (~700–8k features): household electricity (Computers, *KitchenAppliances), EEG/EOG/EMG, pig blood pressure, road-surface (Asphalt*) and motion.

| Dataset | n | p | Length × Ch | Classes | Type |
|---|---|---|---|---|---|
| HouseTwenty | 135 | 3,000 | 3000 × 1 | 2 | DEVICE |
| Cricket | 180 | 7,182 | 1197 × 6 | 12 | HAR |
| ACSF1 | 200 | 1,460 | 1460 × 1 | 10 | DEVICE |
| NerveDamage | 204 | 1,500 | 1500 × 1 | 3 | EMG |
| HandMovementDirection | 234 | 4,000 | 400 × 10 | 4 | EEG |
| PigAirwayPressure | 312 | 2,000 | 2000 × 1 | 52 | HEMODYNAMICS |
| PigArtPressure | 312 | 2,000 | 2000 × 1 | 52 | HEMODYNAMICS |
| PigCVP | 312 | 2,000 | 2000 × 1 | 52 | HEMODYNAMICS |
| NATOPS | 360 | 1,224 | 51 × 24 | 6 | HAR |
| MotionSenseHAR | 361 | 2,400 | 200 × 12 | 6 | HAR |
| SelfRegulationSCP2 | 380 | 8,064 | 1152 × 7 | 2 | EEG |
| FingerMovements | 416 | 1,400 | 50 × 28 | 2 | EEG |
| Haptics | 463 | 1,092 | 1092 × 1 | 5 | MOTION |
| Computers | 500 | 720 | 720 × 1 | 2 | DEVICE |
| EthanolConcentration | 524 | 5,253 | 1751 × 3 | 4 | SPECTRO |
| SelfRegulationSCP1 | 561 | 5,376 | 896 × 6 | 2 | EEG |
| ArticularyWordRecognition | 575 | 1,296 | 144 × 9 | 25 | MOTION |
| AbnormalHeartbeat | 606 | 3,053 | 3053 × 1 | 5 | AUDIO |
| InlineSkate | 650 | 1,882 | 1882 × 1 | 7 | MOTION |
| EOGHorizontalSignal | 724 | 1,250 | 1250 × 1 | 12 | EOG |
| EOGVerticalSignal | 724 | 1,250 | 1250 × 1 | 12 | EOG |
| LargeKitchenAppliances | 750 | 720 | 720 × 1 | 3 | DEVICE |
| RefrigerationDevices | 750 | 720 | 720 × 1 | 3 | DEVICE |
| ScreenType | 750 | 720 | 720 × 1 | 3 | DEVICE |
| SmallKitchenAppliances | 750 | 720 | 720 × 1 | 3 | DEVICE |
| AsphaltObstacles | 781 | 736 | 736† × 1 | 4 | MOTION |
| AsphaltObstaclesCoordinates | 781 | 2,208 | 736† × 3 | 4 | MOTION |
| SemgHandGenderCh2 | 900 | 1,500 | 1500 × 1 | 2 | SPECTRO |
| SemgHandMovementCh2 | 900 | 1,500 | 1500 × 1 | 6 | SPECTRO |
| SemgHandSubjectCh2 | 900 | 1,500 | 1500 × 1 | 5 | SPECTRO |
| Blink | 950 | 2,040 | 510 × 4 | 2 | EEG |
| EthanolLevel | 1,004 | 1,751 | 1751 × 1 | 4 | SPECTRO |
| PLAID | 1,074 | 1,344 | 1344† × 1 | 11 | DEVICE |
| EMOPain | 1,143 | 5,400 | 180 × 30 | 3 | HAR |
| KeplerLightCurves | 1,319 | 4,767 | 4767 × 1 | 7 | SENSOR |
| HandOutlines | 1,370 | 2,709 | 2709 × 1 | 2 | IMAGE |
| CinCECGTorso | 1,420 | 1,639 | 1639 × 1 | 4 | ECG |
| AsphaltRegularity | 1,502 | 4,201 | 4201† × 1 | 2 | MOTION |
| AsphaltRegularityCoordinates | 1,502 | 4,201 | 4201† × 1 | 2 | MOTION |
| AsphaltPavementType | 2,111 | 2,371 | 2371† × 1 | 3 | MOTION |
| AsphaltPavementTypeCoordinates | 2,111 | 7,113 | 2371† × 3 | 3 | MOTION |

## C4: Short series, mid-sized: bone/shape outlines & classic UCR (40)

Hundreds to a few thousand examples with short series (15–350 features), so examples outnumber features. Dominated by image outlines (phalanges, leaves, faces), plus simulated sets (CBF, SyntheticControl) and short sensor/ECG series.

| Dataset | n | p | Length × Ch | Classes | Type |
|---|---|---|---|---|---|
| ECG200 | 200 | 96 | 96 × 1 | 2 | ECG |
| SmoothSubspace | 300 | 15 | 15 × 1 | 3 | SIMULATED |
| Libras | 360 | 90 | 45 × 2 | 15 | HAR |
| PowerCons | 360 | 144 | 144 × 1 | 2 | DEVICE |
| Chinatown | 365 | 24 | 24 × 1 | 2 | TRAFFIC |
| GunPointAgeSpan | 451 | 150 | 150 × 1 | 2 | HAR |
| GunPointMaleVersusFemale | 451 | 150 | 150 × 1 | 2 | HAR |
| GunPointOldVersusYoung | 451 | 150 | 150 × 1 | 2 | HAR |
| DistalPhalanxOutlineAgeGroup | 539 | 80 | 80 × 1 | 3 | IMAGE |
| DistalPhalanxTW | 539 | 80 | 80 × 1 | 6 | IMAGE |
| MiddlePhalanxTW | 553 | 80 | 80 × 1 | 6 | IMAGE |
| MiddlePhalanxOutlineAgeGroup | 554 | 80 | 80 × 1 | 3 | IMAGE |
| SyntheticControl | 600 | 60 | 60 × 1 | 6 | SIMULATED |
| ProximalPhalanxOutlineAgeGroup | 605 | 80 | 80 × 1 | 3 | IMAGE |
| ProximalPhalanxTW | 605 | 80 | 80 × 1 | 6 | IMAGE |
| SonyAIBORobotSurface1 | 621 | 70 | 70 × 1 | 2 | SENSOR |
| JapaneseVowels | 640 | 348 | 29 × 12 | 9 | AUDIO |
| CricketX | 780 | 300 | 300 × 1 | 12 | HAR |
| CricketY | 780 | 300 | 300 × 1 | 12 | HAR |
| CricketZ | 780 | 300 | 300 × 1 | 12 | HAR |
| Adiac | 781 | 176 | 176 × 1 | 37 | IMAGE |
| DistalPhalanxOutlineCorrect | 876 | 80 | 80 × 1 | 2 | IMAGE |
| ECGFiveDays | 884 | 136 | 136 × 1 | 2 | ECG |
| MiddlePhalanxOutlineCorrect | 891 | 80 | 80 × 1 | 2 | IMAGE |
| ProximalPhalanxOutlineCorrect | 891 | 80 | 80 × 1 | 2 | IMAGE |
| FiftyWords | 905 | 270 | 270 × 1 | 50 | IMAGE |
| WordSynonyms | 905 | 270 | 270 × 1 | 25 | IMAGE |
| CBF | 930 | 128 | 128 × 1 | 3 | SIMULATED |
| SonyAIBORobotSurface2 | 980 | 65 | 65 × 1 | 2 | SENSOR |
| Strawberry | 983 | 235 | 235 × 1 | 2 | SPECTRO |
| ItalyPowerDemand | 1,096 | 24 | 24 × 1 | 2 | SENSOR |
| SwedishLeaf | 1,125 | 128 | 128 × 1 | 15 | IMAGE |
| MedicalImages | 1,141 | 99 | 99 × 1 | 10 | IMAGE |
| TwoLeadECG | 1,162 | 82 | 82 × 1 | 2 | ECG |
| MoteStrain | 1,272 | 84 | 84 × 1 | 2 | SENSOR |
| SharePriceIncrease | 1,930 | 60 | 60 × 1 | 2 | FINANCIAL |
| FaceAll | 2,250 | 131 | 131 × 1 | 14 | IMAGE |
| FacesUCR | 2,250 | 131 | 131 × 1 | 14 | IMAGE |
| PhalangesOutlinesCorrect | 2,658 | 80 | 80 × 1 | 2 | IMAGE |
| MelbournePedestrian | 3,633 | 24 | 24 × 1 | 10 | TRAFFIC |

## C5: Larger sensor, motion & shape collections (32)

Thousands of examples with a few hundred features: accelerometer gestures (UWave, WalkingSittingStanding), engine and wafer sensors (FordA/B, Wafer), fetal ECG and shape images (MixedShapes, Yoga).

| Dataset | n | p | Length × Ch | Classes | Type |
|---|---|---|---|---|---|
| AllGestureWiimoteX | 1,000 | 500 | 500† × 1 | 10 | HAR |
| AllGestureWiimoteY | 1,000 | 500 | 500† × 1 | 10 | HAR |
| AllGestureWiimoteZ | 1,000 | 500 | 500† × 1 | 10 | HAR |
| Handwriting | 1,000 | 456 | 152 × 3 | 26 | HAR |
| Symbols | 1,020 | 398 | 398 × 1 | 6 | IMAGE |
| ShapesAll | 1,200 | 512 | 512 × 1 | 60 | IMAGE |
| Phoneme | 2,110 | 1,024 | 1024 × 1 | 39 | AUDIO |
| Mallat | 2,400 | 1,024 | 1024 × 1 | 8 | SIMULATED |
| MixedShapesSmallTrain | 2,525 | 1,024 | 1024 × 1 | 5 | IMAGE |
| CharacterTrajectories | 2,858 | 546 | 182† × 3 | 20 | MOTION |
| FreezerSmallTrain | 2,878 | 301 | 301 × 1 | 2 | DEVICE |
| MixedShapesRegularTrain | 2,925 | 1,024 | 1024 × 1 | 5 | IMAGE |
| FreezerRegularTrain | 3,000 | 301 | 301 × 1 | 2 | DEVICE |
| Yoga | 3,300 | 426 | 426 × 1 | 2 | IMAGE |
| NonInvasiveFetalECGThorax1 | 3,765 | 750 | 750 × 1 | 42 | ECG |
| NonInvasiveFetalECGThorax2 | 3,765 | 750 | 750 × 1 | 42 | ECG |
| ChlorineConcentration | 4,307 | 166 | 166 × 1 | 3 | SIMULATED |
| ElectricDeviceDetection | 4,390 | 256 | 256 × 1 | 2 | SENSOR |
| FordB | 4,446 | 500 | 500 × 1 | 2 | SENSOR |
| UWaveGestureLibraryAll | 4,478 | 945 | 945 × 1 | 8 | HAR |
| UWaveGestureLibraryX | 4,478 | 315 | 315 × 1 | 8 | HAR |
| UWaveGestureLibraryY | 4,478 | 315 | 315 × 1 | 8 | HAR |
| UWaveGestureLibraryZ | 4,478 | 315 | 315 × 1 | 8 | HAR |
| UWaveGestureLibrary | 4,479 | 945 | 315 × 3 | 8 | HAR |
| FordA | 4,921 | 500 | 500 × 1 | 2 | SENSOR |
| LSST | 4,925 | 216 | 36 × 6 | 14 | OTHER |
| ECG5000 | 5,000 | 140 | 140 × 1 | 5 | ECG |
| TwoPatterns | 5,000 | 128 | 128 × 1 | 4 | SIMULATED |
| Wafer | 7,164 | 152 | 152 × 1 | 2 | SENSOR |
| SpokenArabicDigits | 8,798 | 1,209 | 93 × 13 | 10 | SPEECH |
| StarLightCurves | 9,236 | 1,024 | 1024 × 1 | 3 | SENSOR |
| WalkingSittingStanding | 10,299 | 618 | 206 × 3 | 6 | HAR |

## C6: Large audio & industrial sensor datasets (10)

Thousands to hundreds of thousands of examples with 1.5k–44k features: insect, whale and urban audio, bearing fault detection and ECG arrhythmia.

| Dataset | n | p | Length × Ch | Classes | Type |
|---|---|---|---|---|---|
| UrbanSound | 5,425 | 44,100 | 44100 × 1 | 10 | AUDIO |
| PhonemeSpectra | 6,668 | 2,387 | 217 × 11 | 39 | AUDIO |
| FaceDetection | 9,414 | 8,928 | 62 × 144 | 2 | EEG |
| RightWhaleCalls | 12,896 | 4,000 | 4000 × 1 | 2 | AUDIO |
| FaultDetectionA | 13,640 | 5,120 | 5120 × 1 | 3 | SENSOR |
| FaultDetectionB | 13,640 | 5,120 | 5120 × 1 | 3 | SENSOR |
| FruitFlies | 34,518 | 5,000 | 5000 × 1 | 3 | AUDIO |
| CardiacArrhythmia | 45,577 | 1,500 | 1500 × 1 | 3 | ECG |
| InsectWingbeat | 50,000 | 4,400 | 22† × 200 | 10 | AUDIO |
| MosquitoSound | 279,766 | 3,750 | 3750 × 1 | 6 | AUDIO |

## C7: Very many, very short series: earth observation, digits, power, sleep (7)

11k–570k examples with only 16–600 features: satellite time series (Crop, Tiselac), PenDigits, ElectricDevices, InsectSound, sleep/seizure EEG.

| Dataset | n | p | Length × Ch | Classes | Type |
|---|---|---|---|---|---|
| PenDigits | 10,992 | 16 | 8 × 2 | 10 | MOTION |
| EpilepticSeizures | 11,500 | 178 | 178 × 1 | 2 | EEG |
| ElectricDevices | 16,637 | 96 | 96 × 1 | 7 | DEVICE |
| Crop | 24,000 | 46 | 46 × 1 | 24 | IMAGE |
| InsectSound | 50,000 | 600 | 600 × 1 | 10 | AUDIO |
| Tiselac | 99,687 | 230 | 23 × 10 | 9 | IMAGE |
| Sleep | 569,100 | 178 | 178 × 1 | 5 | EEG |
