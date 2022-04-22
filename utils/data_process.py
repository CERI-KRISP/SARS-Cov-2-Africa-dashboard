from datetime import datetime
import time
import os, sys
import numpy as np
import requests
import lzma
import json
import pandas as pd
import streamlit as st

from utils.dicts import variant_names, variant_cutoffs, standardize_country_names
from utils.functions import lineages_to_concerned_variants

@st.experimental_memo(suppress_st_warning=True)
def process_data_from_gisaid_api(last_update):
    if abs((datetime.today() - datetime.strptime(last_update, '%Y-%m-%d')).days) > 0:
        last_update = datetime.today().strftime('%Y-%m-%d')
        from config import GISAID_URL, GISAID_USERNAME, GISAID_PASSWORD

        base_url = GISAID_URL
        username = GISAID_USERNAME
        password = GISAID_PASSWORD

        headers = {'Content-Type': 'application/json'}

        req = requests.get(base_url, headers=headers, auth=(username, password))
        print(GISAID_URL, GISAID_USERNAME, GISAID_PASSWORD)
        with open("data/gisaid_data/provision.json.xz", "wb") as file:
            file.write(req.content)

        s = lzma.open('data/gisaid_data/provision.json.xz').read().decode('utf8').replace("}", "},")
        s = s[0:-2]
        s = '[' + s + ']'
        json_data = json.loads(s)
        df = pd.DataFrame.from_dict(json_data)
        with open('data/gisaid_data/provision.json', 'w') as jsonfile:
            json.dump(json_data, jsonfile)
    else:
        with open('data/gisaid_data/provision.json', 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)

    #TODO: Criar uma função para pegar as colunas do arquivo e definir qual que é qual, independente do covv na frente
    # https://github.com/joicy/SARS-Cov-2-Africa-dashboard/projects/1#card-78707541

    #Split region columns
    df[['region', 'country','province']] = df['covv_location'].str.split('/', n=2, expand=True)
    df.drop(columns='covv_location', inplace=True)
    df['country'] = df['country'].str.lstrip()
    df['country'] = df['country'].str.rstrip()

    #Fill variant columns with lineage when is empty
    variants = []
    for index, row in df.iterrows():
        if row['covv_variant'] != '':
            variants.append(row['covv_variant'])
        else:
            variants.append(row['covv_lineage'])
    df['covv_variant'] = variants

    # Drop nones
    lineages = []
    for index, row in df.iterrows():
        if row['covv_lineage'] == 'None':
            lineages.append(np.nan)
        else:
            lineages.append(row['covv_lineage'])
    df['covv_lineage'] = lineages
    df.dropna(subset=['covv_lineage', 'country', 'covv_collection_date'], inplace=True)

    #convert to date columns
    df['covv_collection_date'] = pd.to_datetime(df['covv_collection_date'], format='%Y-%m-%d', yearfirst=True)
    df['covv_subm_date'] = pd.to_datetime(df['covv_subm_date'], format='%Y-%m-%d', yearfirst=True)

    df['date_weekly'] = df['covv_collection_date'].dt.to_period('W').apply(lambda r: r.start_time)
    df['date_2weeks'] = df['covv_collection_date'] + pd.offsets.SemiMonthEnd()
    df['date_month'] = df['covv_collection_date'].dt.to_period('M').apply(lambda r: r.start_time)

    df['date_weekly'] = df['date_weekly'].dt.strftime('%Y-%m-%d')
    df['date_2weeks'] = df['date_2weeks'].dt.strftime('%Y-%m-%d')
    df['date_month'] = df['date_month'].dt.strftime('%Y-%m-%d')

    #Standardize columns and variant names
    convert_columns = {'covv_collection_date':'collection_date', 'covv_lineage': 'lineage', 'covv_clade':'clade',
                       'covv_subm_date': 'subm_date', 'covv_variant': 'variant_GISAID_name'}
    df.rename(columns=convert_columns, inplace=True)
    df['variant'] = df['variant_GISAID_name']
    df.replace({"variant": variant_names}, inplace=True)
    df['variant'] = lineages_to_concerned_variants(df, 'variant')

    #Drop itens where collenction date is before variant_cutoff (First sampled date)
    df['voc_earliest_sample_date'] = df['variant']
    df.replace({'voc_earliest_sample_date': variant_cutoffs}, inplace=True)

    temp = []
    for index, row in df.iterrows():
        if row['voc_earliest_sample_date'] == "":
            temp.append(row['collection_date'])
        else:
            temp.append(row['voc_earliest_sample_date'])
    df['voc_earliest_sample_date'] = temp
    df['voc_earliest_sample_date'] = pd.to_datetime(df['voc_earliest_sample_date'], format='%Y-%m-%d', yearfirst=True)

    df['drop_decision'] = np.where((df['collection_date'] < df['voc_earliest_sample_date']), 'yes', 'no')
    df.drop(df[df['drop_decision'] == 'yes'].index, inplace=True)
    df.drop(['drop_decision'], axis=1, inplace=True)

    # standardize country names
    df.replace({"country": standardize_country_names}, inplace=True)
    df.to_csv("data/analyses/africa_dashboard_22_04_2022.csv", index=False)
    return df, last_update

def process_data_from_gisaid_metadata():
    df_path = "./data/metadata.csv"
    df = pd.read_csv(df_path)
    #TODO: mudar colunas para pegar as originais dos metadados e padronizar com as
    df = df[df.pangolin_lineage != 'None']
    df['variant'] = df['pangolin_lineage']
    df.replace({"variant": variant_names}, inplace=True)
    return df