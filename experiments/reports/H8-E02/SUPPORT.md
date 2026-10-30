# H8-E02 -- supporting record

The record behind [REPORT.md](REPORT.md): the runs, the criteria as registered, the parameters, the per-seed numbers and how to reproduce them.

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H8-E02` |
| Hypothesis ID | H8 |
| Run IDs | `20261030T005602Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005725Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005726Z_h8e02_eodata_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005725Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005725Z_h8e02_covertype_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005726Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005726Z_h8e02_phishing_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005726Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005726Z_h8e02_higgs_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_har_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_diabetes130_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_spambase_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_har_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005729Z_h8e02_adult_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005729Z_h8e02_heloc_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005729Z_h8e02_spambase_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005730Z_h8e02_adult_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005730Z_h8e02_phishing_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005729Z_h8e02_gas_drift_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005729Z_h8e02_pc4_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005731Z_h8e02_spambase_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005731Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005731Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005731Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005732Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005732Z_h8e02_spambase_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005734Z_h8e02_spambase_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005734Z_h8e02_phishing_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005735Z_h8e02_spambase_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005812Z_h8e02_pc4_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005813Z_h8e02_pc4_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005814Z_h8e02_pc4_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005828Z_h8e02_pc4_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005829Z_h8e02_mice_protein_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005834Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005855Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2020` (ok)<br>`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2021` (ok)<br>`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005858Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2020` (ok)<br>`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005900Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2021` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2022` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2024` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2021` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2023` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2022` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2023` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2020` (ok)<br>`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2024` (ok)<br>`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2023` (ok)<br>`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2024` (ok)<br>`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2022` (ok)<br>`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2021` (ok) |
| Algorithm IDs | `fastener_llm_haiku_blind@79d5ac2+9226b90#8b24`<br>`fastener_llm_opus_blind@79d5ac2+9226b90#e4af`<br>`fastener_llm_sonnet_blind@79d5ac2+9226b90#6637` |
| Pre-registration | `experiments/HYPOTHESES.md` at `79d5ac2` |
| Code commits | `79d5ac2` |
| Dates | runs 2026-10-30T00:56:02.611862+00:00 to 2026-10-30T02:14:33.390565+00:00; report 2026-10-30 |
| Verdict | H8: **not supported** for the three Anthropic models (part (i) holds for all three, part (ii) for none); see [REPORT.md](REPORT.md) |

**Note:** `experiments/HYPOTHESES.md` has changed since `79d5ac2`. The quotes below are from `79d5ac2`, the version in force when the experiment ran.

## 2. Hypothesis

> ## H8 -- An LLM relevance prior lets FASTENER reach its target in fewer fits
>
> **Claim.** On datasets whose features have meaningful names, FASTENER guided
> by a relevance prior from a large language model reaches a common validation
> target in fewer fits than stock FASTENER, and the gain is lost when the
> feature names are scrambled.

## 3. Evaluation criteria

### H8

> **Arms.** `fastener` (stock); `fastener_llm` (the prior, lambda fixed before the
> runs); `fastener_llm_scrambled` (the same model and prompt, feature names
> replaced by neutral tokens: the control for memorised benchmark knowledge);
> `fastener_seed_mrmr` from H10 (a prior from the data alone, the control an
> LLM prior has to beat).

> **Primary metric.** Fits to a common target, as H0: per dataset and seed, the
> target is the lower of the two arms' final validation AUF (K = 10), and an
> arm's result is the cumulative fits at its first snapshot at or above it.

