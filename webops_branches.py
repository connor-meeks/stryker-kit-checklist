import streamlit as st

import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
import pandas as pd   
import numpy as np
from numpy import nan

import webops_api_token

def webops_branches_request():

    # API Authentication/Token
    username = st.secrets['username']
    password = st.secrets['password']
    access_token = webops_api_token.getToken()

    # API Request
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    now_id = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    url = 'https://sandbox-api.webops.net/api/1.0/branches'

    data = {}
    data['timestamp']= now
    data['messageId'] = now_id
    data['manufacturerId']= '1015'
    data['limit'] = 500

    headers = {}
    headers['Access_token'] = access_token

    # request
    res = requests.post(url, json=data, headers=headers, auth=HTTPBasicAuth(username, password))

    # convert to json
    res_json = json.loads(res.content.decode('utf-8'))

    # convert json to df
    df = pd.json_normalize(res_json)

    # Explode series
    df = df.explode('branches')

    # convert to string
    df['branches'] = df['branches'].astype(str) 

    # map nested columns
    df['branches'] = df['branches'].map(lambda x: eval(x) if pd.notnull(x) else x)
    df = pd.concat([df, df.pop('branches').apply(pd.Series)], axis=1)

    # Only active branches
    df_branches = df[df['active'] == True]

    # Get columns needed
    df_branches = df_branches[['id','name']].rename(columns={"id": "branchId", "name": "branchName"})

    # Results
    return df_branches