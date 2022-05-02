# SARS-COV-2 Africa dashboard
Repository contains code and files to interactive genomics Africa Dashboard

## How to install:
1. `conda env create -f requirements.yml`
2. `conda (or source) activate SARS-Cov-2-Africa-dashboard`
3. `streamlit run app.py`

## Data
You can run the dashboard using your own data or setting up GISAID API.
### Using metadata
1. Edit config.py and set `data_source` variable with your option: `data_source="metadata"`
2. Create your metadata based on [data/template_metadata.csv](data/template_metadata.csv) and save in `./data/metadata.csv`

### Using API
1. Edit config.py and set `data_source` variable with your option: `data_source="GISAID_API"`
2. Work with GISAID to get a Data Provision Agreement. 
3. Define the following environment variables in config.py:
~~~
GISAID_URL
GISAID_USERNAME
GISAID_PASSWORD
~~~
4. Do the editions you need to fit your data if they differ from ours in [source/data_process.py](source/data_process.py)