> **Falsification criterion.** Per dataset, the effect is the mean over seeds of
> log2(stock fits / LLM fits). H8 is **supported** if the effect is positive on
> more datasets than negative and a two-sided Wilcoxon test over the datasets is
> significant at alpha = 0.05, **and** the same holds for `fastener_llm` against
> `fastener_llm_scrambled`. Without the second part a gain is attributed to the
> prior's form, not to the knowledge in the names.
>
> **To fix before any run, in a revision:** the datasets (at least 12 with
> meaningful feature names: EOData, crop mapping, har, covertype and higgs are
> on disk; the rest from OpenML), the budget (500-2,000 fits), lambda, the LLM
> and its prompt, and the classifier. *Fixed on 2026-10-30 (revision below,
> [DEC-49](DECISIONS.md#dec-49)).*

> ## Revisions
>
> **2026-09-25 -- H0 on every other dataset (H0-E02) added.** Added after
> H0-E01 had finished and been reported as not supported, with its datasets split
> (fixed code faster on TOX_171 and USPS, 2020 code on BASEHOCK, neither on crop
> mapping and har). H0's own criterion, datasets and verdict are unchanged. The
> new experiment takes every remaining dataset rather than a chosen subset, and
> its criterion is written here before any of its runs started.
>
> **2026-09-30 -- The fixed arm keeps the top genes.** After H0-E01 and H0-E02
> were reported, `include_top_genes` became `True` in the clone's defaults and in
> the `fastener` arm, so the fixed code now differs from the 2020 code only in
> `allow_self_mating`. H0-E01 and H0-E02 tested the fixed code with both flags
> off; their verdicts are about that code, not this one. Stock FASTENER in H2-H6
> is the new default. Runs of the two arms carry different algorithm IDs through
> both repositories' commits (FASTENER `144621c` before, `08e6acd` after), so
> they are never pooled. Up to H0-E03 the config part of the ID recorded only the
> mating version's name, so the old and new fixed arms share a config hash; from
> 2026-10-07 the config also records both flags.
>
> **2026-09-30 -- Twice the budget where the search had not converged.** Decided
> after H0-E01 and H0-E02 were reported, from their validation curves only (test
> scores played no part). A dataset counts as not converged when the mean
> validation AUF at K = 10 of at least one H0 arm rose by 0.005 or more over the
> last quarter of its budget (4,500 to 6,000 fits). Eleven datasets meet it:
>
> | dataset | rise over the last quarter, fixed / 2020 |
> |---|---|
> | BASEHOCK | 0.025 / 0.014 |
> | nci9 | 0.024 / 0.001 |
> | lung_discrete | 0.013 / 0.015 |
> | PCMAC | 0.006 / 0.013 |
> | warpAR10P | 0.013 / 0.001 |
> | TOX_171 | 0.009 / 0.005 |
> | arcene | 0.006 / 0.008 |
> | ORL | 0.004 / 0.007 |
> | RELATHE | 0.001 / 0.007 |
> | warpPIE10P | 0.003 / 0.005 |
> | CLL_SUB_111 | 0.003 / 0.005 |
>
> These get 12,000 fits per run in H1-H6, for every arm (`protocol.fit_budget`);
> every other dataset keeps 6,000, and the EO sets in H0 keep 1,000. On the
> smallest of the eleven (nci9, lung_discrete, TOX_171) the validation split has
> 12-34 rows, so part of the late rise can be the search fitting validation noise
> rather than finding better subsets; the extra budget gives it room either way,
> and test scores will show which. H0's verdicts are unchanged: its budgets were
> fixed before its runs.
>
> **2026-10-07 -- Experiment designs moved to `EXPERIMENTS.md`.** The H0-E02 and
> H0-E03 subsections of H0 moved, with their text unchanged, to *Experiment
> designs* in [`EXPERIMENTS.md`](EXPERIMENTS.md). H0 now lists its experiments as
> bullets. This file keeps the hypotheses, the protocol and what experiments of
> one hypothesis share; designs of later experiments go to `EXPERIMENTS.md`. No
> claim, criterion or verdict changed.
>
> **2026-10-07 -- The new FASTENER for every later experiment.** Decided by the
> PI after H0-E03 was reported (not supported: without self-mating, the current
> code converges neither faster nor slower than the 2020 code, and ends level).
> Every FASTENER arm in H1-H6 runs the current code, as the *FASTENER version*
> row of the protocol states. This confirms what the 2026-09-30 revision already
> set for stock FASTENER; no criterion changes.
>
> **2026-10-07 -- H1's datasets: eight, spread by feature count.** Decided by
> the PI before any H1 result was read. H1 had been registered on the four
> development sets, whose feature counts span only 174-970. The claim is about
> OBL starting at half the features, so it predicts an effect that grows with p
> and vanishes at small p; the four could not show either end. H1 now runs on
> satimage, EOData, USPS, har, COIL20, gisette, Prostate_GE and arcene (36 to
> 10,000 features), and the criterion's "at least one other development set"
> reads "at least one other of the eight datasets". The 4-of-5-seeds rule, the
> arms, the metric and EOData's place in the criterion are unchanged.
> `make_report.py` reads H1 on these eight (`H1_SETS`).
>
> The change was committed (`3e1ce0c`) without this entry, and `H1-E01` was
> started from that commit. It was stopped after 13 minutes, with only EOData's
> ten runs started and none finished, and is recorded as failed; no score was
> looked at. `H1-E02` restarts it from the commit that adds this entry, one
> process per dataset, arm and seed (`run_queue.py`).
>
> **2026-10-09 -- H2 and H3: forty datasets, datasets as the unit, a
> calibrated budget.** Decided by the PI before any H2 or H3 run; no swap-arm
> result of this round exists. Three changes, to both hypotheses alike:
>
> * **Datasets.** The four development sets span 174-970 features and two
>   domains, too narrow for a claim about an operator FASTENER lacks on any
>   data. H2 and H3 now run on the 39 UCR/UEA time series sets of
>   `DATASETS_USED.md`, chosen by shape cluster, and on EOData: 40 datasets,
>   16 to 363,150 features. Crop mapping, madelon and gina leave H2 and H3; they
>   remain development sets for H5 and H6.
> * **Criterion.** With 40 datasets the per-seed rule on EOData and one other
>   set is no longer the useful test. Each hypothesis is now read with datasets
>   as the unit, as H0-E02 was: the per-dataset effect is the mean over seeds of
>   the swap arm's AUF (K = 10) minus stock's, and the hypothesis is supported if
>   the effects lean positive and a two-sided Wilcoxon signed-rank test over them
>   is significant at alpha = 0.05. EOData's own 4-of-5 count is reported beside
>   it, no longer part of the verdict. The seed count stays at 5.
> * **Budget.** Per dataset, set from one Boruta run and one 12,000-fit
>   calibration run of stock FASTENER (seed 1999, validation only), by the rule
>   in H2, the same for every arm. The PI's reason: some datasets settle within
>   1,000 fits and others do not, and fits past the point where the search has
>   settled buy nothing.
>
> Unchanged: the arms, the metric, the seeds, the classifier, the split. The
> FASTENER clone moves to `b7e724d`, which only counts what the pruning step
> does -- swaps proposed, fitted and kept -- for H2 and H3's secondary
> reporting. The counters read what pruning did and draw no random numbers, so
> the search is the one at `08e6acd`.
> Recorded as [DEC-33](DECISIONS.md#dec-33).
>
> **2026-10-09 -- DuckDuckGeese leaves H2 and H3.** Decided by the PI during
> the budget calibration, before any H2 or H3 run. At 363,150 features
> FASTENER's own bookkeeping, which handles every subset as a vector over all
> features, made its calibration run the slowest by far: 1,480 of 12,000 fits
> after an hour, about nine hours in all, against two to three for the next
> slowest. At a 12,000-fit budget its 15 experiment runs would each take as
> long. The cost comes from the feature count, not from anything H2 or H3 is
> about. Its calibration run was stopped; no calibration result of it was read,
> and no H2 or H3 result of any dataset exists. H2 and H3 now run on 39
> datasets: EOData and 38 of the UCR/UEA sets. The rule is unchanged, including
> the limit of 6 datasets left out. Recorded as
> [DEC-34](DECISIONS.md#dec-34).
>
> **2026-10-09 -- The budget calibration ended early.** Decided by the PI after
> reading the calibration's validation curves, before any H2 or H3 run. 35 of
> the 39 stock FASTENER runs had reached 12,000 fits; eodata, EigenWorms,
> MotorImagery and PEMS-SF were stopped at 5,770-9,009. For those four the
> budget rule's "its value at 12,000" reads "its value where it stopped", and
> only grid values the run reached can count as settled; nothing else in the
> rule changes. The budgets: 10 datasets at 2,000 fits, 2 at 4,000, 10 at
> 6,000, 17 at 12,000 (table in `EXPERIMENTS.md`, H2H3-E01). Recorded as
> [DEC-35](DECISIONS.md#dec-35).
>
> **2026-10-10 -- H4 at equal compute.** Decided by the PI before any H4 run.
> H4 was registered at equal fits, 6,000 per run (12,000 on the long-budget
> datasets), FS-SDS's split over k = 1..20. A fit costs the two methods very
> different amounts: in a 40-second smoke run on colon, at equal CPU time,
> FS-SDS made 14,052 fits and FASTENER 3,479. The comparison the hypothesis is
> about -- which search does better with the same means -- is a comparison at
> equal compute, so every H4 run now stops on process CPU time, the same for
> both methods on a dataset, set from one stock FASTENER run per dataset at its
> protocol fit budget (seed 1999). The arms, datasets, seeds, metric and
> criterion are unchanged. Recorded as [DEC-36](DECISIONS.md#dec-36).
>
> **2026-10-10 -- Single-threaded numeric libraries for every run.** Found
> while calibrating H4's CPU budgets, before any H4 run. The environment's MKL
> (8 threads) and OpenMP (16) pools made CPU time exceed wall time on 8 of the
> 25 benchmarks (nci9: 3,084 CPU s in 1,629 s). On lymphoma, 1,500 FASTENER
> fits took 384.6 CPU s with the pools and 40.3 s with one thread each, with the
> same front. A CPU budget set on spinning threads would charge the methods for
> idle time, unevenly, so every run now limits each library to one thread, and
> the first calibration (kept as `results/h4-calibration-multithreaded`, not
> used) was repeated. No result of any experiment changes; run times before
> and after are not comparable. Recorded as [DEC-37](DECISIONS.md#dec-37).
>
> **2026-10-10 -- H4-E02: H4 with the ELM.** Decided by the PI after H4-E01 was
> reported. H4-E01 found the two methods comparable when both are driven by the
> decision tree; whether that holds with the paper's FS-SDS classifier is open.
> H4-E02 drives and scores both FASTENER and FS-SDS with the ELM
> (`paper_protocol.ELMClassifier`: 160 sigmoid hidden neurons, fixed random
> weights, least-squares output), a departure from the protocol's single
> classifier for this experiment only, kept within its spirit: each arm is
> judged by the classifier that drove its search. Budgets are H4-E01's CPU
> budgets, unchanged, so all four method-classifier cells get the same compute.
> No tree scores are computed for the ELM arms. Criterion, datasets, seeds and
> metric are H4's. Recorded as [DEC-38](DECISIONS.md#dec-38).
>
> **2026-10-11 -- H4-E03: H4 at equal fits, with FASTENER's bookkeeping
> fixed.** Decided by the PI after H4-E01 and H4-E02 were reported. Profiling
> showed why FS-SDS made 4-5 times FASTENER's fits at equal CPU time: on wide
> data FASTENER spent most of its CPU outside model fits -- a one-off
> mutual-information pass over all features and pure-Python bookkeeping over
> all p genes per candidate (nci9: 2% of its time in tree fits). The
> bookkeeping was vectorised in FASTENER clone `3877a1a`, which gives identical
> fronts for the same seed and fits (checked on 10 cases). H4-E03 compares the
> methods at equal model fits, the budget H4 was first registered with: the
> protocol's fit budget per run, 6,000 or 12,000 on the long-budget datasets,
> FS-SDS's split evenly over k = 1..20. The decision tree drives and scores
> both; criterion, datasets, seeds and metric are H4's. H4-E01 and H4-E02 keep
> their verdicts; their explanation of the fit counts is corrected by a dated
> note. Recorded as [DEC-39](DECISIONS.md#dec-39).
>
> **2026-10-12 -- H5 and H6 on the C1-C7 datasets, with a per-run cap.**
> Decided by the PI before any H5 or H6 run, after a timing pilot (one seed,
> all 18 arms, searches at 600 fits; not an experiment, not in the ledger).
>
> * *Datasets.* H5 and H6 run on H2/H3's 39 datasets -- the 38 UCR/UEA sets
>   drawn from the seven clusters C1-C7 of the archive, and EOData -- instead
>   of the 36 first registered. The 36 lean on wide, small sets (25 paper
>   benchmarks, 12 of them gene expression); the C1-C7 sets were chosen to
>   spread over the archive's shapes, and the result can be read cluster by
>   cluster as H2/H3's was.
> * *Budget.* Each dataset's H2/H3 fit budget
>   (`results/h2h3-calibration/budgets.json`, DEC-33): 2,000 to 12,000 fits
>   per run, for every search alike; FS-SDS splits it evenly over k = 1..20.
> * *Per-run cap: 6 hours.* Uncapped, the pilot put the grid at about 2,500
>   CPU-hours, 90% of it NSGA-II (OBL start) and NSGAII-MIIP on a handful of
>   large datasets, where they start from subsets of about half the features.
>   A method that cannot finish one run in 6 hours has no result on that
>   dataset, with the reason stated. Twelve cells are left out before the run
>   (`h5h6_skip.txt`): NSGAII-MIIP on the three sets with 108,000-192,000
>   features, whose pairwise mutual-information matrix does not fit in memory,
>   and nine NSGA-II and NSGAII-MIIP cells predicted at 6.3 to 138 hours per
>   run. Every other run is stopped if it reaches 6 hours. FASTENER and every
>   other method run on all 39 datasets. The pairwise tests use the datasets
>   on which both methods have results, as registered.
> * *Deterministic selectors run once.* mRMR, ReliefF, HSIC Lasso, the three
>   rankers, RFE and all features give the same subsets for every seed, so each
>   runs once per dataset.
> * *Fixes found by the pilot.* NSGAII-MIIP could compute feature distances a
>   rounding error below zero and fail in k-medoids seeding (Heartbeat,
>   EthanolConcentration, LSST); they are clipped at 0. pyHSICLasso catches an
>   exception under a numpy path numpy 2 removed, so a singular step failed
>   instead of being handled (EOData); the alias is restored. FASTENER clone
>   `3be5697` computes its mutual information 5-11x faster with identical
>   values, and the protocol's weighted F1 is computed in numpy, bit-identical
>   to scikit-learn's; neither changes any result.
>
> Recorded as [DEC-40](DECISIONS.md#dec-40).
>
> **2026-10-26 -- H5 and H6 again, with a random forest (H5H6-E02).** Added after
> H5H6-E01 was reported, before any H5H6-E02 run. H5's and H6's claims,
> criteria, datasets, budgets and cap are unchanged. The new experiment runs
> them with a random forest of 100 trees as the protocol classifier, for every
> method, in place of the decision tree. It is the first test of D2 (conclusions
> are model-dependent) on this grid: whether the verdicts and the cluster
> picture of H5H6-E01 hold under another learner. NSGA-II (OBL and sparse) and
> NSGAII-MIIP now stop after 50 generations that score no new subset, as FS-SDS
> already did; in H5H6-E01 their converged runs spun until the cap.
>
> Recorded as [DEC-41](DECISIONS.md#dec-41).
>
> **2026-10-28 -- H5 and H6 again, with LightGBM (H5H6-E03).** Added after
> H5H6-E02 was reported, before any H5H6-E03 run. H5's and H6's claims,
> criteria, datasets, budgets and cap are unchanged. The third learner is a
> boosted ensemble, LightGBM at its defaults except the smallest leaf, which
> scales with the training split (a twentieth of its rows, 1 to 20): at
> LightGBM's default of 20 the smallest datasets, with 24-34 training rows,
> are nearly unlearnable. With the decision tree (H5H6-E01) and the random
> forest (H5H6-E02) it tests D2 with a learner of another kind.
>
> Recorded as [DEC-44](DECISIONS.md#dec-44); runs record their commit as
> [DEC-43](DECISIONS.md#dec-43) describes.
>
> **2026-10-28 -- H7 to H10 planned.** Added after H5H6-E03 was reported. Their
> claims and criteria are fixed here; what each lists under *To fix before any
> run* is fixed in a later revision before its runs start. For H7, which
> analyses existing runs, nothing at the intermediate checkpoints had been
> computed or read when it was written: the end-of-budget scores of the three
> grids had been. Recorded as [DEC-45](DECISIONS.md#dec-45).
>
> **2026-10-29 -- H10's comparisons fixed for H10-E01.** Before any H10 run: (b)'s
> bootstrap is 10,000 paired resamples over datasets, seed 20200; (c) is read
> with H7-E01's procedure, Holm over its two checkpoints; a Boruta-seeded run's
> checkpoints are offset by Boruta's own fits, which precede FASTENER's. The
> claim and criterion are unchanged.
>
> **2026-10-29 -- H10 under the forest and the tree.** Before any H10 result was
> fetched or read: H10-E02 and H10-E03 run the same two arms on H5H6-E02's and
> H5H6-E01's grids, and H10's criterion is applied to each unchanged, under its
> classifier. H10's verdict stays H10-E01's, as registered; the other two say
> whether it holds under the other classifiers, as the H5H6 grids did for H5 and
> H6. Recorded as [DEC-46](DECISIONS.md#dec-46).
>
> **2026-10-30 -- H8's open points fixed for H8-E01, before any prior was made
> or any run started.** Recorded as [DEC-49](DECISIONS.md#dec-49).
>
> - *Datasets:* the 16 of `DATASETS_USED.md`, "H8: datasets with named
>   features" (six on disk, ten from OpenML), each with a data dictionary
>   (`priors/dictionaries/`, written by `make_h8_dictionaries.py`).
> - *Models and prompt:* three Anthropic models through OpenRouter,
>   `anthropic/claude-opus-5.5`, `anthropic/claude-sonnet-5.5` and
>   `anthropic/claude-haiku-5.5`; temperature 0, seed 20200; the prompt of
>   `llm_guidance.LLMFeaturePrior` (the task, class names, data description and
>   each feature's index, name and documented description; a score in [0, 1]
>   per feature), at most 300 features per call. One prior per dataset and
>   model, and one scrambled (names replaced by neutral tokens, descriptions
>   dropped), made once and committed with the full responses before any run.
> - *What the prior guides:* all three operators -- mating, mutation
>   (`guidance.PriorGuidedMutationStrategy`) and the initial singles, five
>   drawn from the weights in place of stock FASTENER's five random ones --
>   with lambda = 0.5. The claim's "drawn its initial singles from w" and "w
>   wherever it now uses mutual information" are kept; mutation is added.
> - *Arms added:* per model, the prior plus the online subset proposer
>   (`llm_guidance.LLMSubsetProposer`: every 5 generations the model sees the
>   current front and proposes up to 5 subsets of at most 10 features, which
>   are evaluated from the same fit budget); and, with Opus, the prior on one
>   operator at a time (mating, mutation, initial). Both are reported beside the
>   criterion.
> - *Budget, classifier, data:* 1,000 fits per run for every dataset, LightGBM
>   (DEC-44's setting), the 50,000-row cap, seeds 2020-2024, a 6-hour cap per
>   run, on the workstation.
> - *Criterion, made exact for three models:* for each model, part (i)
>   `fastener_llm_<model>` against `fastener` and part (ii) against
>   `fastener_llm_<model>_scrambled`, each as registered (log2 fits ratio to
>   the common target, more positive datasets than negative, two-sided
>   Wilcoxon), Holm-corrected over the three models within each part. H8 is
>   supported if both parts hold for at least one model. The common target
>   reads validation AUF (K = 10) from each run's trajectory: the mean over
>   k = 1..10 of the best validation score of a subset of at most k features,
>   0 for a size not reached.
>
> **2026-10-30 -- H8-E01 moves to HPC Vega, before any result was read.** On
> the workstation, one thread per run, a 1,000-fit run on the 50,000-row sets
> took about 5 hours (eodata), near the 6-hour cap, so the experiment would
> have taken 5-6 days. It runs on Vega instead, 8 cores per run as H5H6-E03;
> the proposer arms reach OpenRouter from the compute nodes (checked). Nothing
> else changes. The first start on the workstation was stopped after 15
> minutes; its 12 unfinished runs are set aside unread. Recorded as
> [DEC-50](DECISIONS.md#dec-50).
>
> **2026-10-30 -- H8's control made strict, before any result of H8-E01 was
> read.** Writing the methods section, the scrambled prompt turned out to keep
> the dataset description (which says how the names are built, e.g. spambase's
> word_freq_WORD) and the column order; the scrambled priors follow the named
> ones closely (Spearman up to 0.99: higgs, phishing, spambase), so they do not
> hide what the features are. Only priors were compared, no run. Part (ii) of
> the criterion is therefore read against a strict control,
> `fastener_llm_<model>_blind`: the features shown in a shuffled order (a fixed
> permutation, seed 20200), each named only by its position, no dataset or
> feature description -- the task and class names stay -- with the scores
> mapped back to the columns. Its priors (48) are made now; its 240 runs are
> H8-E02, on H8-E01's setup. H8-E01's scrambled arm is reported beside the
> criterion, as names hidden but context kept. Everything else is unchanged.
> Recorded as [DEC-51](DECISIONS.md#dec-51).

Secondary, shown for interpretation only: AUF at the other K, hypervolume, the smallest subset size on the front, fits and wall clock.

## 4. Description of the experiment

### Setup

**`20261030T005602Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005725Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2022`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_eodata_fastener_llm_opus_blind_s2022`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_eodata_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005725Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2020`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2021`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_eodata_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2020`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_eodata_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005725Z_h8e02_covertype_fastener_llm_opus_blind_s2020`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_covertype_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2024`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_eodata_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2021`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_covertype_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2023`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_covertype_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2021`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2024`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2020`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2022`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2022`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2021`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2023`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2024`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_eodata_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2023`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2021`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_eodata_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_opus_blind_s2023`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_eodata_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2022`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_covertype_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2024`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2021`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2021`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_eodata_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2023`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_covertype_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2020`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_covertype_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2023`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_eodata_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2023`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_diabetes130_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2021`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_covertype_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2021`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_covertype_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2023`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_eodata_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2022`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_eodata_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2022`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_covertype_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2022`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_eodata_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2020`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_eodata_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2024`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_eodata_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2022`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_covertype_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2024`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_covertype_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2020`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_covertype_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2020`** -- dataset `eodata`: 182 features, 29976/10008/10008 train/val/test rows.

```
run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_eodata_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2024`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_covertype_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2024`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2024`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_covertype_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2023`** -- dataset `covertype`: 54 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_covertype_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2020`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2020`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_diabetes130_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2022`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_diabetes130_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2021`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_diabetes130_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2020`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2023`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_phishing_fastener_llm_opus_blind_s2020`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_phishing_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2023`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005726Z_h8e02_higgs_fastener_llm_haiku_blind_s2024`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_higgs_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2023`** -- dataset `crop_mapping`: 174 features, 30002/9999/9999 train/val/test rows.

```
run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2021`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_har_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2022`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2021`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2020`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_har_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2024`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_higgs_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2020`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_higgs_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2021`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_higgs_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2022`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_higgs_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2024`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_phishing_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2023`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_har_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2020`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_higgs_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2024`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2022`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_higgs_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2020`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2023`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_higgs_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2024`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2024`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_higgs_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_har_fastener_llm_sonnet_blind_s2020`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_har_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2021`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2022`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_har_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2022`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_diabetes130_fastener_llm_opus_blind_s2024`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_diabetes130_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2021`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_higgs_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2021`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_phishing_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2024`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_har_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2021`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_adult_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2020`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2022`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_adult_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2023`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_higgs_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2021`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_adult_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2022`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2020`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2022`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_higgs_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2024`** -- dataset `diabetes130`: 132 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2023`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_higgs_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2020`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_higgs_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2023`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2021`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2021`** -- dataset `higgs`: 28 features, 30000/10000/10000 train/val/test rows.

```
run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_higgs_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2021`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_heloc_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2022`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2020`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_phishing_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2024`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2022`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_phishing_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2021`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2023`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2023`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_spambase_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2022`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_phishing_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2024`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_heloc_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2022`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_spambase_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_spambase_fastener_llm_opus_blind_s2024`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_spambase_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2022`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2023`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2021`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2020`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_har_fastener_llm_haiku_blind_s2022`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_har_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2023`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_phishing_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2024`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_phishing_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2022`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_heloc_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2024`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_heloc_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2023`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_adult_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2024`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_adult_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2022`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_heloc_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2023`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_phishing_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2021`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_gas_drift_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2020`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_heloc_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2021`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_phishing_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2024`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_heloc_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2021`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2024`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_gas_drift_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2023`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_har_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2023`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_spambase_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2020`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_gas_drift_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2024`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_adult_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2021`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_heloc_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2020`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_heloc_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2023`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_adult_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_adult_fastener_llm_haiku_blind_s2020`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_adult_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2022`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_phishing_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2021`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_phishing_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2023`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_adult_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2024`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_adult_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2020`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_phishing_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2021`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_heloc_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2023`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_heloc_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2023`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_heloc_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2022`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_heloc_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2023`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_heloc_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2023`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_gas_drift_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2021`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_spambase_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2022`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_spambase_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2020`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_har_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2020`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2024`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_spambase_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2024`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2021`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_adult_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2021`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_har_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2023`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_har_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2022`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_har_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_heloc_fastener_llm_opus_blind_s2020`** -- dataset `heloc`: 22 features, 6000/2000/2000 train/val/test rows.

```
run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_heloc_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2024`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_har_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2020`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2024`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2020`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_adult_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2024`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_har_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2021`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2024`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_pc4_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2021`** -- dataset `har`: 561 features, 6181/2059/2059 train/val/test rows.

```
run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_har_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2023`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_pc4_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2024`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2023`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2022`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_pc4_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2021`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_pc4_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2023`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_spambase_fastener_llm_haiku_blind_s2020`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_spambase_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2024`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_spambase_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005730Z_h8e02_adult_fastener_llm_haiku_blind_s2022`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_adult_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005730Z_h8e02_phishing_fastener_llm_haiku_blind_s2024`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_phishing_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_gas_drift_fastener_llm_opus_blind_s2022`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_gas_drift_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2021`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_spambase_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2020`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_adult_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2022`** -- dataset `ozone_8hr`: 72 features, 1520/507/507 train/val/test rows.

```
run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2022`** -- dataset `adult`: 63 features, 29306/9768/9768 train/val/test rows.

```
run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_adult_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_pc4_fastener_llm_opus_blind_s2020`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_pc4_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2020`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_spambase_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005731Z_h8e02_spambase_fastener_llm_opus_blind_s2020`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_spambase_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005731Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2021`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005731Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2022`** -- dataset `gas_drift`: 128 features, 8346/2782/2782 train/val/test rows.

```
run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005731Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2022`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005732Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2023`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005732Z_h8e02_spambase_fastener_llm_opus_blind_s2021`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_spambase_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005734Z_h8e02_spambase_fastener_llm_opus_blind_s2022`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_spambase_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005734Z_h8e02_phishing_fastener_llm_haiku_blind_s2023`** -- dataset `phishing`: 30 features, 6633/2211/2211 train/val/test rows.

```
run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_phishing_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2020`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_eye_movements_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_spambase_fastener_llm_opus_blind_s2023`** -- dataset `spambase`: 57 features, 2759/921/921 train/val/test rows.

```
run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_spambase_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2020`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2021`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2024`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2023`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2024`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2021`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_eye_movements_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2020`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2023`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_eye_movements_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2022`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2022`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_eye_movements_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2024`** -- dataset `eye_movements`: 20 features, 4564/1522/1522 train/val/test rows.

```
run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_eye_movements_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005812Z_h8e02_pc4_fastener_llm_sonnet_blind_s2021`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_pc4_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005813Z_h8e02_pc4_fastener_llm_sonnet_blind_s2023`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_pc4_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005814Z_h8e02_pc4_fastener_llm_sonnet_blind_s2020`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_pc4_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2022`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_pc4_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2024`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_pc4_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2022`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_pc4_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2023`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_pc4_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2021`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_pc4_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2024`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_pc4_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005828Z_h8e02_pc4_fastener_llm_haiku_blind_s2020`** -- dataset `pc4`: 37 features, 874/292/292 train/val/test rows.

```
run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_pc4_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2021`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_mice_protein_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2020`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_mice_protein_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005829Z_h8e02_mice_protein_fastener_llm_opus_blind_s2022`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_mice_protein_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2023`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_mice_protein_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2024`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_mice_protein_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2020`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2021`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005834Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2023`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2022`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2024`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005855Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2020`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2021`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2022`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005858Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2020`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2023`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2024`** -- dataset `mice_protein`: 77 features, 648/216/216 train/val/test rows.

```
run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005900Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2021`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2022`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2024`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2021`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2023`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2022`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2023`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2020`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2024`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2023`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2024`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2022`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

**`20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2021`** -- dataset `qsar_biodeg`: 41 features, 633/211/211 train/val/test rows.

```
run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
```

Parameters per run:

| parameter | 20261030T005602Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020 | 20261030T005725Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2022 | 20261030T005726Z_h8e02_eodata_fastener_llm_opus_blind_s2022 | 20261030T005725Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2020 | 20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2021 | 20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2020 | 20261030T005725Z_h8e02_covertype_fastener_llm_opus_blind_s2020 | 20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2024 | 20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2021 | 20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2021 | 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2024 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2020 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2022 | 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2022 | 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2021 | 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2023 | 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2024 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2021 | 20261030T005728Z_h8e02_eodata_fastener_llm_opus_blind_s2023 | 20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2022 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2024 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2021 | 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2021 | 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2023 | 20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2020 | 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2023 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2023 | 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2021 | 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2021 | 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2022 | 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2022 | 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2022 | 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2020 | 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2024 | 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2022 | 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2024 | 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2020 | 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2020 | 20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2024 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2024 | 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2024 | 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2023 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2020 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2020 | 20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2022 | 20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2021 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2020 | 20261030T005726Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2023 | 20261030T005726Z_h8e02_phishing_fastener_llm_opus_blind_s2020 | 20261030T005726Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2023 | 20261030T005726Z_h8e02_higgs_fastener_llm_haiku_blind_s2024 | 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2023 | 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2021 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2022 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2021 | 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2020 | 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2024 | 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2020 | 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2021 | 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2022 | 20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2024 | 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2023 | 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2020 | 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2024 | 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2022 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2020 | 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2023 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2024 | 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2024 | 20261030T005727Z_h8e02_har_fastener_llm_sonnet_blind_s2020 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2021 | 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2022 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2022 | 20261030T005728Z_h8e02_diabetes130_fastener_llm_opus_blind_s2024 | 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2021 | 20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2021 | 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2024 | 20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2021 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2020 | 20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2022 | 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2023 | 20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2021 | 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2022 | 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2020 | 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2022 | 20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2024 | 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2023 | 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2020 | 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2023 | 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2021 | 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2021 | 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2021 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2022 | 20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2020 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2024 | 20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2022 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2021 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2023 | 20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2023 | 20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2022 | 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2024 | 20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2022 | 20261030T005728Z_h8e02_spambase_fastener_llm_opus_blind_s2024 | 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2022 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2021 | 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2020 | 20261030T005728Z_h8e02_har_fastener_llm_haiku_blind_s2022 | 20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2023 | 20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2024 | 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2022 | 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2024 | 20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2024 | 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2022 | 20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2023 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2021 | 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2020 | 20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2021 | 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2024 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2021 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2024 | 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2020 | 20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2024 | 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2021 | 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2020 | 20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2023 | 20261030T005729Z_h8e02_adult_fastener_llm_haiku_blind_s2020 | 20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2022 | 20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2021 | 20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2023 | 20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2024 | 20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2020 | 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2021 | 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2023 | 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2022 | 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2023 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2023 | 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2021 | 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2022 | 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2020 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2020 | 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2024 | 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2024 | 20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2021 | 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2021 | 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2023 | 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2022 | 20261030T005729Z_h8e02_heloc_fastener_llm_opus_blind_s2020 | 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2024 | 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2020 | 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2024 | 20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2020 | 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2024 | 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2021 | 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2024 | 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2021 | 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2023 | 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2024 | 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2023 | 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2022 | 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2021 | 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2023 | 20261030T005729Z_h8e02_spambase_fastener_llm_haiku_blind_s2020 | 20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2024 | 20261030T005730Z_h8e02_adult_fastener_llm_haiku_blind_s2022 | 20261030T005730Z_h8e02_phishing_fastener_llm_haiku_blind_s2024 | 20261030T005729Z_h8e02_gas_drift_fastener_llm_opus_blind_s2022 | 20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2021 | 20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2020 | 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2022 | 20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2022 | 20261030T005729Z_h8e02_pc4_fastener_llm_opus_blind_s2020 | 20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2020 | 20261030T005731Z_h8e02_spambase_fastener_llm_opus_blind_s2020 | 20261030T005731Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2021 | 20261030T005731Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2022 | 20261030T005731Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2022 | 20261030T005732Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2023 | 20261030T005732Z_h8e02_spambase_fastener_llm_opus_blind_s2021 | 20261030T005734Z_h8e02_spambase_fastener_llm_opus_blind_s2022 | 20261030T005734Z_h8e02_phishing_fastener_llm_haiku_blind_s2023 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2020 | 20261030T005735Z_h8e02_spambase_fastener_llm_opus_blind_s2023 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2020 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2021 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2024 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2023 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2024 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2021 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2020 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2023 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2022 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2022 | 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2024 | 20261030T005812Z_h8e02_pc4_fastener_llm_sonnet_blind_s2021 | 20261030T005813Z_h8e02_pc4_fastener_llm_sonnet_blind_s2023 | 20261030T005814Z_h8e02_pc4_fastener_llm_sonnet_blind_s2020 | 20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2022 | 20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2024 | 20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2022 | 20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2023 | 20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2021 | 20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2024 | 20261030T005828Z_h8e02_pc4_fastener_llm_haiku_blind_s2020 | 20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2021 | 20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2020 | 20261030T005829Z_h8e02_mice_protein_fastener_llm_opus_blind_s2022 | 20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2023 | 20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2024 | 20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2020 | 20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2021 | 20261030T005834Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2023 | 20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2022 | 20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2024 | 20261030T005855Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2020 | 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2021 | 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2022 | 20261030T005858Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2020 | 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2023 | 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2024 | 20261030T005900Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2021 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2022 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2024 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2021 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2023 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2022 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2023 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2020 | 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2024 | 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2023 | 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2024 | 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2022 | 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2021 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| boruta_estimator | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "protocol LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" |
| boruta_max_iter | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| cpu_seconds_per_run | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null |
| dataset | "qsar_biodeg" | "crop_mapping" | "eodata" | "diabetes130" | "eodata" | "eodata" | "covertype" | "eodata" | "covertype" | "covertype" | "crop_mapping" | "crop_mapping" | "crop_mapping" | "crop_mapping" | "crop_mapping" | "crop_mapping" | "crop_mapping" | "eodata" | "crop_mapping" | "eodata" | "eodata" | "covertype" | "crop_mapping" | "crop_mapping" | "eodata" | "covertype" | "covertype" | "eodata" | "diabetes130" | "covertype" | "covertype" | "eodata" | "eodata" | "covertype" | "eodata" | "eodata" | "eodata" | "covertype" | "covertype" | "covertype" | "eodata" | "covertype" | "crop_mapping" | "covertype" | "covertype" | "crop_mapping" | "diabetes130" | "diabetes130" | "diabetes130" | "crop_mapping" | "diabetes130" | "phishing" | "diabetes130" | "higgs" | "crop_mapping" | "har" | "diabetes130" | "diabetes130" | "har" | "higgs" | "higgs" | "higgs" | "higgs" | "phishing" | "har" | "higgs" | "ozone_8hr" | "higgs" | "diabetes130" | "higgs" | "diabetes130" | "higgs" | "har" | "diabetes130" | "har" | "diabetes130" | "diabetes130" | "higgs" | "phishing" | "har" | "adult" | "gas_drift" | "adult" | "higgs" | "adult" | "ozone_8hr" | "ozone_8hr" | "higgs" | "diabetes130" | "higgs" | "higgs" | "ozone_8hr" | "ozone_8hr" | "higgs" | "heloc" | "gas_drift" | "phishing" | "gas_drift" | "phishing" | "gas_drift" | "gas_drift" | "spambase" | "phishing" | "heloc" | "spambase" | "spambase" | "ozone_8hr" | "gas_drift" | "ozone_8hr" | "ozone_8hr" | "har" | "phishing" | "phishing" | "heloc" | "heloc" | "adult" | "adult" | "heloc" | "phishing" | "gas_drift" | "heloc" | "phishing" | "heloc" | "gas_drift" | "gas_drift" | "har" | "spambase" | "gas_drift" | "adult" | "heloc" | "heloc" | "adult" | "adult" | "phishing" | "phishing" | "adult" | "adult" | "phishing" | "heloc" | "heloc" | "heloc" | "heloc" | "heloc" | "gas_drift" | "spambase" | "spambase" | "har" | "gas_drift" | "spambase" | "gas_drift" | "adult" | "har" | "har" | "har" | "heloc" | "har" | "ozone_8hr" | "ozone_8hr" | "adult" | "har" | "ozone_8hr" | "pc4" | "har" | "pc4" | "ozone_8hr" | "ozone_8hr" | "pc4" | "pc4" | "ozone_8hr" | "spambase" | "spambase" | "adult" | "phishing" | "gas_drift" | "spambase" | "adult" | "ozone_8hr" | "adult" | "pc4" | "spambase" | "spambase" | "eye_movements" | "gas_drift" | "eye_movements" | "eye_movements" | "spambase" | "spambase" | "phishing" | "eye_movements" | "spambase" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "eye_movements" | "pc4" | "pc4" | "pc4" | "pc4" | "pc4" | "pc4" | "pc4" | "pc4" | "pc4" | "pc4" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "mice_protein" | "qsar_biodeg" | "mice_protein" | "mice_protein" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" | "qsar_biodeg" |
| evaluation_budget_per_seed | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| fastener_arms | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_opus_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_sonnet_blind"] | ["llm_opus_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] | ["llm_haiku_blind"] |
| fastener_max_fits | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| fastener_rounds | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 | 100000 |
| fs_sds_cpu_seconds_per_k | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null |
| fs_sds_evaluations_per_k | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 |
| fs_sds_evaluations_total | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| fs_sds_iterations | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null |
| fs_sds_k_range | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] |
| fs_sds_population | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null | null |
| k_grid | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100, 200, 500] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50, 100] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 50] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30] |
| lgbm_min_child_samples | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| max_rows | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 |
| methods | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] | [] |
| model | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" | "LGBMClassifier(100 trees, min_child_samples=min(20, max(1, n_train // 20)), deterministic)" |
| model_n_jobs | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| model_seed | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 | 20200 |
| n_rows_used | 1055 | 50000 | 49992 | 50000 | 49992 | 49992 | 50000 | 49992 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 49992 | 50000 | 49992 | 49992 | 50000 | 50000 | 50000 | 49992 | 50000 | 50000 | 49992 | 50000 | 50000 | 50000 | 49992 | 49992 | 50000 | 49992 | 49992 | 49992 | 50000 | 50000 | 50000 | 49992 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 50000 | 11055 | 50000 | 50000 | 50000 | 10299 | 50000 | 50000 | 10299 | 50000 | 50000 | 50000 | 50000 | 11055 | 10299 | 50000 | 2534 | 50000 | 50000 | 50000 | 50000 | 50000 | 10299 | 50000 | 10299 | 50000 | 50000 | 50000 | 11055 | 10299 | 48842 | 13910 | 48842 | 50000 | 48842 | 2534 | 2534 | 50000 | 50000 | 50000 | 50000 | 2534 | 2534 | 50000 | 10000 | 13910 | 11055 | 13910 | 11055 | 13910 | 13910 | 4601 | 11055 | 10000 | 4601 | 4601 | 2534 | 13910 | 2534 | 2534 | 10299 | 11055 | 11055 | 10000 | 10000 | 48842 | 48842 | 10000 | 11055 | 13910 | 10000 | 11055 | 10000 | 13910 | 13910 | 10299 | 4601 | 13910 | 48842 | 10000 | 10000 | 48842 | 48842 | 11055 | 11055 | 48842 | 48842 | 11055 | 10000 | 10000 | 10000 | 10000 | 10000 | 13910 | 4601 | 4601 | 10299 | 13910 | 4601 | 13910 | 48842 | 10299 | 10299 | 10299 | 10000 | 10299 | 2534 | 2534 | 48842 | 10299 | 2534 | 1458 | 10299 | 1458 | 2534 | 2534 | 1458 | 1458 | 2534 | 4601 | 4601 | 48842 | 11055 | 13910 | 4601 | 48842 | 2534 | 48842 | 1458 | 4601 | 4601 | 7608 | 13910 | 7608 | 7608 | 4601 | 4601 | 11055 | 7608 | 4601 | 7608 | 7608 | 7608 | 7608 | 7608 | 7608 | 7608 | 7608 | 7608 | 7608 | 7608 | 1458 | 1458 | 1458 | 1458 | 1458 | 1458 | 1458 | 1458 | 1458 | 1458 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1080 | 1055 | 1080 | 1080 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 | 1055 |
| nsga_max_barren_generations | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 |
| nsgaii_miip_init | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" | "obl" |
| numeric_threads | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} | {"openmp:libgomp": 1, "openblas:libopenblas": 1} | {"openblas:libopenblas": 1, "openmp:libgomp": 1} |
| poss_k | 41 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 30 | 50 | 28 | 50 | 50 | 50 | 50 | 50 | 28 | 28 | 28 | 28 | 30 | 50 | 28 | 50 | 28 | 50 | 28 | 50 | 28 | 50 | 50 | 50 | 50 | 50 | 28 | 30 | 50 | 50 | 50 | 50 | 28 | 50 | 50 | 50 | 28 | 50 | 28 | 28 | 50 | 50 | 28 | 22 | 50 | 30 | 50 | 30 | 50 | 50 | 50 | 30 | 22 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 30 | 30 | 22 | 22 | 50 | 50 | 22 | 30 | 50 | 22 | 30 | 22 | 50 | 50 | 50 | 50 | 50 | 50 | 22 | 22 | 50 | 50 | 30 | 30 | 50 | 50 | 30 | 22 | 22 | 22 | 22 | 22 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 22 | 50 | 50 | 50 | 50 | 50 | 50 | 37 | 50 | 37 | 50 | 50 | 37 | 37 | 50 | 50 | 50 | 50 | 30 | 50 | 50 | 50 | 50 | 50 | 37 | 50 | 50 | 20 | 50 | 20 | 20 | 50 | 50 | 30 | 20 | 50 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 37 | 37 | 37 | 37 | 37 | 37 | 37 | 37 | 37 | 37 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 41 | 50 | 50 | 41 | 41 | 41 | 41 | 41 | 41 | 41 | 41 | 41 | 41 | 41 | 41 | 41 |
| primary_metric | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" | "f1_weighted" |
| protocol_model | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" | "lgbm" |
| quick | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false | false |
| search_model | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" | "tree" |
| seeds | [2020] | [2022] | [2022] | [2020] | [2021] | [2020] | [2020] | [2024] | [2021] | [2023] | [2021] | [2024] | [2020] | [2022] | [2022] | [2021] | [2023] | [2024] | [2023] | [2021] | [2023] | [2022] | [2024] | [2021] | [2021] | [2023] | [2020] | [2023] | [2023] | [2021] | [2021] | [2023] | [2022] | [2022] | [2022] | [2020] | [2024] | [2022] | [2024] | [2020] | [2020] | [2024] | [2024] | [2024] | [2023] | [2020] | [2020] | [2022] | [2021] | [2020] | [2023] | [2020] | [2023] | [2024] | [2023] | [2021] | [2022] | [2021] | [2020] | [2024] | [2020] | [2021] | [2022] | [2024] | [2023] | [2020] | [2024] | [2022] | [2020] | [2023] | [2024] | [2024] | [2020] | [2021] | [2022] | [2022] | [2024] | [2021] | [2021] | [2024] | [2021] | [2020] | [2022] | [2023] | [2021] | [2022] | [2020] | [2022] | [2024] | [2023] | [2020] | [2023] | [2021] | [2021] | [2021] | [2022] | [2020] | [2024] | [2022] | [2021] | [2023] | [2023] | [2022] | [2024] | [2022] | [2024] | [2022] | [2023] | [2021] | [2020] | [2022] | [2023] | [2024] | [2022] | [2024] | [2023] | [2024] | [2022] | [2023] | [2021] | [2020] | [2021] | [2024] | [2021] | [2024] | [2023] | [2023] | [2020] | [2024] | [2021] | [2020] | [2023] | [2020] | [2022] | [2021] | [2023] | [2024] | [2020] | [2021] | [2023] | [2023] | [2022] | [2023] | [2023] | [2021] | [2022] | [2020] | [2020] | [2024] | [2024] | [2021] | [2021] | [2023] | [2022] | [2020] | [2024] | [2020] | [2024] | [2020] | [2024] | [2021] | [2024] | [2021] | [2023] | [2024] | [2023] | [2022] | [2021] | [2023] | [2020] | [2024] | [2022] | [2024] | [2022] | [2021] | [2020] | [2022] | [2022] | [2020] | [2020] | [2020] | [2021] | [2022] | [2022] | [2023] | [2021] | [2022] | [2023] | [2020] | [2023] | [2020] | [2021] | [2024] | [2023] | [2024] | [2021] | [2020] | [2023] | [2022] | [2022] | [2024] | [2021] | [2023] | [2020] | [2022] | [2024] | [2022] | [2023] | [2021] | [2024] | [2020] | [2021] | [2020] | [2022] | [2023] | [2024] | [2020] | [2021] | [2023] | [2022] | [2024] | [2020] | [2021] | [2022] | [2020] | [2023] | [2024] | [2021] | [2022] | [2024] | [2021] | [2023] | [2022] | [2023] | [2020] | [2024] | [2023] | [2024] | [2022] | [2021] |
| split | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" | "protocol" |
| with_fastener | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true | true |

Arms:

| arm | algorithm ID | what distinguishes it |
|---|---|---|
| fastener_llm_haiku_blind | `fastener_llm_haiku_blind@79d5ac2+9226b90#8b24` | FASTENER guided as H8-E01's `fastener_llm_haiku` (mating, mutation and the five starting singles; lambda 0.5), with Haiku 5.5's *blind* prior: the features shown in a fixed shuffled order (permutation seed 20200), each named `feature_<position>`, no dataset or feature description, the task and class names kept; the scores mapped back to the columns. `#8b24` is the hash of this config (model, prior file); one per arm. No model call during the run. |
| fastener_llm_opus_blind | `fastener_llm_opus_blind@79d5ac2+9226b90#e4af` | FASTENER guided as H8-E01's `fastener_llm_opus` (mating, mutation and the five starting singles; lambda 0.5), with Opus 5.5's *blind* prior: the features shown in a fixed shuffled order (permutation seed 20200), each named `feature_<position>`, no dataset or feature description, the task and class names kept; the scores mapped back to the columns. `#e4af` is the hash of this config (model, prior file); one per arm. No model call during the run. |
| fastener_llm_sonnet_blind | `fastener_llm_sonnet_blind@79d5ac2+9226b90#6637` | FASTENER guided as H8-E01's `fastener_llm_sonnet` (mating, mutation and the five starting singles; lambda 0.5), with Sonnet 5.5's *blind* prior: the features shown in a fixed shuffled order (permutation seed 20200), each named `feature_<position>`, no dataset or feature description, the task and class names kept; the scores mapped back to the columns. `#6637` is the hash of this config (model, prior file); one per arm. No model call during the run. |

**Deviations from the protocol:** none from the design registered on 2026-10-30 (DEC-51), before any H8-E01 result was read. Execution as H8-E01: HPC Vega, 8 cores and 8 GB per run, LightGBM, 1,000 fits for every dataset (`experiments/h8_budgets.json`), the 50,000-row cap, 6-hour limit; `hpc/vega/h8e02.env`. H8-E02's runs are on experiments commit `79d5ac2`, H8-E01's on `df0f88b`; FASTENER is `9226b90` for both. Between the two commits only `llm_guidance.py` (the blind mode, added beside the named and scrambled ones), `run_sota.py` (the three blind arms), `h8_report.py`, tests and docs changed; the named and stock arms' code paths are unchanged, so the criterion compares runs of the same algorithm apart from the prior.

### How the blind prior was made

As H8-E01's priors (its SUPPORT.md, *How the language models were used*), with `llm_guidance.LLMFeaturePrior(blind=True)`: the same system instruction, model, temperature 0, seed 20200 and `max_tokens`; the user message keeps `Task:` and `Classes:`, drops the `Data:` description and the feature descriptions, and lists the features as `<position>: feature_<position>` in the order of a fixed permutation (`np.random.RandomState(20200).permutation(n_features)`, stored in each prior file as `permutation`). Position p showed column `permutation[p]`; the scores are mapped back to the columns before they are saved. The prompt does not say that the order is shuffled. 48 priors (16 datasets x 3 models; har in two calls of at most 300 features), 51 calls, $0.84, committed in `79d5ac2` with the call log (`experiments/priors/calls.jsonl`) before any run. Spambase's prompt and reply for each model, as sent: [methods/](methods/) (`prior_spambase_*_blind.txt`). 8 of the 48 are flat (one score for every feature): diabetes130 for all three models; Haiku's crop_mapping, eodata, mice_protein, ozone_8hr and qsar_biodeg.

### What happened

| run | status | started (UTC) | ended (UTC) | elapsed (s) | results file |
|---|---|---|---|---|---|
| `20261030T005602Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:56:02.611862+00:00 | 2026-10-30T00:57:09.310646+00:00 | 66.6990 | raw_results.json |
| `20261030T005725Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:25.755387+00:00 | 2026-10-30T01:14:35.369068+00:00 | 1029.6140 | raw_results.json |
| `20261030T005726Z_h8e02_eodata_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:26.792185+00:00 | 2026-10-30T01:53:06.615738+00:00 | 3339.8240 | raw_results.json |
| `20261030T005725Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:25.178520+00:00 | 2026-10-30T01:03:27.721127+00:00 | 362.5430 | raw_results.json |
| `20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:27.663549+00:00 | 2026-10-30T02:14:33.390565+00:00 | 4625.7270 | raw_results.json |
| `20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:27.465069+00:00 | 2026-10-30T02:14:16.070056+00:00 | 4608.6050 | raw_results.json |
| `20261030T005725Z_h8e02_covertype_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:25.987374+00:00 | 2026-10-30T01:11:25.828341+00:00 | 839.8410 | raw_results.json |
| `20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:27.730660+00:00 | 2026-10-30T02:13:05.359598+00:00 | 4537.6290 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:26.213527+00:00 | 2026-10-30T01:20:10.279690+00:00 | 1364.0660 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:26.596850+00:00 | 2026-10-30T01:17:06.758077+00:00 | 1180.1610 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.006274+00:00 | 2026-10-30T01:15:51.340883+00:00 | 1103.3350 | raw_results.json |
| `20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:27.839249+00:00 | 2026-10-30T01:20:10.868841+00:00 | 1363.0300 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:28.006739+00:00 | 2026-10-30T01:22:08.073945+00:00 | 1480.0670 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:28.005825+00:00 | 2026-10-30T01:17:24.226433+00:00 | 1196.2210 | raw_results.json |
| `20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:27.777424+00:00 | 2026-10-30T01:19:46.273287+00:00 | 1338.4960 | raw_results.json |
| `20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:27.957554+00:00 | 2026-10-30T01:17:38.769147+00:00 | 1210.8120 | raw_results.json |
| `20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:27.914196+00:00 | 2026-10-30T01:26:53.986206+00:00 | 1766.0720 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:28.201482+00:00 | 2026-10-30T01:55:15.865136+00:00 | 3467.6640 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:28.173951+00:00 | 2026-10-30T01:21:23.131037+00:00 | 1434.9570 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:28.079608+00:00 | 2026-10-30T01:55:32.789027+00:00 | 3484.7090 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:28.174030+00:00 | 2026-10-30T01:50:21.106813+00:00 | 3172.9330 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:27.000399+00:00 | 2026-10-30T01:17:18.656856+00:00 | 1191.6560 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:28.384787+00:00 | 2026-10-30T01:19:16.055375+00:00 | 1307.6710 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:28.577336+00:00 | 2026-10-30T01:24:51.241790+00:00 | 1642.6640 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.196373+00:00 | 2026-10-30T01:51:17.872989+00:00 | 3229.6770 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:26.647363+00:00 | 2026-10-30T01:11:46.783636+00:00 | 860.1360 | raw_results.json |
| `20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:27.322697+00:00 | 2026-10-30T01:17:24.983983+00:00 | 1197.6610 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:28.216108+00:00 | 2026-10-30T01:52:01.472953+00:00 | 3273.2570 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:27.130010+00:00 | 2026-10-30T01:06:52.934138+00:00 | 565.8040 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:26.722727+00:00 | 2026-10-30T01:11:35.250604+00:00 | 848.5280 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:26.732125+00:00 | 2026-10-30T01:12:01.457127+00:00 | 874.7250 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:28.270257+00:00 | 2026-10-30T01:48:39.033254+00:00 | 3070.7630 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:28.248743+00:00 | 2026-10-30T02:12:43.090226+00:00 | 4514.8420 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:26.723477+00:00 | 2026-10-30T01:11:08.201873+00:00 | 821.4780 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:28.269494+00:00 | 2026-10-30T01:52:05.246180+00:00 | 3276.9770 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:28.253414+00:00 | 2026-10-30T01:51:44.692365+00:00 | 3256.4390 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:28.197591+00:00 | 2026-10-30T01:51:16.770706+00:00 | 3228.5730 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:26.724164+00:00 | 2026-10-30T01:11:26.206926+00:00 | 839.4830 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:26.872486+00:00 | 2026-10-30T01:11:27.606425+00:00 | 840.7340 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:26.868216+00:00 | 2026-10-30T01:11:14.998297+00:00 | 828.1300 | raw_results.json |
| `20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:28.330757+00:00 | 2026-10-30T01:51:33.756582+00:00 | 3245.4260 | raw_results.json |
| `20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:27.000671+00:00 | 2026-10-30T01:15:35.686956+00:00 | 1088.6860 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:28.586332+00:00 | 2026-10-30T01:21:36.205144+00:00 | 1447.6190 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:26.896708+00:00 | 2026-10-30T01:22:38.620800+00:00 | 1511.7240 | raw_results.json |
| `20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:26.897515+00:00 | 2026-10-30T01:18:50.179273+00:00 | 1283.2820 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:28.554866+00:00 | 2026-10-30T01:15:10.115900+00:00 | 1061.5610 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:27.263103+00:00 | 2026-10-30T01:06:51.373928+00:00 | 564.1110 | raw_results.json |
| `20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:26.935682+00:00 | 2026-10-30T01:05:56.682742+00:00 | 509.7470 | raw_results.json |
| `20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:26.935175+00:00 | 2026-10-30T01:06:06.905191+00:00 | 519.9700 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:28.307358+00:00 | 2026-10-30T01:14:46.338418+00:00 | 1038.0310 | raw_results.json |
| `20261030T005726Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:26.896567+00:00 | 2026-10-30T01:03:21.017552+00:00 | 354.1210 | raw_results.json |
| `20261030T005726Z_h8e02_phishing_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:26.741243+00:00 | 2026-10-30T00:59:00.870708+00:00 | 94.1290 | raw_results.json |
| `20261030T005726Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:26.945727+00:00 | 2026-10-30T01:03:20.093021+00:00 | 353.1470 | raw_results.json |
| `20261030T005726Z_h8e02_higgs_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:26.922351+00:00 | 2026-10-30T01:00:08.700567+00:00 | 161.7780 | raw_results.json |
| `20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:28.638998+00:00 | 2026-10-30T01:19:53.885062+00:00 | 1345.2460 | raw_results.json |
| `20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:27.220623+00:00 | 2026-10-30T01:04:14.896579+00:00 | 407.6760 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:27.258899+00:00 | 2026-10-30T01:03:23.844650+00:00 | 356.5860 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:27.427248+00:00 | 2026-10-30T01:03:29.774548+00:00 | 362.3470 | raw_results.json |
| `20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:27.466868+00:00 | 2026-10-30T01:04:24.861783+00:00 | 417.3950 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:27.436074+00:00 | 2026-10-30T01:00:17.450748+00:00 | 170.0150 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:27.580797+00:00 | 2026-10-30T01:00:15.833407+00:00 | 168.2530 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:27.657368+00:00 | 2026-10-30T01:00:12.129604+00:00 | 164.4720 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:27.517220+00:00 | 2026-10-30T01:00:17.409087+00:00 | 169.8920 | raw_results.json |
| `20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:27.627222+00:00 | 2026-10-30T00:59:03.236946+00:00 | 95.6100 | raw_results.json |
| `20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:27.777302+00:00 | 2026-10-30T01:04:41.737613+00:00 | 433.9600 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:27.686560+00:00 | 2026-10-30T01:00:14.740044+00:00 | 167.0540 | raw_results.json |
| `20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:27.860331+00:00 | 2026-10-30T00:58:16.209298+00:00 | 48.3490 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:27.824490+00:00 | 2026-10-30T01:00:10.898576+00:00 | 163.0740 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:27.854234+00:00 | 2026-10-30T01:03:34.255385+00:00 | 366.4010 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:27.822311+00:00 | 2026-10-30T01:00:11.300624+00:00 | 163.4780 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:27.864911+00:00 | 2026-10-30T01:03:26.620820+00:00 | 358.7560 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:27.834061+00:00 | 2026-10-30T01:00:13.214938+00:00 | 165.3810 | raw_results.json |
| `20261030T005727Z_h8e02_har_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:27.895062+00:00 | 2026-10-30T01:04:00.629424+00:00 | 392.7340 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:27.861419+00:00 | 2026-10-30T01:03:29.924707+00:00 | 362.0630 | raw_results.json |
| `20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:27.914049+00:00 | 2026-10-30T01:04:04.226415+00:00 | 396.3120 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:27.854731+00:00 | 2026-10-30T01:03:23.875555+00:00 | 356.0210 | raw_results.json |
| `20261030T005728Z_h8e02_diabetes130_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:28.174086+00:00 | 2026-10-30T01:03:24.527856+00:00 | 356.3540 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:27.825662+00:00 | 2026-10-30T01:00:14.948433+00:00 | 167.1230 | raw_results.json |
| `20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:27.807262+00:00 | 2026-10-30T00:59:01.090620+00:00 | 93.2830 | raw_results.json |
| `20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:27.906545+00:00 | 2026-10-30T01:04:19.306221+00:00 | 411.4000 | raw_results.json |
| `20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:28.678497+00:00 | 2026-10-30T01:00:11.248658+00:00 | 162.5700 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:28.196419+00:00 | 2026-10-30T01:09:42.630817+00:00 | 734.4340 | raw_results.json |
| `20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:28.699714+00:00 | 2026-10-30T01:00:14.513474+00:00 | 165.8140 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:27.905957+00:00 | 2026-10-30T01:00:19.718642+00:00 | 171.8130 | raw_results.json |
| `20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.822200+00:00 | 2026-10-30T01:00:59.715574+00:00 | 210.8930 | raw_results.json |
| `20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:27.924162+00:00 | 2026-10-30T00:58:17.325363+00:00 | 49.4010 | raw_results.json |
| `20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:27.946131+00:00 | 2026-10-30T00:58:16.345122+00:00 | 48.3990 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:27.895455+00:00 | 2026-10-30T01:00:07.927967+00:00 | 160.0330 | raw_results.json |
| `20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:27.920760+00:00 | 2026-10-30T01:03:28.427477+00:00 | 360.5070 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:27.894624+00:00 | 2026-10-30T01:00:14.544963+00:00 | 166.6500 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:27.965232+00:00 | 2026-10-30T01:00:12.018015+00:00 | 164.0530 | raw_results.json |
| `20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:27.961810+00:00 | 2026-10-30T00:58:17.640909+00:00 | 49.6790 | raw_results.json |
| `20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:27.949456+00:00 | 2026-10-30T00:58:18.429183+00:00 | 50.4800 | raw_results.json |
| `20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:27.981405+00:00 | 2026-10-30T01:00:19.628312+00:00 | 171.6470 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:28.330784+00:00 | 2026-10-30T00:59:22.866581+00:00 | 114.5360 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:28.423747+00:00 | 2026-10-30T01:09:35.123945+00:00 | 726.7000 | raw_results.json |
| `20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:27.967243+00:00 | 2026-10-30T00:59:04.704988+00:00 | 96.7380 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:28.415045+00:00 | 2026-10-30T01:09:34.767137+00:00 | 726.3520 | raw_results.json |
| `20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:27.993943+00:00 | 2026-10-30T00:59:01.604188+00:00 | 93.6100 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.424220+00:00 | 2026-10-30T01:14:44.791437+00:00 | 1036.3670 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:28.459011+00:00 | 2026-10-30T01:10:48.575647+00:00 | 800.1170 | raw_results.json |
| `20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:28.214126+00:00 | 2026-10-30T00:58:44.284713+00:00 | 76.0710 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:28.049422+00:00 | 2026-10-30T00:59:02.291536+00:00 | 94.2420 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:28.046425+00:00 | 2026-10-30T00:58:46.052044+00:00 | 78.0060 | raw_results.json |
| `20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:28.213581+00:00 | 2026-10-30T00:58:57.418095+00:00 | 89.2050 | raw_results.json |
| `20261030T005728Z_h8e02_spambase_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:28.360789+00:00 | 2026-10-30T00:59:29.991507+00:00 | 121.6310 | raw_results.json |
| `20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:28.212766+00:00 | 2026-10-30T00:58:23.432007+00:00 | 55.2190 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:28.662044+00:00 | 2026-10-30T01:10:46.943462+00:00 | 798.2810 | raw_results.json |
| `20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:28.212348+00:00 | 2026-10-30T00:58:19.506046+00:00 | 51.2940 | raw_results.json |
| `20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:28.211643+00:00 | 2026-10-30T00:58:20.945848+00:00 | 52.7340 | raw_results.json |
| `20261030T005728Z_h8e02_har_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:28.974289+00:00 | 2026-10-30T01:08:21.466195+00:00 | 652.4920 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:28.173992+00:00 | 2026-10-30T00:58:59.743835+00:00 | 91.5700 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:28.200438+00:00 | 2026-10-30T00:59:00.339068+00:00 | 92.1390 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:28.197528+00:00 | 2026-10-30T00:58:46.051189+00:00 | 77.8540 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:28.198607+00:00 | 2026-10-30T00:58:47.587964+00:00 | 79.3890 | raw_results.json |
| `20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:28.578380+00:00 | 2026-10-30T01:00:06.810869+00:00 | 158.2330 | raw_results.json |
| `20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:28.577896+00:00 | 2026-10-30T01:00:11.643055+00:00 | 163.0650 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:28.201177+00:00 | 2026-10-30T00:59:21.827155+00:00 | 113.6260 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:28.199800+00:00 | 2026-10-30T00:59:05.990464+00:00 | 97.7910 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:28.577383+00:00 | 2026-10-30T01:05:39.556877+00:00 | 490.9800 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:28.198091+00:00 | 2026-10-30T00:58:46.049152+00:00 | 77.8510 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:28.196415+00:00 | 2026-10-30T00:59:02.662568+00:00 | 94.4660 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:28.646577+00:00 | 2026-10-30T00:58:47.620443+00:00 | 78.9740 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:28.975242+00:00 | 2026-10-30T01:10:08.322013+00:00 | 759.3470 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:28.673081+00:00 | 2026-10-30T01:12:36.670205+00:00 | 907.9970 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:29.328279+00:00 | 2026-10-30T01:10:09.540877+00:00 | 760.2130 | raw_results.json |
| `20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:28.889672+00:00 | 2026-10-30T00:58:54.575374+00:00 | 85.6860 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:28.801108+00:00 | 2026-10-30T01:05:34.631271+00:00 | 485.8300 | raw_results.json |
| `20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:29.452905+00:00 | 2026-10-30T01:00:52.367432+00:00 | 202.9150 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.425978+00:00 | 2026-10-30T00:58:44.284805+00:00 | 75.8590 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:28.416687+00:00 | 2026-10-30T00:58:44.288011+00:00 | 75.8710 | raw_results.json |
| `20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:29.395118+00:00 | 2026-10-30T01:00:49.270376+00:00 | 199.8750 | raw_results.json |
| `20261030T005729Z_h8e02_adult_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:29.414421+00:00 | 2026-10-30T01:00:54.794416+00:00 | 205.3800 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:28.428668+00:00 | 2026-10-30T00:59:03.853051+00:00 | 95.4240 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.455813+00:00 | 2026-10-30T00:59:02.235430+00:00 | 93.7800 | raw_results.json |
| `20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:29.143954+00:00 | 2026-10-30T01:01:14.257814+00:00 | 225.1140 | raw_results.json |
| `20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:29.143400+00:00 | 2026-10-30T01:01:10.382239+00:00 | 221.2390 | raw_results.json |
| `20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:28.416264+00:00 | 2026-10-30T00:59:03.644000+00:00 | 95.2280 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:28.428111+00:00 | 2026-10-30T00:58:44.283122+00:00 | 75.8550 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:28.423368+00:00 | 2026-10-30T00:58:47.618599+00:00 | 79.1950 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:28.417890+00:00 | 2026-10-30T00:58:49.814844+00:00 | 81.3970 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:28.427493+00:00 | 2026-10-30T00:58:51.804742+00:00 | 83.3770 | raw_results.json |
| `20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:28.450152+00:00 | 2026-10-30T00:59:22.468747+00:00 | 114.0190 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:28.667278+00:00 | 2026-10-30T01:09:17.064296+00:00 | 708.3970 | raw_results.json |
| `20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.894914+00:00 | 2026-10-30T00:58:55.794052+00:00 | 86.8990 | raw_results.json |
| `20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:28.890415+00:00 | 2026-10-30T00:58:58.349272+00:00 | 89.4590 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:29.329063+00:00 | 2026-10-30T01:09:25.133422+00:00 | 715.8040 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:28.916698+00:00 | 2026-10-30T01:13:15.289547+00:00 | 946.3730 | raw_results.json |
| `20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:28.974155+00:00 | 2026-10-30T00:58:58.172602+00:00 | 89.1980 | raw_results.json |
| `20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:28.974191+00:00 | 2026-10-30T01:10:28.451343+00:00 | 779.4770 | raw_results.json |
| `20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:29.143461+00:00 | 2026-10-30T01:00:15.196573+00:00 | 166.0530 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:29.634802+00:00 | 2026-10-30T01:13:22.951789+00:00 | 953.3170 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:29.335962+00:00 | 2026-10-30T01:07:37.918002+00:00 | 608.5820 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:29.335801+00:00 | 2026-10-30T01:09:35.162475+00:00 | 725.8270 | raw_results.json |
| `20261030T005729Z_h8e02_heloc_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:29.143332+00:00 | 2026-10-30T00:59:24.056175+00:00 | 114.9130 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:29.910145+00:00 | 2026-10-30T01:18:11.354917+00:00 | 1241.4450 | raw_results.json |
| `20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:29.396296+00:00 | 2026-10-30T00:58:23.371626+00:00 | 53.9750 | raw_results.json |
| `20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:29.434187+00:00 | 2026-10-30T00:58:21.299273+00:00 | 51.8650 | raw_results.json |
| `20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:29.328476+00:00 | 2026-10-30T01:01:02.454017+00:00 | 213.1260 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:29.789084+00:00 | 2026-10-30T01:08:24.575316+00:00 | 654.7860 | raw_results.json |
| `20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:28.776648+00:00 | 2026-10-30T00:58:13.028970+00:00 | 44.2520 | raw_results.json |
| `20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:28.775601+00:00 | 2026-10-30T00:58:00.810033+00:00 | 32.0340 | raw_results.json |
| `20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:29.559704+00:00 | 2026-10-30T01:10:23.129426+00:00 | 773.5700 | raw_results.json |
| `20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:28.777024+00:00 | 2026-10-30T00:58:01.595782+00:00 | 32.8190 | raw_results.json |
| `20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:28.778205+00:00 | 2026-10-30T00:58:13.172782+00:00 | 44.3950 | raw_results.json |
| `20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:28.776245+00:00 | 2026-10-30T00:58:13.924943+00:00 | 45.1490 | raw_results.json |
| `20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:28.777597+00:00 | 2026-10-30T00:58:01.903205+00:00 | 33.1260 | raw_results.json |
| `20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:28.779174+00:00 | 2026-10-30T00:58:01.870881+00:00 | 33.0920 | raw_results.json |
| `20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:29.705014+00:00 | 2026-10-30T00:58:23.821006+00:00 | 54.1160 | raw_results.json |
| `20261030T005729Z_h8e02_spambase_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:29.108285+00:00 | 2026-10-30T00:58:58.504361+00:00 | 89.3960 | raw_results.json |
| `20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:29.328392+00:00 | 2026-10-30T00:58:51.235826+00:00 | 81.9070 | raw_results.json |
| `20261030T005730Z_h8e02_adult_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:30.354660+00:00 | 2026-10-30T01:02:58.240252+00:00 | 327.8860 | raw_results.json |
| `20261030T005730Z_h8e02_phishing_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:30.354442+00:00 | 2026-10-30T00:59:04.168328+00:00 | 93.8140 | raw_results.json |
| `20261030T005729Z_h8e02_gas_drift_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:29.705092+00:00 | 2026-10-30T01:11:07.922623+00:00 | 818.2180 | raw_results.json |
| `20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:29.783902+00:00 | 2026-10-30T00:58:55.725816+00:00 | 85.9420 | raw_results.json |
| `20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:30.038030+00:00 | 2026-10-30T01:01:20.218353+00:00 | 230.1800 | raw_results.json |
| `20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:29.356997+00:00 | 2026-10-30T00:58:13.690226+00:00 | 44.3330 | raw_results.json |
| `20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:30.003716+00:00 | 2026-10-30T01:01:10.527964+00:00 | 220.5240 | raw_results.json |
| `20261030T005729Z_h8e02_pc4_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:29.475351+00:00 | 2026-10-30T00:58:04.671892+00:00 | 35.1970 | raw_results.json |
| `20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:29.994495+00:00 | 2026-10-30T00:58:54.541923+00:00 | 84.5470 | raw_results.json |
| `20261030T005731Z_h8e02_spambase_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:31.491324+00:00 | 2026-10-30T00:58:55.452167+00:00 | 83.9610 | raw_results.json |
| `20261030T005731Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:57:31.661323+00:00 | 2026-10-30T00:59:15.458454+00:00 | 103.7970 | raw_results.json |
| `20261030T005731Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:31.813264+00:00 | 2026-10-30T01:10:41.925066+00:00 | 790.1120 | raw_results.json |
| `20261030T005731Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:57:31.984784+00:00 | 2026-10-30T00:58:46.048132+00:00 | 74.0630 | raw_results.json |
| `20261030T005732Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:57:32.065501+00:00 | 2026-10-30T00:58:39.925598+00:00 | 67.8600 | raw_results.json |
| `20261030T005732Z_h8e02_spambase_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:32.027482+00:00 | 2026-10-30T00:58:54.578727+00:00 | 82.5510 | raw_results.json |
| `20261030T005734Z_h8e02_spambase_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:34.237502+00:00 | 2026-10-30T00:59:02.821899+00:00 | 88.5840 | raw_results.json |
| `20261030T005734Z_h8e02_phishing_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:34.395457+00:00 | 2026-10-30T00:59:08.035178+00:00 | 93.6400 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:57:35.074772+00:00 | 2026-10-30T00:59:10.027485+00:00 | 94.9530 | raw_results.json |
| `20261030T005735Z_h8e02_spambase_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:35.386155+00:00 | 2026-10-30T00:59:01.074123+00:00 | 85.6880 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:57:35.427222+00:00 | 2026-10-30T00:58:47.626929+00:00 | 72.2000 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:57:35.424221+00:00 | 2026-10-30T00:58:46.011924+00:00 | 70.5880 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:57:35.424775+00:00 | 2026-10-30T00:58:49.832366+00:00 | 74.4080 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:57:35.438985+00:00 | 2026-10-30T00:58:47.564910+00:00 | 72.1260 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:57:35.456865+00:00 | 2026-10-30T00:58:53.125635+00:00 | 77.6690 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:57:35.198730+00:00 | 2026-10-30T00:59:12.433672+00:00 | 97.2350 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:57:35.316582+00:00 | 2026-10-30T00:59:23.546337+00:00 | 108.2300 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:57:35.251826+00:00 | 2026-10-30T00:59:21.411681+00:00 | 106.1600 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:57:35.209769+00:00 | 2026-10-30T00:59:23.306178+00:00 | 108.0960 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:57:35.400364+00:00 | 2026-10-30T00:59:23.621467+00:00 | 108.2210 | raw_results.json |
| `20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:57:35.243438+00:00 | 2026-10-30T00:59:21.033882+00:00 | 105.7900 | raw_results.json |
| `20261030T005812Z_h8e02_pc4_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:58:12.918972+00:00 | 2026-10-30T00:58:58.170763+00:00 | 45.2520 | raw_results.json |
| `20261030T005813Z_h8e02_pc4_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:58:13.534714+00:00 | 2026-10-30T00:58:59.164641+00:00 | 45.6300 | raw_results.json |
| `20261030T005814Z_h8e02_pc4_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:58:14.952250+00:00 | 2026-10-30T00:59:30.216238+00:00 | 75.2640 | raw_results.json |
| `20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:58:15.606794+00:00 | 2026-10-30T01:00:17.330327+00:00 | 121.7240 | raw_results.json |
| `20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:58:15.811634+00:00 | 2026-10-30T00:59:03.420532+00:00 | 47.6090 | raw_results.json |
| `20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:58:26.242669+00:00 | 2026-10-30T00:59:40.700692+00:00 | 74.4580 | raw_results.json |
| `20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:58:26.271353+00:00 | 2026-10-30T00:59:38.890055+00:00 | 72.6190 | raw_results.json |
| `20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:58:26.272792+00:00 | 2026-10-30T00:59:15.102470+00:00 | 48.8300 | raw_results.json |
| `20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:58:26.867471+00:00 | 2026-10-30T00:59:12.827117+00:00 | 45.9600 | raw_results.json |
| `20261030T005828Z_h8e02_pc4_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:58:28.484206+00:00 | 2026-10-30T00:59:44.187350+00:00 | 75.7030 | raw_results.json |
| `20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:58:28.485853+00:00 | 2026-10-30T01:02:38.350864+00:00 | 249.8650 | raw_results.json |
| `20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:58:28.484322+00:00 | 2026-10-30T01:02:42.016822+00:00 | 253.5330 | raw_results.json |
| `20261030T005829Z_h8e02_mice_protein_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:58:30.524676+00:00 | 2026-10-30T01:02:43.738030+00:00 | 253.2130 | raw_results.json |
| `20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:58:32.684929+00:00 | 2026-10-30T01:05:43.770335+00:00 | 431.0850 | raw_results.json |
| `20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:58:32.684886+00:00 | 2026-10-30T01:02:45.408286+00:00 | 252.7230 | raw_results.json |
| `20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:58:34.721852+00:00 | 2026-10-30T01:02:52.251240+00:00 | 257.5290 | raw_results.json |
| `20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:58:34.723160+00:00 | 2026-10-30T01:02:45.486087+00:00 | 250.7630 | raw_results.json |
| `20261030T005834Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:58:34.724317+00:00 | 2026-10-30T01:02:45.737414+00:00 | 251.0130 | raw_results.json |
| `20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:58:40.025015+00:00 | 2026-10-30T01:02:54.777926+00:00 | 254.7530 | raw_results.json |
| `20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:58:39.799287+00:00 | 2026-10-30T01:02:48.149455+00:00 | 248.3500 | raw_results.json |
| `20261030T005855Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2020` | ok | 2026-10-30T00:58:55.286661+00:00 | 2026-10-30T01:03:02.030532+00:00 | 246.7440 | raw_results.json |
| `20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:58:58.528075+00:00 | 2026-10-30T01:02:53.582643+00:00 | 235.0550 | raw_results.json |
| `20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:58:58.691666+00:00 | 2026-10-30T01:02:51.090872+00:00 | 232.3990 | raw_results.json |
| `20261030T005858Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2020` | ok | 2026-10-30T00:58:58.826019+00:00 | 2026-10-30T00:59:37.202220+00:00 | 38.3760 | raw_results.json |
| `20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:58:58.836994+00:00 | 2026-10-30T01:02:55.816418+00:00 | 236.9790 | raw_results.json |
| `20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:58:58.845896+00:00 | 2026-10-30T01:02:56.542958+00:00 | 237.6970 | raw_results.json |
| `20261030T005900Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2021` | ok | 2026-10-30T00:59:00.452932+00:00 | 2026-10-30T01:00:11.639665+00:00 | 71.1870 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2022` | ok | 2026-10-30T00:59:02.172327+00:00 | 2026-10-30T01:00:00.204776+00:00 | 58.0320 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2024` | ok | 2026-10-30T00:59:02.150927+00:00 | 2026-10-30T00:59:38.056698+00:00 | 35.9060 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2021` | ok | 2026-10-30T00:59:02.245910+00:00 | 2026-10-30T00:59:39.931694+00:00 | 37.6860 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2023` | ok | 2026-10-30T00:59:02.265691+00:00 | 2026-10-30T00:59:39.774619+00:00 | 37.5090 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2022` | ok | 2026-10-30T00:59:02.313842+00:00 | 2026-10-30T00:59:40.735714+00:00 | 38.4220 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2023` | ok | 2026-10-30T00:59:02.922501+00:00 | 2026-10-30T01:00:09.941763+00:00 | 67.0190 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2020` | ok | 2026-10-30T00:59:02.327979+00:00 | 2026-10-30T01:00:02.452368+00:00 | 60.1240 | raw_results.json |
| `20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2024` | ok | 2026-10-30T00:59:02.431843+00:00 | 2026-10-30T01:00:08.435971+00:00 | 66.0040 | raw_results.json |
| `20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2023` | ok | 2026-10-30T00:59:06.314778+00:00 | 2026-10-30T00:59:44.445956+00:00 | 38.1310 | raw_results.json |
| `20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2024` | ok | 2026-10-30T00:59:06.632880+00:00 | 2026-10-30T01:00:05.904631+00:00 | 59.2720 | raw_results.json |
| `20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2022` | ok | 2026-10-30T00:59:06.751989+00:00 | 2026-10-30T01:00:11.904245+00:00 | 65.1520 | raw_results.json |
| `20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2021` | ok | 2026-10-30T00:59:06.820873+00:00 | 2026-10-30T00:59:46.590226+00:00 | 39.7690 | raw_results.json |

Run keys (240; full list in [tables/run_keys.csv](tables/run_keys.csv)):

| dataset | arm | seed | AUF K=10 | AUF K=20 | hypervolume | min subset | fits | seconds | stopped on |
|---|---|---|---|---|---|---|---|---|---|
| qsar_biodeg | fastener_llm_haiku_blind | 2020 | 0.8381 | 0.8536 | 34.4539 | 1 | 1000 | 65.3900 | "fit_budget" |
| crop_mapping | fastener_llm_sonnet_blind | 2022 | 0.9202 | 0.9553 | 171.0482 | 1 | 1000 | 1003.9300 | "fit_budget" |
| eodata | fastener_llm_opus_blind | 2022 | 0.5617 | 0.6248 | 126.2025 | 1 | 1000 | 3261.4900 | "fit_budget" |
| diabetes130 | fastener_llm_sonnet_blind | 2020 | 0.5187 | 0.5245 | 69.5873 | 1 | 1000 | 357.0800 | "fit_budget" |
| eodata | fastener_llm_opus_blind | 2021 | 0.5433 | 0.6145 | 127.3171 | 1 | 1000 | 4499.7400 | "fit_budget" |
| eodata | fastener_llm_opus_blind | 2020 | 0.5601 | 0.6274 | 128.0513 | 1 | 1000 | 4501.7000 | "fit_budget" |
| covertype | fastener_llm_opus_blind | 2020 | 0.7747 | 0.8029 | 43.5809 | 1 | 1000 | 825.1100 | "fit_budget" |
| eodata | fastener_llm_opus_blind | 2024 | 0.5602 | 0.6262 | 127.1312 | 1 | 1000 | 4442.3500 | "fit_budget" |
| covertype | fastener_llm_haiku_blind | 2021 | 0.7749 | 0.8029 | 43.5621 | 1 | 1000 | 1342.6600 | "fit_budget" |
| covertype | fastener_llm_haiku_blind | 2023 | 0.7754 | 0.8033 | 43.5604 | 1 | 1000 | 1161.2700 | "fit_budget" |
| crop_mapping | fastener_llm_haiku_blind | 2021 | 0.9249 | 0.9586 | 171.1058 | 1 | 1000 | 1084.4700 | "fit_budget" |
| crop_mapping | fastener_llm_opus_blind | 2024 | 0.9215 | 0.9563 | 170.9848 | 1 | 1000 | 1340.5800 | "fit_budget" |
| crop_mapping | fastener_llm_haiku_blind | 2020 | 0.9238 | 0.9578 | 171.0948 | 1 | 1000 | 1458.3400 | "fit_budget" |
| crop_mapping | fastener_llm_haiku_blind | 2022 | 0.9194 | 0.9549 | 171.0749 | 1 | 1000 | 1174.1200 | "fit_budget" |
| crop_mapping | fastener_llm_opus_blind | 2022 | 0.9209 | 0.9559 | 170.8548 | 1 | 1000 | 1316.8100 | "fit_budget" |
| crop_mapping | fastener_llm_opus_blind | 2021 | 0.9223 | 0.9568 | 170.9295 | 1 | 1000 | 1189.4600 | "fit_budget" |
| crop_mapping | fastener_llm_opus_blind | 2023 | 0.9202 | 0.9551 | 170.9152 | 1 | 1000 | 1733.4000 | "fit_budget" |
| eodata | fastener_llm_sonnet_blind | 2024 | 0.5500 | 0.6176 | 126.4742 | 1 | 1000 | 3384.2900 | "fit_budget" |
| crop_mapping | fastener_llm_haiku_blind | 2023 | 0.9274 | 0.9590 | 170.9807 | 1 | 1000 | 1407.6100 | "fit_budget" |
| eodata | fastener_llm_sonnet_blind | 2021 | 0.5632 | 0.6279 | 127.3590 | 1 | 1000 | 3408.3500 | "fit_budget" |
| eodata | fastener_llm_opus_blind | 2023 | 0.5468 | 0.6168 | 126.8411 | 1 | 1000 | 3101.5000 | "fit_budget" |
| covertype | fastener_llm_haiku_blind | 2022 | 0.7731 | 0.8016 | 43.5647 | 1 | 1000 | 1171.3300 | "fit_budget" |
| crop_mapping | fastener_llm_sonnet_blind | 2024 | 0.9198 | 0.9558 | 170.9254 | 1 | 1000 | 1286.3400 | "fit_budget" |
| crop_mapping | fastener_llm_sonnet_blind | 2021 | 0.9249 | 0.9582 | 170.9114 | 1 | 1000 | 1617.1300 | "fit_budget" |
| eodata | fastener_llm_haiku_blind | 2021 | 0.5640 | 0.6277 | 127.6212 | 1 | 1000 | 3156.9300 | "fit_budget" |
| covertype | fastener_llm_opus_blind | 2023 | 0.7725 | 0.8024 | 43.6830 | 1 | 1000 | 845.1000 | "fit_budget" |
| covertype | fastener_llm_haiku_blind | 2020 | 0.7736 | 0.8008 | 43.4090 | 1 | 1000 | 1180.2100 | "fit_budget" |
| eodata | fastener_llm_sonnet_blind | 2023 | 0.5642 | 0.6285 | 127.3744 | 1 | 1000 | 3196.9700 | "fit_budget" |
| diabetes130 | fastener_llm_opus_blind | 2023 | 0.5207 | 0.5255 | 69.3815 | 1 | 1000 | 557.5800 | "fit_budget" |
| covertype | fastener_llm_sonnet_blind | 2021 | 0.7733 | 0.8021 | 43.5504 | 1 | 1000 | 836.1100 | "fit_budget" |
| covertype | fastener_llm_opus_blind | 2021 | 0.7734 | 0.8018 | 43.4939 | 1 | 1000 | 862.6200 | "fit_budget" |
| eodata | fastener_llm_haiku_blind | 2023 | 0.5541 | 0.6221 | 126.2461 | 1 | 1000 | 3005.3100 | "fit_budget" |
| eodata | fastener_llm_sonnet_blind | 2022 | 0.5613 | 0.6255 | 126.5552 | 1 | 1000 | 4418.8100 | "fit_budget" |
| covertype | fastener_llm_opus_blind | 2022 | 0.7728 | 0.8005 | 43.4840 | 1 | 1000 | 806.9700 | "fit_budget" |
| eodata | fastener_llm_haiku_blind | 2022 | 0.5592 | 0.6253 | 127.2718 | 1 | 1000 | 3199.1600 | "fit_budget" |
| eodata | fastener_llm_sonnet_blind | 2020 | 0.5641 | 0.6273 | 126.9237 | 1 | 1000 | 3187.2800 | "fit_budget" |
| eodata | fastener_llm_haiku_blind | 2024 | 0.5663 | 0.6272 | 126.8979 | 1 | 1000 | 3152.5600 | "fit_budget" |
| covertype | fastener_llm_sonnet_blind | 2022 | 0.7734 | 0.8012 | 43.4574 | 1 | 1000 | 828.3600 | "fit_budget" |
| covertype | fastener_llm_opus_blind | 2024 | 0.7739 | 0.8012 | 43.5186 | 1 | 1000 | 829.0700 | "fit_budget" |
| covertype | fastener_llm_sonnet_blind | 2020 | 0.7757 | 0.8007 | 43.2743 | 1 | 1000 | 815.0500 | "fit_budget" |
| eodata | fastener_llm_haiku_blind | 2020 | 0.5434 | 0.6207 | 127.0527 | 1 | 1000 | 3173.1300 | "fit_budget" |
| covertype | fastener_llm_haiku_blind | 2024 | 0.7747 | 0.8010 | 43.3679 | 1 | 1000 | 1072.0800 | "fit_budget" |
| crop_mapping | fastener_llm_haiku_blind | 2024 | 0.9207 | 0.9559 | 171.0916 | 1 | 1000 | 1413.3700 | "fit_budget" |
| covertype | fastener_llm_sonnet_blind | 2024 | 0.7759 | 0.8027 | 43.5061 | 1 | 1000 | 1488.9400 | "fit_budget" |
| covertype | fastener_llm_sonnet_blind | 2023 | 0.7758 | 0.8012 | 43.3553 | 1 | 1000 | 1265.9800 | "fit_budget" |
| crop_mapping | fastener_llm_opus_blind | 2020 | 0.9190 | 0.9550 | 170.9701 | 1 | 1000 | 1037.2000 | "fit_budget" |
| diabetes130 | fastener_llm_opus_blind | 2020 | 0.5187 | 0.5245 | 69.5873 | 1 | 1000 | 555.4900 | "fit_budget" |
| diabetes130 | fastener_llm_opus_blind | 2022 | 0.5193 | 0.5222 | 69.0044 | 1 | 1000 | 504.0300 | "fit_budget" |
| diabetes130 | fastener_llm_opus_blind | 2021 | 0.5219 | 0.5266 | 69.6979 | 1 | 1000 | 510.5500 | "fit_budget" |
| crop_mapping | fastener_llm_sonnet_blind | 2020 | 0.9181 | 0.9545 | 170.8983 | 1 | 1000 | 1017.3300 | "fit_budget" |
| diabetes130 | fastener_llm_haiku_blind | 2023 | 0.5207 | 0.5255 | 69.3815 | 1 | 1000 | 348.3800 | "fit_budget" |
| phishing | fastener_llm_opus_blind | 2020 | 0.9276 | 0.9392 | 27.3798 | 1 | 1000 | 91.8100 | "fit_budget" |
| diabetes130 | fastener_llm_sonnet_blind | 2023 | 0.5207 | 0.5255 | 69.3815 | 1 | 1000 | 347.4300 | "fit_budget" |
| higgs | fastener_llm_haiku_blind | 2024 | 0.6873 | 0.7024 | 19.0738 | 1 | 1000 | 158.0000 | "fit_budget" |
| crop_mapping | fastener_llm_sonnet_blind | 2023 | 0.9221 | 0.9563 | 170.7802 | 1 | 1000 | 1326.4000 | "fit_budget" |
| har | fastener_llm_opus_blind | 2021 | 0.8957 | 0.9369 | 547.9939 | 1 | 1000 | 399.9900 | "fit_budget" |
| diabetes130 | fastener_llm_sonnet_blind | 2022 | 0.5193 | 0.5222 | 69.0044 | 1 | 1000 | 352.3500 | "fit_budget" |
| diabetes130 | fastener_llm_haiku_blind | 2021 | 0.5219 | 0.5266 | 69.6979 | 1 | 1000 | 356.4400 | "fit_budget" |
| har | fastener_llm_opus_blind | 2020 | 0.8998 | 0.9364 | 546.6632 | 1 | 1000 | 410.8800 | "fit_budget" |
| higgs | fastener_llm_sonnet_blind | 2024 | 0.6862 | 0.7015 | 19.0872 | 1 | 1000 | 166.4700 | "fit_budget" |
| higgs | fastener_llm_opus_blind | 2020 | 0.6878 | 0.7020 | 19.0736 | 1 | 1000 | 165.0100 | "fit_budget" |
| higgs | fastener_llm_opus_blind | 2021 | 0.6879 | 0.7016 | 19.0846 | 1 | 1000 | 161.1300 | "fit_budget" |
| higgs | fastener_llm_haiku_blind | 2022 | 0.6873 | 0.7038 | 19.1202 | 1 | 1000 | 166.4600 | "fit_budget" |
| phishing | fastener_llm_sonnet_blind | 2024 | 0.9277 | 0.9422 | 27.4607 | 1 | 1000 | 93.1900 | "fit_budget" |
| har | fastener_llm_opus_blind | 2023 | 0.8974 | 0.9368 | 549.6105 | 1 | 1000 | 426.3200 | "fit_budget" |
| higgs | fastener_llm_sonnet_blind | 2020 | 0.6869 | 0.7016 | 19.0487 | 1 | 1000 | 163.5600 | "fit_budget" |
| ozone_8hr | fastener_llm_opus_blind | 2024 | 0.9147 | 0.9139 | 65.4004 | 1 | 1000 | 46.6200 | "fit_budget" |
| higgs | fastener_llm_opus_blind | 2022 | 0.6867 | 0.7007 | 19.0181 | 1 | 1000 | 160.0100 | "fit_budget" |
| diabetes130 | fastener_llm_haiku_blind | 2020 | 0.5187 | 0.5245 | 69.5873 | 1 | 1000 | 361.1700 | "fit_budget" |
| higgs | fastener_llm_haiku_blind | 2023 | 0.6870 | 0.7009 | 19.0215 | 1 | 1000 | 160.4400 | "fit_budget" |
| diabetes130 | fastener_llm_haiku_blind | 2024 | 0.5203 | 0.5239 | 69.2737 | 1 | 1000 | 354.1400 | "fit_budget" |
| higgs | fastener_llm_opus_blind | 2024 | 0.6875 | 0.7033 | 19.1317 | 1 | 1000 | 161.5500 | "fit_budget" |
| har | fastener_llm_sonnet_blind | 2020 | 0.9027 | 0.9403 | 547.2743 | 1 | 1000 | 386.6300 | "fit_budget" |
| diabetes130 | fastener_llm_sonnet_blind | 2021 | 0.5219 | 0.5266 | 69.6979 | 1 | 1000 | 356.1600 | "fit_budget" |
| har | fastener_llm_opus_blind | 2022 | 0.8844 | 0.9308 | 547.3505 | 1 | 1000 | 389.5100 | "fit_budget" |
| diabetes130 | fastener_llm_haiku_blind | 2022 | 0.5193 | 0.5222 | 69.0044 | 1 | 1000 | 351.8500 | "fit_budget" |
| diabetes130 | fastener_llm_opus_blind | 2024 | 0.5203 | 0.5239 | 69.2737 | 1 | 1000 | 351.5200 | "fit_budget" |
| higgs | fastener_llm_sonnet_blind | 2021 | 0.6869 | 0.6996 | 19.0370 | 1 | 1000 | 164.1100 | "fit_budget" |
| phishing | fastener_llm_opus_blind | 2021 | 0.9270 | 0.9419 | 27.4787 | 1 | 1000 | 90.8800 | "fit_budget" |
| har | fastener_llm_opus_blind | 2024 | 0.9037 | 0.9395 | 549.3623 | 1 | 1000 | 401.8300 | "fit_budget" |
| adult | fastener_llm_sonnet_blind | 2021 | 0.8362 | 0.8493 | 53.2774 | 1 | 1000 | 158.7600 | "fit_budget" |
| gas_drift | fastener_llm_sonnet_blind | 2020 | 0.9235 | 0.9584 | 125.4788 | 1 | 1000 | 724.3300 | "fit_budget" |
| adult | fastener_llm_sonnet_blind | 2022 | 0.8379 | 0.8496 | 53.1939 | 1 | 1000 | 161.5300 | "fit_budget" |
| higgs | fastener_llm_sonnet_blind | 2023 | 0.6869 | 0.7017 | 19.0744 | 1 | 1000 | 168.4600 | "fit_budget" |
| adult | fastener_llm_haiku_blind | 2021 | 0.8390 | 0.8507 | 53.2626 | 1 | 1000 | 206.0800 | "fit_budget" |
| ozone_8hr | fastener_llm_sonnet_blind | 2022 | 0.9134 | 0.9156 | 65.3234 | 1 | 1000 | 47.6100 | "fit_budget" |
| ozone_8hr | fastener_llm_sonnet_blind | 2020 | 0.9164 | 0.9180 | 65.4908 | 1 | 1000 | 46.6300 | "fit_budget" |
| higgs | fastener_llm_sonnet_blind | 2022 | 0.6878 | 0.7009 | 19.0779 | 1 | 1000 | 156.8000 | "fit_budget" |
| diabetes130 | fastener_llm_sonnet_blind | 2024 | 0.5203 | 0.5239 | 69.2737 | 1 | 1000 | 355.7800 | "fit_budget" |
| higgs | fastener_llm_opus_blind | 2023 | 0.6869 | 0.7024 | 19.0744 | 1 | 1000 | 163.6400 | "fit_budget" |
| higgs | fastener_llm_haiku_blind | 2020 | 0.6872 | 0.7016 | 19.0723 | 1 | 1000 | 160.6000 | "fit_budget" |
| ozone_8hr | fastener_llm_opus_blind | 2023 | 0.9158 | 0.9170 | 65.7328 | 1 | 1000 | 47.7600 | "fit_budget" |
| ozone_8hr | fastener_llm_sonnet_blind | 2021 | 0.9146 | 0.9149 | 65.4032 | 1 | 1000 | 48.4800 | "fit_budget" |
| higgs | fastener_llm_haiku_blind | 2021 | 0.6876 | 0.7023 | 19.1018 | 1 | 1000 | 168.4500 | "fit_budget" |
| heloc | fastener_llm_opus_blind | 2021 | 0.7019 | 0.7058 | 14.8314 | 1 | 1000 | 112.0700 | "fit_budget" |
| gas_drift | fastener_llm_sonnet_blind | 2022 | 0.9235 | 0.9582 | 125.6040 | 1 | 1000 | 715.8800 | "fit_budget" |
| phishing | fastener_llm_sonnet_blind | 2020 | 0.9276 | 0.9413 | 27.4507 | 1 | 1000 | 94.2800 | "fit_budget" |
| gas_drift | fastener_llm_haiku_blind | 2024 | 0.9181 | 0.9555 | 125.4258 | 1 | 1000 | 716.1000 | "fit_budget" |
| phishing | fastener_llm_opus_blind | 2022 | 0.9281 | 0.9433 | 27.5082 | 1 | 1000 | 91.2000 | "fit_budget" |
| gas_drift | fastener_llm_haiku_blind | 2021 | 0.9176 | 0.9550 | 125.3351 | 1 | 1000 | 1022.5300 | "fit_budget" |
| gas_drift | fastener_llm_sonnet_blind | 2023 | 0.9199 | 0.9559 | 125.4771 | 1 | 1000 | 786.0800 | "fit_budget" |
| spambase | fastener_llm_sonnet_blind | 2023 | 0.8964 | 0.9093 | 51.7240 | 1 | 1000 | 72.0000 | "fit_budget" |
| phishing | fastener_llm_sonnet_blind | 2022 | 0.9267 | 0.9419 | 27.5142 | 1 | 1000 | 91.6000 | "fit_budget" |
| heloc | fastener_llm_sonnet_blind | 2024 | 0.7016 | 0.7061 | 14.8509 | 1 | 1000 | 73.7400 | "fit_budget" |
| spambase | fastener_llm_sonnet_blind | 2022 | 0.9004 | 0.9189 | 52.2905 | 1 | 1000 | 86.5800 | "fit_budget" |
| spambase | fastener_llm_opus_blind | 2024 | 0.9000 | 0.9180 | 52.1461 | 1 | 1000 | 118.7300 | "fit_budget" |
| ozone_8hr | fastener_llm_opus_blind | 2022 | 0.9154 | 0.9179 | 65.3545 | 1 | 1000 | 53.0100 | "fit_budget" |
| gas_drift | fastener_llm_haiku_blind | 2023 | 0.9183 | 0.9546 | 125.4098 | 1 | 1000 | 782.8100 | "fit_budget" |
| ozone_8hr | fastener_llm_opus_blind | 2021 | 0.9108 | 0.9126 | 64.9021 | 1 | 1000 | 49.2700 | "fit_budget" |
| ozone_8hr | fastener_llm_opus_blind | 2020 | 0.9203 | 0.9184 | 65.6912 | 1 | 1000 | 50.7500 | "fit_budget" |
| har | fastener_llm_haiku_blind | 2022 | 0.8834 | 0.9295 | 550.1064 | 1 | 1000 | 636.3900 | "fit_budget" |
| phishing | fastener_llm_opus_blind | 2023 | 0.9270 | 0.9418 | 27.4532 | 1 | 1000 | 89.1600 | "fit_budget" |
| phishing | fastener_llm_opus_blind | 2024 | 0.9267 | 0.9422 | 27.4832 | 1 | 1000 | 89.7000 | "fit_budget" |
| heloc | fastener_llm_sonnet_blind | 2022 | 0.7013 | 0.7055 | 14.8342 | 1 | 1000 | 71.8900 | "fit_budget" |
| heloc | fastener_llm_haiku_blind | 2024 | 0.7021 | 0.7054 | 14.8872 | 1 | 1000 | 76.2000 | "fit_budget" |
| adult | fastener_llm_haiku_blind | 2023 | 0.8386 | 0.8511 | 53.2917 | 1 | 1000 | 155.0000 | "fit_budget" |
| adult | fastener_llm_haiku_blind | 2024 | 0.8361 | 0.8491 | 53.2244 | 1 | 1000 | 159.1000 | "fit_budget" |
| heloc | fastener_llm_opus_blind | 2022 | 0.7023 | 0.7042 | 14.8502 | 1 | 1000 | 111.2500 | "fit_budget" |
| phishing | fastener_llm_sonnet_blind | 2023 | 0.9267 | 0.9421 | 27.4888 | 1 | 1000 | 95.3300 | "fit_budget" |
| gas_drift | fastener_llm_opus_blind | 2021 | 0.9177 | 0.9548 | 125.2939 | 1 | 1000 | 483.1900 | "fit_budget" |
| heloc | fastener_llm_haiku_blind | 2020 | 0.7043 | 0.7066 | 14.9061 | 1 | 1000 | 72.4600 | "fit_budget" |
| phishing | fastener_llm_sonnet_blind | 2021 | 0.9270 | 0.9368 | 27.3057 | 1 | 1000 | 92.0200 | "fit_budget" |
| heloc | fastener_llm_opus_blind | 2024 | 0.7007 | 0.7040 | 14.8233 | 1 | 1000 | 75.0800 | "fit_budget" |
| gas_drift | fastener_llm_sonnet_blind | 2021 | 0.9195 | 0.9561 | 125.3562 | 1 | 1000 | 748.0200 | "fit_budget" |
| gas_drift | fastener_llm_opus_blind | 2024 | 0.9235 | 0.9580 | 125.4379 | 1 | 1000 | 896.8700 | "fit_budget" |
| har | fastener_llm_haiku_blind | 2023 | 0.8864 | 0.9337 | 549.4899 | 1 | 1000 | 747.1800 | "fit_budget" |
| spambase | fastener_llm_haiku_blind | 2023 | 0.8936 | 0.9133 | 52.1450 | 1 | 1000 | 82.1000 | "fit_budget" |
| gas_drift | fastener_llm_opus_blind | 2020 | 0.9249 | 0.9578 | 125.4109 | 1 | 1000 | 479.6300 | "fit_budget" |
| adult | fastener_llm_sonnet_blind | 2024 | 0.8384 | 0.8495 | 53.1831 | 1 | 1000 | 199.3200 | "fit_budget" |
| heloc | fastener_llm_haiku_blind | 2021 | 0.7010 | 0.7049 | 14.8223 | 1 | 1000 | 71.1700 | "fit_budget" |
| heloc | fastener_llm_sonnet_blind | 2020 | 0.7022 | 0.7059 | 14.8374 | 1 | 1000 | 71.1800 | "fit_budget" |
| adult | fastener_llm_sonnet_blind | 2023 | 0.8380 | 0.8496 | 53.1662 | 1 | 1000 | 196.1300 | "fit_budget" |
| adult | fastener_llm_haiku_blind | 2020 | 0.8374 | 0.8488 | 53.1433 | 1 | 1000 | 201.8100 | "fit_budget" |
| phishing | fastener_llm_haiku_blind | 2022 | 0.9267 | 0.9410 | 27.4280 | 1 | 1000 | 92.9600 | "fit_budget" |
| phishing | fastener_llm_haiku_blind | 2021 | 0.9265 | 0.9399 | 27.4051 | 1 | 1000 | 91.0200 | "fit_budget" |
| adult | fastener_llm_opus_blind | 2023 | 0.8384 | 0.8510 | 53.3711 | 1 | 1000 | 220.5200 | "fit_budget" |
| adult | fastener_llm_opus_blind | 2024 | 0.8380 | 0.8500 | 53.2048 | 1 | 1000 | 215.0400 | "fit_budget" |
| phishing | fastener_llm_haiku_blind | 2020 | 0.9274 | 0.9391 | 27.3548 | 1 | 1000 | 92.6600 | "fit_budget" |
| heloc | fastener_llm_sonnet_blind | 2021 | 0.6986 | 0.6961 | 14.7605 | 1 | 1000 | 72.1800 | "fit_budget" |
| heloc | fastener_llm_haiku_blind | 2023 | 0.7029 | 0.7068 | 14.8926 | 1 | 1000 | 76.1600 | "fit_budget" |
| heloc | fastener_llm_sonnet_blind | 2023 | 0.7012 | 0.7062 | 14.8491 | 1 | 1000 | 77.1600 | "fit_budget" |
| heloc | fastener_llm_haiku_blind | 2022 | 0.7037 | 0.7062 | 14.9025 | 1 | 1000 | 79.2200 | "fit_budget" |
| heloc | fastener_llm_opus_blind | 2023 | 0.7017 | 0.7052 | 14.8664 | 1 | 1000 | 111.8900 | "fit_budget" |
| gas_drift | fastener_llm_opus_blind | 2023 | 0.9201 | 0.9554 | 125.2729 | 1 | 1000 | 696.2400 | "fit_budget" |
| spambase | fastener_llm_haiku_blind | 2021 | 0.8942 | 0.9180 | 52.3735 | 1 | 1000 | 83.8800 | "fit_budget" |
| spambase | fastener_llm_haiku_blind | 2022 | 0.8977 | 0.9142 | 52.0042 | 1 | 1000 | 86.7300 | "fit_budget" |
| har | fastener_llm_haiku_blind | 2020 | 0.8994 | 0.9374 | 547.5197 | 1 | 1000 | 703.2600 | "fit_budget" |
| gas_drift | fastener_llm_haiku_blind | 2020 | 0.9251 | 0.9579 | 125.4974 | 1 | 1000 | 934.2100 | "fit_budget" |
| spambase | fastener_llm_haiku_blind | 2024 | 0.8864 | 0.9060 | 51.6040 | 1 | 1000 | 86.4600 | "fit_budget" |
| gas_drift | fastener_llm_sonnet_blind | 2024 | 0.9152 | 0.9534 | 125.2642 | 1 | 1000 | 767.6500 | "fit_budget" |
| adult | fastener_llm_opus_blind | 2021 | 0.8386 | 0.8514 | 53.3719 | 1 | 1000 | 162.2700 | "fit_budget" |
| har | fastener_llm_sonnet_blind | 2021 | 0.9014 | 0.9384 | 548.5412 | 1 | 1000 | 934.9300 | "fit_budget" |
| har | fastener_llm_sonnet_blind | 2023 | 0.8819 | 0.9293 | 547.0486 | 1 | 1000 | 597.6300 | "fit_budget" |
| har | fastener_llm_sonnet_blind | 2022 | 0.8800 | 0.9290 | 547.3183 | 1 | 1000 | 709.8600 | "fit_budget" |
| heloc | fastener_llm_opus_blind | 2020 | 0.6999 | 0.7039 | 14.8664 | 1 | 1000 | 112.4000 | "fit_budget" |
| har | fastener_llm_haiku_blind | 2024 | 0.8986 | 0.9384 | 549.3503 | 1 | 1000 | 1218.0000 | "fit_budget" |
| ozone_8hr | fastener_llm_haiku_blind | 2020 | 0.9034 | 0.9024 | 64.8402 | 1 | 1000 | 51.9000 | "fit_budget" |
| ozone_8hr | fastener_llm_sonnet_blind | 2024 | 0.9201 | 0.9210 | 65.7720 | 1 | 1000 | 49.8000 | "fit_budget" |
| adult | fastener_llm_sonnet_blind | 2020 | 0.8356 | 0.8489 | 53.3164 | 1 | 1000 | 208.4700 | "fit_budget" |
| har | fastener_llm_sonnet_blind | 2024 | 0.8927 | 0.9342 | 546.3629 | 1 | 1000 | 643.0200 | "fit_budget" |
| ozone_8hr | fastener_llm_haiku_blind | 2021 | 0.9150 | 0.9144 | 65.1025 | 1 | 1000 | 42.4600 | "fit_budget" |
| pc4 | fastener_llm_opus_blind | 2024 | 0.8974 | 0.9045 | 32.6756 | 1 | 1000 | 30.3600 | "fit_budget" |
| har | fastener_llm_haiku_blind | 2021 | 0.9041 | 0.9401 | 547.5457 | 1 | 1000 | 759.9900 | "fit_budget" |
| pc4 | fastener_llm_opus_blind | 2023 | 0.8964 | 0.9050 | 32.7451 | 1 | 1000 | 31.0600 | "fit_budget" |
| ozone_8hr | fastener_llm_haiku_blind | 2024 | 0.9155 | 0.9156 | 65.4796 | 1 | 1000 | 42.5900 | "fit_budget" |
| ozone_8hr | fastener_llm_haiku_blind | 2023 | 0.9162 | 0.9208 | 65.6170 | 1 | 1000 | 43.2500 | "fit_budget" |
| pc4 | fastener_llm_opus_blind | 2022 | 0.8969 | 0.9000 | 32.7332 | 1 | 1000 | 31.4300 | "fit_budget" |
| pc4 | fastener_llm_opus_blind | 2021 | 0.9006 | 0.9063 | 32.7682 | 1 | 1000 | 31.3000 | "fit_budget" |
| ozone_8hr | fastener_llm_sonnet_blind | 2023 | 0.9130 | 0.9144 | 65.0726 | 1 | 1000 | 51.9200 | "fit_budget" |
| spambase | fastener_llm_haiku_blind | 2020 | 0.8952 | 0.9171 | 52.3141 | 1 | 1000 | 86.8900 | "fit_budget" |
| spambase | fastener_llm_sonnet_blind | 2024 | 0.9010 | 0.9209 | 52.3260 | 1 | 1000 | 78.4000 | "fit_budget" |
| adult | fastener_llm_haiku_blind | 2022 | 0.8386 | 0.8512 | 53.3470 | 1 | 1000 | 320.0200 | "fit_budget" |
| phishing | fastener_llm_haiku_blind | 2024 | 0.9277 | 0.9433 | 27.5376 | 1 | 1000 | 91.0800 | "fit_budget" |
| gas_drift | fastener_llm_opus_blind | 2022 | 0.9208 | 0.9559 | 125.2047 | 1 | 1000 | 805.4200 | "fit_budget" |
| spambase | fastener_llm_sonnet_blind | 2021 | 0.9002 | 0.9231 | 52.5599 | 1 | 1000 | 83.2600 | "fit_budget" |
| adult | fastener_llm_opus_blind | 2020 | 0.8378 | 0.8491 | 53.1468 | 1 | 1000 | 225.6100 | "fit_budget" |
| ozone_8hr | fastener_llm_haiku_blind | 2022 | 0.9143 | 0.9147 | 65.4685 | 1 | 1000 | 42.7200 | "fit_budget" |
| adult | fastener_llm_opus_blind | 2022 | 0.8378 | 0.8503 | 53.3357 | 1 | 1000 | 215.6200 | "fit_budget" |
| pc4 | fastener_llm_opus_blind | 2020 | 0.8968 | 0.8993 | 32.6268 | 1 | 1000 | 33.6200 | "fit_budget" |
| spambase | fastener_llm_sonnet_blind | 2020 | 0.8977 | 0.9158 | 52.0877 | 1 | 1000 | 81.3900 | "fit_budget" |
| spambase | fastener_llm_opus_blind | 2020 | 0.9002 | 0.9196 | 52.4257 | 1 | 1000 | 81.2000 | "fit_budget" |
| eye_movements | fastener_llm_sonnet_blind | 2021 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 102.1200 | "fit_budget" |
| gas_drift | fastener_llm_haiku_blind | 2022 | 0.9267 | 0.9594 | 125.5542 | 1 | 1000 | 777.3200 | "fit_budget" |
| eye_movements | fastener_llm_haiku_blind | 2022 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 67.3800 | "fit_budget" |
| eye_movements | fastener_llm_sonnet_blind | 2023 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 58.4800 | "fit_budget" |
| spambase | fastener_llm_opus_blind | 2021 | 0.8970 | 0.9203 | 52.8049 | 1 | 1000 | 78.9400 | "fit_budget" |
| spambase | fastener_llm_opus_blind | 2022 | 0.8934 | 0.9156 | 52.2827 | 1 | 1000 | 86.0500 | "fit_budget" |
| phishing | fastener_llm_haiku_blind | 2023 | 0.9266 | 0.9419 | 27.4706 | 1 | 1000 | 91.3000 | "fit_budget" |
| eye_movements | fastener_llm_opus_blind | 2020 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 93.0200 | "fit_budget" |
| spambase | fastener_llm_opus_blind | 2023 | 0.8998 | 0.9227 | 52.7034 | 1 | 1000 | 83.3900 | "fit_budget" |
| eye_movements | fastener_llm_haiku_blind | 2020 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 69.3200 | "fit_budget" |
| eye_movements | fastener_llm_haiku_blind | 2021 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 66.6800 | "fit_budget" |
| eye_movements | fastener_llm_sonnet_blind | 2024 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 70.4000 | "fit_budget" |
| eye_movements | fastener_llm_haiku_blind | 2023 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 70.0700 | "fit_budget" |
| eye_movements | fastener_llm_haiku_blind | 2024 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 72.1100 | "fit_budget" |
| eye_movements | fastener_llm_opus_blind | 2021 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 95.5600 | "fit_budget" |
| eye_movements | fastener_llm_sonnet_blind | 2020 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 106.5300 | "fit_budget" |
| eye_movements | fastener_llm_opus_blind | 2023 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 104.2500 | "fit_budget" |
| eye_movements | fastener_llm_sonnet_blind | 2022 | 0.6315 | 0.6350 | 12.2350 | 1 | 1000 | 106.2300 | "fit_budget" |
| eye_movements | fastener_llm_opus_blind | 2022 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 106.4700 | "fit_budget" |
| eye_movements | fastener_llm_opus_blind | 2024 | 0.6302 | 0.6344 | 12.1787 | 1 | 1000 | 103.9800 | "fit_budget" |
| pc4 | fastener_llm_sonnet_blind | 2021 | 0.8898 | 0.8958 | 32.5380 | 1 | 1000 | 43.7500 | "fit_budget" |
| pc4 | fastener_llm_sonnet_blind | 2023 | 0.8995 | 0.9028 | 32.6354 | 1 | 1000 | 44.0500 | "fit_budget" |
| pc4 | fastener_llm_sonnet_blind | 2020 | 0.8995 | 0.9035 | 32.6289 | 1 | 1000 | 73.4000 | "fit_budget" |
| pc4 | fastener_llm_sonnet_blind | 2022 | 0.8938 | 0.8970 | 32.5721 | 1 | 1000 | 119.4700 | "fit_budget" |
| pc4 | fastener_llm_sonnet_blind | 2024 | 0.9001 | 0.9045 | 32.8575 | 1 | 1000 | 46.0000 | "fit_budget" |
| pc4 | fastener_llm_haiku_blind | 2022 | 0.8952 | 0.8985 | 32.5359 | 1 | 1000 | 72.6000 | "fit_budget" |
| pc4 | fastener_llm_haiku_blind | 2023 | 0.8919 | 0.8946 | 32.5359 | 1 | 1000 | 70.8800 | "fit_budget" |
| pc4 | fastener_llm_haiku_blind | 2021 | 0.9048 | 0.9142 | 33.0605 | 1 | 1000 | 47.1600 | "fit_budget" |
| pc4 | fastener_llm_haiku_blind | 2024 | 0.9001 | 0.9046 | 32.6354 | 1 | 1000 | 43.2300 | "fit_budget" |
| pc4 | fastener_llm_haiku_blind | 2020 | 0.9007 | 0.9063 | 32.7273 | 1 | 1000 | 73.7700 | "fit_budget" |
| mice_protein | fastener_llm_opus_blind | 2021 | 0.8436 | 0.9000 | 72.9359 | 1 | 1000 | 245.1700 | "fit_budget" |
| mice_protein | fastener_llm_opus_blind | 2020 | 0.8280 | 0.9025 | 72.7706 | 1 | 1000 | 249.3600 | "fit_budget" |
| mice_protein | fastener_llm_opus_blind | 2022 | 0.8311 | 0.8937 | 71.6194 | 1 | 1000 | 247.4900 | "fit_budget" |
| mice_protein | fastener_llm_opus_blind | 2023 | 0.8077 | 0.8806 | 71.0344 | 1 | 1000 | 422.8800 | "fit_budget" |
| mice_protein | fastener_llm_opus_blind | 2024 | 0.8283 | 0.8979 | 72.1545 | 1 | 1000 | 246.9100 | "fit_budget" |
| mice_protein | fastener_llm_sonnet_blind | 2020 | 0.8302 | 0.8964 | 72.1648 | 1 | 1000 | 252.9800 | "fit_budget" |
| mice_protein | fastener_llm_sonnet_blind | 2021 | 0.8229 | 0.8878 | 71.4996 | 1 | 1000 | 245.7800 | "fit_budget" |
| mice_protein | fastener_llm_sonnet_blind | 2023 | 0.8436 | 0.9102 | 72.9069 | 1 | 1000 | 246.3300 | "fit_budget" |
| mice_protein | fastener_llm_sonnet_blind | 2022 | 0.8352 | 0.9060 | 72.8562 | 1 | 1000 | 249.5100 | "fit_budget" |
| mice_protein | fastener_llm_sonnet_blind | 2024 | 0.8391 | 0.9034 | 72.5558 | 1 | 1000 | 243.8500 | "fit_budget" |
| mice_protein | fastener_llm_haiku_blind | 2020 | 0.8385 | 0.9029 | 72.5691 | 1 | 1000 | 243.2100 | "fit_budget" |
| mice_protein | fastener_llm_haiku_blind | 2021 | 0.8441 | 0.9057 | 72.2926 | 1 | 1000 | 231.5100 | "fit_budget" |
| mice_protein | fastener_llm_haiku_blind | 2022 | 0.8243 | 0.8885 | 71.1608 | 1 | 1000 | 228.2100 | "fit_budget" |
| qsar_biodeg | fastener_llm_opus_blind | 2020 | 0.8264 | 0.8572 | 34.9032 | 1 | 1000 | 36.4500 | "fit_budget" |
| mice_protein | fastener_llm_haiku_blind | 2023 | 0.8347 | 0.9058 | 72.8249 | 1 | 1000 | 232.9400 | "fit_budget" |
| mice_protein | fastener_llm_haiku_blind | 2024 | 0.8320 | 0.9020 | 72.4788 | 1 | 1000 | 234.0300 | "fit_budget" |
| qsar_biodeg | fastener_llm_opus_blind | 2021 | 0.8429 | 0.8631 | 34.9301 | 1 | 1000 | 68.9800 | "fit_budget" |
| qsar_biodeg | fastener_llm_opus_blind | 2022 | 0.8492 | 0.8706 | 35.2497 | 1 | 1000 | 56.1800 | "fit_budget" |
| qsar_biodeg | fastener_llm_sonnet_blind | 2024 | 0.8362 | 0.8478 | 34.1521 | 1 | 1000 | 33.8100 | "fit_budget" |
| qsar_biodeg | fastener_llm_sonnet_blind | 2021 | 0.8262 | 0.8364 | 33.6803 | 1 | 1000 | 36.0600 | "fit_budget" |
| qsar_biodeg | fastener_llm_sonnet_blind | 2023 | 0.8313 | 0.8393 | 34.0296 | 1 | 1000 | 35.9400 | "fit_budget" |
| qsar_biodeg | fastener_llm_sonnet_blind | 2022 | 0.8351 | 0.8547 | 34.6059 | 1 | 1000 | 36.7000 | "fit_budget" |
| qsar_biodeg | fastener_llm_opus_blind | 2023 | 0.8334 | 0.8428 | 34.9746 | 1 | 1000 | 65.0700 | "fit_budget" |
| qsar_biodeg | fastener_llm_sonnet_blind | 2020 | 0.8358 | 0.8437 | 34.5390 | 1 | 1000 | 57.2800 | "fit_budget" |
| qsar_biodeg | fastener_llm_opus_blind | 2024 | 0.8312 | 0.8533 | 34.6466 | 1 | 1000 | 63.7900 | "fit_budget" |
| qsar_biodeg | fastener_llm_haiku_blind | 2023 | 0.8322 | 0.8470 | 34.6622 | 1 | 1000 | 36.3300 | "fit_budget" |
| qsar_biodeg | fastener_llm_haiku_blind | 2024 | 0.8178 | 0.8258 | 33.7513 | 1 | 1000 | 57.3300 | "fit_budget" |
| qsar_biodeg | fastener_llm_haiku_blind | 2022 | 0.8422 | 0.8608 | 34.8023 | 1 | 1000 | 63.1000 | "fit_budget" |
| qsar_biodeg | fastener_llm_haiku_blind | 2021 | 0.8343 | 0.8497 | 34.4692 | 1 | 1000 | 38.0700 | "fit_budget" |

Progress curves: every run key's trajectory is in its run's `trajectories/` directory.

**Timeline (UTC, Vega's clock; the workstation's clock is 10 minutes ahead, so commit times read 10 minutes later than the runs' times).**

1. **Registration (30 Oct).** The strict control registered in `0d7a9c3` (DEC-51), from the priors only, before any H8-E01 result was read.
2. **Priors.** The 48 blind priors made on the workstation and committed with their call log in `79d5ac2` ($0.84).
3. **Test job (00:52).** `test.sbatch`'s quick real job (`qsar_biodeg:fastener_llm_haiku_blind`, seed 2020) started before the Vega clone had pulled `79d5ac2` and failed at once: the blind prior file was missing (`FileNotFoundError`). Its folder `20261030T005231Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020` holds only a manifest and `progress.json`, is `failed`, and is out of the ledger. After the pull the job list was built (00:55) and the arrays submitted.
4. **All runs (00:56 to 02:14, 1 h 18 min).** 240 jobs on `79d5ac2` and FASTENER `9226b90`, all `ok`, evidence, `code_dirty: false`, each stopped on `fit_budget` at exactly 1,000 fits. The job logs (`distill_logs.py`) hold no error, no warning and no incomplete log; wall time per run median 165 s, 90th percentile 1,326 s, longest 4,502 s (75 min); 36.5 run-hours in all. No model call during the runs.

**Checks after the fetch.**
- Every run's recorded `prior_sha256` equals the SHA256 of the prior file committed in `79d5ac2` (240 of 240), so each run read the committed blind prior, whatever the clocks say.
- One config hash per arm; the three arms on diabetes130 run identically (their priors are all flat, so the guidance is the same), as expected.
- The blind priors recall the datasets' column order (REPORT F2): found while writing this report, from the priors and the runs' results; nothing was rerun or changed.

## 5. Evidence

The numbers the criterion is evaluated on. What they mean is in [REPORT.md](REPORT.md).

### H8: the criterion

Verdict (`tables/verdict.json`): **not supported** for Opus, Sonnet and Haiku -- part (i) holds for all three, part (ii) for none.

| part | arm | opponent | datasets | W-T-L | mean log2 ratio | median | p | Holm p | holds |
|---|---|---|---|---|---|---|---|---|---|
| (i) | fastener_llm_opus | fastener | 16 | 13-0-3 | +0.610 | +0.421 | 0.00763 | 0.0153 | True |
| (i) | fastener_llm_sonnet | fastener | 16 | 13-0-3 | +0.731 | +0.738 | 0.00168 | 0.00504 | True |
| (i) | fastener_llm_haiku | fastener | 16 | 13-0-3 | +0.571 | +0.543 | 0.00763 | 0.0153 | True |
| (ii) | fastener_llm_opus | fastener_llm_opus_blind | 16 | 10-0-6 | +0.180 | +0.168 | 0.433 | 1 | False |
| (ii) | fastener_llm_sonnet | fastener_llm_sonnet_blind | 16 | 8-0-8 | +0.077 | +0.028 | 0.744 | 1 | False |
| (ii) | fastener_llm_haiku | fastener_llm_haiku_blind | 16 | 9-0-7 | +0.173 | +0.043 | 0.562 | 1 | False |

Beside the criterion (`tables/beside.csv`; unadjusted p; H8-E01's arms with H8-E02's):

| arm | opponent | datasets | W-T-L | mean log2 ratio | p |
|---|---|---|---|---|---|
| fastener_llm_opus | fastener_llm_opus_scrambled | 16 | 8-0-8 | -0.060 | 0.669 |
| fastener_llm_sonnet | fastener_llm_sonnet_scrambled | 16 | 8-0-8 | -0.077 | 0.562 |
| fastener_llm_haiku | fastener_llm_haiku_scrambled | 16 | 7-0-9 | +0.054 | 0.744 |
| fastener_llm_opus_scrambled | fastener_llm_opus_blind | 16 | 13-0-3 | +0.331 | 0.0214 |
| fastener_llm_sonnet_scrambled | fastener_llm_sonnet_blind | 16 | 10-0-6 | +0.226 | 0.252 |
| fastener_llm_haiku_scrambled | fastener_llm_haiku_blind | 16 | 6-1-9 | +0.037 | 0.89 |
| fastener_llm_opus_blind | fastener | 16 | 10-0-6 | +0.361 | 0.0507 |
| fastener_llm_sonnet_blind | fastener | 16 | 14-0-2 | +0.495 | 0.00336 |
| fastener_llm_haiku_blind | fastener | 16 | 10-0-6 | +0.327 | 0.0507 |
| fastener_llm_opus_proposer | fastener_llm_opus | 16 | 8-0-8 | +0.260 | 0.211 |
| fastener_llm_sonnet_proposer | fastener_llm_sonnet | 16 | 11-0-5 | +0.189 | 0.231 |
| fastener_llm_haiku_proposer | fastener_llm_haiku | 16 | 10-0-6 | +0.175 | 0.298 |
| fastener_llm_opus_proposer | fastener | 16 | 12-0-4 | +0.807 | 0.00516 |
| fastener_llm_sonnet_proposer | fastener | 16 | 14-0-2 | +0.910 | 0.000305 |
| fastener_llm_haiku_proposer | fastener | 16 | 13-0-3 | +0.744 | 0.00516 |
| fastener_llm_opus_mating | fastener | 16 | 8-0-8 | +0.043 | 0.632 |
| fastener_llm_opus_mutation | fastener | 16 | 11-0-5 | +0.493 | 0.0654 |
| fastener_llm_opus_initial | fastener | 16 | 10-0-6 | +0.169 | 0.464 |
| fastener_llm_opus_mating | fastener_llm_opus | 16 | 5-0-11 | -0.610 | 0.0214 |
| fastener_llm_opus_mutation | fastener_llm_opus | 16 | 7-0-9 | -0.045 | 0.706 |
| fastener_llm_opus_initial | fastener_llm_opus | 16 | 3-0-13 | -0.406 | 0.0507 |
| fastener_seed_mrmr | fastener | 16 | 11-0-5 | +0.356 | 0.117 |
| fastener_llm_opus | fastener_seed_mrmr | 16 | 11-0-5 | +0.310 | 0.348 |
| fastener_llm_sonnet | fastener_seed_mrmr | 16 | 10-0-6 | +0.261 | 0.375 |
| fastener_llm_haiku | fastener_seed_mrmr | 16 | 11-0-5 | +0.324 | 0.0739 |

Per seed: `tables/per_seed.csv` (target, fits of each arm, effect).

End-of-budget test AUF (K = 10), mean over datasets (`tables/end_auf.csv`):

| arm | mean AUF |
|---|---|
| fastener | 0.7965 |
| fastener_llm_haiku | 0.7984 |
| fastener_llm_haiku_blind | 0.7968 |
| fastener_llm_haiku_proposer | 0.7975 |
| fastener_llm_haiku_scrambled | 0.7960 |
| fastener_llm_opus | 0.7964 |
| fastener_llm_opus_blind | 0.7966 |
| fastener_llm_opus_initial | 0.7958 |
| fastener_llm_opus_mating | 0.7967 |
| fastener_llm_opus_mutation | 0.7973 |
| fastener_llm_opus_proposer | 0.7962 |
| fastener_llm_opus_scrambled | 0.7974 |
| fastener_llm_sonnet | 0.7964 |
| fastener_llm_sonnet_blind | 0.7969 |
| fastener_llm_sonnet_proposer | 0.7974 |
| fastener_llm_sonnet_scrambled | 0.7977 |
| fastener_seed_mrmr | 0.7972 |

Priors (`tables/prior_agreement.csv`), per dataset and model: Spearman of the named prior with mutual information on the training split (`spearman_mi`), with its scrambled and blind twins; the blind prior's Spearman with mutual information (`blind_spearman_mi`); whether it is flat (`blind_flat`); and its layout recall (`blind_layout_recall`: the blind scores read by shown position against the named scores read by column index). Model calls of H8-E01 and H8-E02: `tables/spend.csv`.

Bootstrap intervals, the 7-pair split and the correlations of REPORT F1, F3 and F4 come from `tables/per_seed.csv` and `tables/prior_agreement.csv` (mean over seeds per dataset; the intervals are `ci_low` and `ci_high` of `criterion.csv` and `beside.csv`, 10,000 resamples of the 16 datasets in `h8_report.compare`; the split and the Spearman correlations over the 40 non-flat dataset-model pairs are computed from the two tables).

Figures, in [figures/](figures/) (`h8_report.py --experiment H8-E01 --control H8-E02 --out H8-E02`): `F1_H8_criterion.png`, `F2_blind_recall.png`, `F3_blind_mi.png`, `F4_blind_split.png`, `F5_end_auf.png`, and beside them `F6_beside.png` (every comparison beside the criterion) and `F7_priors_and_cost.png` (the priors' agreement with mutual information; the cost of all model calls). The prompts as sent: [methods/](methods/).

## 6. Reproduction

From a clean checkout of both repositories at the commits in the header:

```
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_eodata_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_eodata_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_eodata_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_covertype_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_eodata_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_covertype_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_covertype_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_eodata_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_eodata_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_eodata_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_covertype_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_eodata_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_covertype_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_covertype_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_eodata_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_diabetes130_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_covertype_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_covertype_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_eodata_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_eodata_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_covertype_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_eodata_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_eodata_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_eodata_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_covertype_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_covertype_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_covertype_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eodata --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_eodata_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_covertype_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_crop_mapping_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_covertype_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset covertype --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_covertype_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_crop_mapping_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_diabetes130_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_diabetes130_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_diabetes130_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_phishing_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_higgs_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset crop_mapping --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_crop_mapping_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_har_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_har_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_higgs_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_higgs_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_higgs_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_higgs_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_phishing_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_har_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_higgs_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_higgs_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_higgs_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_higgs_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_har_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_har_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_diabetes130_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_diabetes130_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_higgs_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_phishing_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_har_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_adult_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_adult_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_higgs_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_adult_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_higgs_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset diabetes130 --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_diabetes130_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_higgs_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_higgs_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset higgs --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_higgs_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_heloc_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_phishing_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_phishing_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_spambase_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_phishing_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_heloc_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_spambase_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_spambase_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_ozone_8hr_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_har_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_phishing_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_phishing_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_heloc_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_heloc_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_adult_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_adult_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_heloc_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_phishing_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_gas_drift_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_heloc_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_phishing_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_heloc_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_gas_drift_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_har_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_spambase_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_gas_drift_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_adult_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_heloc_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_heloc_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_adult_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_adult_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_phishing_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_phishing_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_adult_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_adult_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_phishing_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_heloc_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_heloc_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_heloc_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_heloc_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_heloc_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_gas_drift_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_spambase_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_spambase_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_har_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_spambase_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_gas_drift_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_adult_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_har_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_har_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_har_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset heloc --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_heloc_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_har_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_adult_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_har_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_pc4_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset har --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_har_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_pc4_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_pc4_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_pc4_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_spambase_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_spambase_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_adult_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_phishing_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_gas_drift_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_spambase_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_adult_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset ozone_8hr --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_ozone_8hr_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset adult --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_adult_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_pc4_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_spambase_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_spambase_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset gas_drift --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_gas_drift_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_spambase_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_spambase_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset phishing --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_phishing_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_eye_movements_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset spambase --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_spambase_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_eye_movements_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_eye_movements_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_eye_movements_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_eye_movements_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_eye_movements_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset eye_movements --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_eye_movements_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_pc4_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_pc4_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_pc4_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_pc4_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_pc4_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_pc4_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_pc4_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_pc4_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_pc4_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset pc4 --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_pc4_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_mice_protein_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_mice_protein_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_mice_protein_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_mice_protein_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_mice_protein_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_mice_protein_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2020 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2020 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset mice_protein --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_mice_protein_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2021 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2022 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2024 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2021 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2023 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2022 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2023 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_sonnet_blind --seed 2020 --name h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2020 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_opus_blind --seed 2024 --name h8e02_qsar_biodeg_fastener_llm_opus_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2023 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2023 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2024 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2024 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2022 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2022 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/run_sota.py --dataset qsar_biodeg --methods  --fastener-arm llm_haiku_blind --seed 2021 --name h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2021 --experiment H8-E02 --evaluations 1000 --model lgbm --model-jobs 8 --n-jobs 8
python experiments/make_report.py --experiment H8-E02 --runs 20261030T005602Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2020 20261030T005725Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2022 20261030T005726Z_h8e02_eodata_fastener_llm_opus_blind_s2022 20261030T005725Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2020 20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2021 20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2020 20261030T005725Z_h8e02_covertype_fastener_llm_opus_blind_s2020 20261030T005727Z_h8e02_eodata_fastener_llm_opus_blind_s2024 20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2021 20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2021 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2024 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2020 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2022 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2022 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2021 20261030T005727Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2023 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2024 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2021 20261030T005728Z_h8e02_eodata_fastener_llm_opus_blind_s2023 20261030T005726Z_h8e02_covertype_fastener_llm_haiku_blind_s2022 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2024 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2021 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2021 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2023 20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2020 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2023 20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2023 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2021 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2021 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2022 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2022 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2022 20261030T005728Z_h8e02_eodata_fastener_llm_sonnet_blind_s2020 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2024 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2022 20261030T005726Z_h8e02_covertype_fastener_llm_opus_blind_s2024 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2020 20261030T005728Z_h8e02_eodata_fastener_llm_haiku_blind_s2020 20261030T005727Z_h8e02_covertype_fastener_llm_haiku_blind_s2024 20261030T005728Z_h8e02_crop_mapping_fastener_llm_haiku_blind_s2024 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2024 20261030T005726Z_h8e02_covertype_fastener_llm_sonnet_blind_s2023 20261030T005728Z_h8e02_crop_mapping_fastener_llm_opus_blind_s2020 20261030T005727Z_h8e02_diabetes130_fastener_llm_opus_blind_s2020 20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2022 20261030T005726Z_h8e02_diabetes130_fastener_llm_opus_blind_s2021 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2020 20261030T005726Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2023 20261030T005726Z_h8e02_phishing_fastener_llm_opus_blind_s2020 20261030T005726Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2023 20261030T005726Z_h8e02_higgs_fastener_llm_haiku_blind_s2024 20261030T005728Z_h8e02_crop_mapping_fastener_llm_sonnet_blind_s2023 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2021 20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2022 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2021 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2020 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2024 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2020 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2021 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2022 20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2024 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2023 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2020 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2024 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2022 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2020 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2023 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2024 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2024 20261030T005727Z_h8e02_har_fastener_llm_sonnet_blind_s2020 20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2021 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2022 20261030T005727Z_h8e02_diabetes130_fastener_llm_haiku_blind_s2022 20261030T005728Z_h8e02_diabetes130_fastener_llm_opus_blind_s2024 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2021 20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2021 20261030T005727Z_h8e02_har_fastener_llm_opus_blind_s2024 20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2021 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2020 20261030T005728Z_h8e02_adult_fastener_llm_sonnet_blind_s2022 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2023 20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2021 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2022 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2020 20261030T005727Z_h8e02_higgs_fastener_llm_sonnet_blind_s2022 20261030T005727Z_h8e02_diabetes130_fastener_llm_sonnet_blind_s2024 20261030T005727Z_h8e02_higgs_fastener_llm_opus_blind_s2023 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2020 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2023 20261030T005727Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2021 20261030T005727Z_h8e02_higgs_fastener_llm_haiku_blind_s2021 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2021 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2022 20261030T005727Z_h8e02_phishing_fastener_llm_sonnet_blind_s2020 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2024 20261030T005727Z_h8e02_phishing_fastener_llm_opus_blind_s2022 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2021 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2023 20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2023 20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2022 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2024 20261030T005728Z_h8e02_spambase_fastener_llm_sonnet_blind_s2022 20261030T005728Z_h8e02_spambase_fastener_llm_opus_blind_s2024 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2022 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2021 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_opus_blind_s2020 20261030T005728Z_h8e02_har_fastener_llm_haiku_blind_s2022 20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2023 20261030T005728Z_h8e02_phishing_fastener_llm_opus_blind_s2024 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2022 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2024 20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_adult_fastener_llm_haiku_blind_s2024 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2022 20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2023 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2021 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2020 20261030T005728Z_h8e02_phishing_fastener_llm_sonnet_blind_s2021 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2024 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2021 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2024 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2020 20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2024 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2021 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2020 20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2023 20261030T005729Z_h8e02_adult_fastener_llm_haiku_blind_s2020 20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2022 20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2021 20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2023 20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2024 20261030T005728Z_h8e02_phishing_fastener_llm_haiku_blind_s2020 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2021 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_heloc_fastener_llm_sonnet_blind_s2023 20261030T005728Z_h8e02_heloc_fastener_llm_haiku_blind_s2022 20261030T005728Z_h8e02_heloc_fastener_llm_opus_blind_s2023 20261030T005728Z_h8e02_gas_drift_fastener_llm_opus_blind_s2023 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2021 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2022 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2020 20261030T005728Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2020 20261030T005728Z_h8e02_spambase_fastener_llm_haiku_blind_s2024 20261030T005728Z_h8e02_gas_drift_fastener_llm_sonnet_blind_s2024 20261030T005729Z_h8e02_adult_fastener_llm_opus_blind_s2021 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2021 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2023 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2022 20261030T005729Z_h8e02_heloc_fastener_llm_opus_blind_s2020 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2024 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2020 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2024 20261030T005729Z_h8e02_adult_fastener_llm_sonnet_blind_s2020 20261030T005729Z_h8e02_har_fastener_llm_sonnet_blind_s2024 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2021 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2024 20261030T005729Z_h8e02_har_fastener_llm_haiku_blind_s2021 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2023 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2024 20261030T005728Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2023 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2022 20261030T005728Z_h8e02_pc4_fastener_llm_opus_blind_s2021 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_sonnet_blind_s2023 20261030T005729Z_h8e02_spambase_fastener_llm_haiku_blind_s2020 20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2024 20261030T005730Z_h8e02_adult_fastener_llm_haiku_blind_s2022 20261030T005730Z_h8e02_phishing_fastener_llm_haiku_blind_s2024 20261030T005729Z_h8e02_gas_drift_fastener_llm_opus_blind_s2022 20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2021 20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2020 20261030T005729Z_h8e02_ozone_8hr_fastener_llm_haiku_blind_s2022 20261030T005730Z_h8e02_adult_fastener_llm_opus_blind_s2022 20261030T005729Z_h8e02_pc4_fastener_llm_opus_blind_s2020 20261030T005729Z_h8e02_spambase_fastener_llm_sonnet_blind_s2020 20261030T005731Z_h8e02_spambase_fastener_llm_opus_blind_s2020 20261030T005731Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2021 20261030T005731Z_h8e02_gas_drift_fastener_llm_haiku_blind_s2022 20261030T005731Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2022 20261030T005732Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2023 20261030T005732Z_h8e02_spambase_fastener_llm_opus_blind_s2021 20261030T005734Z_h8e02_spambase_fastener_llm_opus_blind_s2022 20261030T005734Z_h8e02_phishing_fastener_llm_haiku_blind_s2023 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2020 20261030T005735Z_h8e02_spambase_fastener_llm_opus_blind_s2023 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2020 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2021 20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2024 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2023 20261030T005735Z_h8e02_eye_movements_fastener_llm_haiku_blind_s2024 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2021 20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2020 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2023 20261030T005735Z_h8e02_eye_movements_fastener_llm_sonnet_blind_s2022 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2022 20261030T005735Z_h8e02_eye_movements_fastener_llm_opus_blind_s2024 20261030T005812Z_h8e02_pc4_fastener_llm_sonnet_blind_s2021 20261030T005813Z_h8e02_pc4_fastener_llm_sonnet_blind_s2023 20261030T005814Z_h8e02_pc4_fastener_llm_sonnet_blind_s2020 20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2022 20261030T005815Z_h8e02_pc4_fastener_llm_sonnet_blind_s2024 20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2022 20261030T005825Z_h8e02_pc4_fastener_llm_haiku_blind_s2023 20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2021 20261030T005826Z_h8e02_pc4_fastener_llm_haiku_blind_s2024 20261030T005828Z_h8e02_pc4_fastener_llm_haiku_blind_s2020 20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2021 20261030T005828Z_h8e02_mice_protein_fastener_llm_opus_blind_s2020 20261030T005829Z_h8e02_mice_protein_fastener_llm_opus_blind_s2022 20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2023 20261030T005832Z_h8e02_mice_protein_fastener_llm_opus_blind_s2024 20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2020 20261030T005833Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2021 20261030T005834Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2023 20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2022 20261030T005838Z_h8e02_mice_protein_fastener_llm_sonnet_blind_s2024 20261030T005855Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2020 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2021 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2022 20261030T005858Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2020 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2023 20261030T005858Z_h8e02_mice_protein_fastener_llm_haiku_blind_s2024 20261030T005900Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2021 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2022 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2024 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2021 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2023 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2022 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2023 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_sonnet_blind_s2020 20261030T005902Z_h8e02_qsar_biodeg_fastener_llm_opus_blind_s2024 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2023 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2024 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2022 20261030T005906Z_h8e02_qsar_biodeg_fastener_llm_haiku_blind_s2021
python experiments/h8_report.py --experiment H8-E01 --control H8-E02 --out H8-E02
```

The last command reads H8-E01's run keys (`reports/H8-E01/tables/run_keys.csv`) with H8-E02's and writes this report's tables, figures and [methods/](methods/).
