import streamlit as st

import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
import pandas as pd   
import numpy as np
from numpy import nan

import webops_api_token

def webops_api_request(picker_start_date, picker_end_date):

    picker_start_date = picker_start_date.strftime('%Y-%m-%d') + ' 00:00'
    picker_end_date = picker_end_date.strftime('%Y-%m-%d') + ' 23:59'

    # API Authentication/Token
    username = st.secrets['username']
    password = st.secrets['password']
    access_token = webops_api_token.getToken()

    # API Request
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    now_id = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    url = 'https://sandbox-api.webops.net/api/1.0/cases'

    data = {}
    data['timestamp']= now
    data['messageId'] = now_id
    data['manufacturerId']= '1015'
    data['branchId'] = '140'
    data['caseStatuses'] = 'Kits Assigned'
    # data['surgeryDateMin'] = '2024-08-11 00:00'
    # data['surgeryDateMax'] = '2024-08-17 00:00'
    data['surgeryDateMin'] = picker_start_date
    data['surgeryDateMax'] = picker_end_date
    # data['ids'] = '24243968'
    data['includeProductSystems'] = True
    data['limit'] = '500'
    data['page'] = '1'

    headers = {}
    headers['Access_token'] = access_token

    # request
    res = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(username, password))
    res.content

    # convert to json
    res_json = json.loads(res.content.decode('utf-8'))

    # convert json to df
    df = pd.json_normalize(res_json)

    # Explode series
    df = df.explode('cases')

    # ---

    # check if results
    if type(df.cases[0]) is float: 
        return -1
    else:
        # convert to string
        df['cases'] = df['cases'].astype(str) 

        # map nested columns
        df['cases'] = df['cases'].map(lambda x: eval(x) if pd.notnull(x) else x)
        df = pd.concat([df, df.pop('cases').apply(pd.Series)], axis=1)

        # ---

        # Explode series
        df = df.explode('productSystems')

        # convert to string
        df['productSystems'] = df['productSystems'].astype(str) 

        # map nested columns
        df['productSystems'] = df['productSystems'].map(lambda x: eval(x) if pd.notnull(x) else x)
        df = pd.concat([df, df.pop('productSystems').apply(pd.Series)], axis=1)

        # ---

        # Explode series
        df = df.explode('kitFamilies')

        # convert to string
        df['kitFamilies'] = df['kitFamilies'].astype(str) 

        # map nested columns
        df['kitFamilies'] = df['kitFamilies'].map(lambda x: eval(x) if pd.notnull(x) else x)
        df = pd.concat([df, df.pop('kitFamilies').apply(pd.Series)], axis=1)

        # ---

        # detect Assigned Kits
        if 'kitId' in df:
            df['kitAssigned'] = np.where(df['kitId'].isnull(), False, True)
        else:
            df['kitAssigned'] = False

        # results
        df_results = df[df['kitAssigned'] == True]
        df_results = df_results[['branchId', 'id', 'surgeryDate', 'caseType', 'name', 'kitAssigned']]
        df_results['id'] = df_results['id'].astype(str)
        df_results = df_results.rename(columns={'id': 'caseId', 'name': 'kitName'})

        return df_results