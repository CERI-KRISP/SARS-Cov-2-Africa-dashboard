# SARS-COV-2 Africa dashboard
Repository contains code and files to interactive genomics Africa Dashboard

### Before starts:
To generate or update `data/africa.csv` file, first run R script in `source/generate_africa_df.R <Excel file path>`
Example: `Rscript source/generate_africa_df.R  data/africa_all_data_versions/Africa_all_data_4dec_gooddates.xlsx`
### How to install:
1. `conda env create -f requirements.yml`
2. `conda activate SARS-Cov-2-Africa-dashboard`
3. `streamlit run app.py`