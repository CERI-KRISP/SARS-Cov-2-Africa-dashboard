import os, sys
import numpy as np
import requests
#import lzma
import json
import pandas as pd

from utils.dicts import variant_names



def process_data_from_gisaid_api():
    from config import GISAID_URL, GISAID_USERNAME, GISAID_PASSWORD

    base_url = GISAID_URL
    username = GISAID_USERNAME
    password = GISAID_PASSWORD

    headers = {'Content-Type': 'application/json'}

    req = requests.get(base_url, headers=headers, auth=(username, password))
    print(GISAID_URL, GISAID_USERNAME, GISAID_PASSWORD)
    with open("../data/gisaid_data/provision.json.xz", "wb") as file:
        file.write(req.content)

    s = lzma.open('../data/gisaid_data/provision.json.xz').read().decode('utf8').replace("}", "},")
    s = s[0:-2]
    s = '[' + s + ']'
    json_data = json.loads(s)
    df = pd.DataFrame.from_dict(json_data)
    #TODO: Criar uma função para pegar as colunas do arquivo e definir qual que é qual, independente do covv na frente
    # https://github.com/joicy/SARS-Cov-2-Africa-dashboard/projects/1#card-78707541

    #Split region columns
    df[['region', 'country', 'city']] = df['covv_location'].str.split('/', n=2, expand=True)
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

    convert_columns = {'covv_collection_date':'collection_date', 'covv_lineage': 'lineage', 'covv_subm_date': 'subm_date',
                      'covv_variant': 'variant_GISAID_name'}
    df.rename(columns=convert_columns, inplace=True)
    df['variant'] = df['lineage']
    df.replace({"variant": variant_names}, inplace=True)
    return df
def process_data_from_gisaid_metadata():
    df_path = "./data/metadata.csv"
    df = pd.read_csv(df_path)
    #TODO: mudar colunas para pegar as originais dos metadados
    df = df[df.pangolin_lineage != 'None']
    df['variant'] = df['pangolin_lineage']
    df.replace({"variant": variant_names}, inplace=True)
    return df
