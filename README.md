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
You can run the dashboard using GISAID data or your own data through a csv file
### Using your own data
Fill the csv with your data in `data/database_template.csv`

### Using GISAID data
1. Work with GISAID to get a data agreement. 
2. Define the following environment variables:
~~~
GISAID_URL
GISAID_USERNAME
GISAID_PASSWORD
~~~