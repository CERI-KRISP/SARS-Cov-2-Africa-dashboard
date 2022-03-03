import os, sys

import numpy as np
import requests
import lzma
import json
import pandas as pd

def process_data_from_gisaid_api():
    #Check environment variables
    try:
        os.environ["GISAID_URL"]
    except KeyError:
        print("Please set the environment variable GISAID_URL")
        sys.exit(1)

    try:
        os.environ["GISAID_USERNAME"]
    except KeyError:
        print("Please set the environment variable GISAID_USERNAME")
        sys.exit(1)

    try:
        os.environ["GISAID_PASSWORD"]
    except KeyError:
        print("Please set the environment variable GISAID_PASSWORD")
        sys.exit(1)

    base_url = os.environ.get('GISAID_URL')
    username = os.environ.get('GISAID_USERNAME')
    password = os.environ.get('GISAID_PASSWORD')

    headers = {'Content-Type': 'application/json'}

    req = requests.get(base_url, headers=headers, auth=(username, password))
    with open("../data/gisaid_data/provision.json.xz", "wb") as file:
        file.write(req.content)

    s = lzma.open('../data/gisaid_data/provision.json.xz').read().decode('utf8').replace("}", "},")
    s = s[0:-2]
    s = '[' + s + ']'
    json_data = json.loads(s)
    df = pd.DataFrame.from_dict(json_data)

    #Split region columns
    df[['continent', 'country', 'city']] = df['covv_location'].str.split('/', n=2, expand=True)
    df.drop(columns='covv_location', inplace=True)

    #Fill variant columns with lineage when is empty
    variants = []
    for index, row in df.iterrows():
        if row['covv_variant'] != '':
            variants.append(row['covv_variant'])
        else:
            variants.append(row['covv_lineage'])
    df['covv_variant'] = variants

    #convert to date columns
    df['covv_subm_date'] = pd.to_datetime(df['covv_subm_date'], format='%Y-%m-%d', yearfirst=True)

    df['date_weekly'] = df['covv_subm_date'].dt.to_period('W').apply(lambda r: r.start_time)
    df['date_2weeks'] = df['covv_subm_date'] + pd.offsets.SemiMonthEnd()
    df['date_month'] = df['covv_subm_date'].dt.to_period('M').apply(lambda r: r.start_time)

    #Drop nones
    lineages = []
    for index, row in df.iterrows():
        if row['covv_lineage'] == 'None':
            lineages.append(np.nan)
        else:
            lineages.append(row['covv_lineage'])
    df['covv_lineage'] = lineages
    df.dropna(subset=['covv_lineage'], inplace=True)
    return df
process_data_from_gisaid_api()