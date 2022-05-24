# SARS-COV-2 Africa dashboard
Repository contains code and files to interactive genomics Africa Dashboard

## How to install:
1. `conda env create -f requirements.yml`
2. `conda (or source) activate SARS-Cov-2-Africa-dashboard`

## Data
You can run the dashboard using your own data or setting up GISAID API.
In order to inform your choice, set an environment variable:
- `export COVID_DASHBOARD_SOURCE=metadata`, to use your customized data
- `export COVID_DASHBOARD_SOURCE=GISAID_API`, to use GISAID API

### Using metadata
Create your metadata based on [data/template_metadata.csv](data/template_metadata.csv) and save as `./data/metadata.csv`

### Using GISAID API
1. Work with GISAID to get a Data Provision Agreement. 
2. Define the following environment variables in your environment:
~~~
GISAID_URL
GISAID_USERNAME
GISAID_PASSWORD
~~~
4. Do the editions you need to fit your data if they differ from ours in [data_process.py](data_process.py)

## Running the app
Once your environment is set, run the following commands to generate the files and run the app:
1. `python data_process.py`
2. `Rscript source/dashboard_tables.R`
3. `streamlit run app.py`