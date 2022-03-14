# SARS-COV-2 Africa dashboard
Repository contains code and files to interactive genomics Africa Dashboard

### Before starts:
To generate or update `data/africa.csv` file, first run R script in `source/generate_africa_df.R <Excel file path>`

Example: `Rscript source/generate_africa_df.R  data/africa_all_data_versions/Africa_all_data_4dec_gooddates.xlsx`
## How to install:
1. `conda env create -f requirements.yml`
2. `conda (or source) activate SARS-Cov-2-Africa-dashboard`
3. `streamlit run app.py`

## Data
You can run the dashboard using metadata input for the Augur pipeline, provided by GISAID or setup to automatically from GISAID API.
See a template when the required columns highlighted [here](data/template_metadata.csv).
### Using metadata
1. Define the environment variable with your option: `export SARSCOV2_DATA="metadata"`
2. Generate or update `data/metadata.csv` file: 
   1. Run R script in `source/generate_africa_df.R <Excel file path>`
   2. Example: `Rscript source/generate_africa_df.R  data/africa_all_data_versions/Africa_all_data_4dec_gooddates.xlsx`

### Using API
1. Define the environment variable with your option: `export SARSCOV2_DATA="GISAID_API"`
2. Work with GISAID to get a data agreement. 
3. Define the following environment variables:
~~~
GISAID_URL
GISAID_USERNAME
GISAID_PASSWORD
~~~