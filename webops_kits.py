import streamlit as st

import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
import pandas as pd   
import numpy as np
from numpy import nan

import webops_api_token

def webops_kits_request(kit_ids):
    
    # API Authentication/Token
    username = st.secrets['username']
    password = st.secrets['password']
    access_token = webops_api_token.getToken()

    # API Request
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    now_id = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    url = 'https://sandbox-api.webops.net/api/1.0/kits'

    data = {}
    data['timestamp']= now
    data['messageId'] = now_id
    data['manufacturerId']= '1015'
    data['ids'] = kit_ids
    data['limit'] = '500'
    data['page'] = '1'

    headers = {}
    headers['Access_token'] = access_token

    # request
    res = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(username, password))
    res.content

    # convert to json
    res_json = json.loads(res.content.decode('utf-8'))
    res_json

    # convert json to df
    df = pd.json_normalize(res_json)

    # Explode series
    df = df.explode('kits')

    # convert to string
    df['kits'] = df['kits'].astype(str) 

    # map nested columns
    df['kits'] = df['kits'].map(lambda x: eval(x) if pd.notnull(x) else x)
    df = pd.concat([df, df.pop('kits').apply(pd.Series)], axis=1)

    # kit lookup df
    df_kits = df[['kitId','kitName']]
    df_kits['kitId'] = df_kits['kitId'].astype(str).str.split('.', expand = True)[0]

    # results
    return df_kits