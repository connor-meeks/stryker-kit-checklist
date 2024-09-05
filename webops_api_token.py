import streamlit as st

import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
import pandas as pd   
import numpy as np
from numpy import nan

def getToken():
    # API Authentication/Token
    username = st.secrets['username']
    password = st.secrets['password']
    token_url = 'https://sandbox-api.webops.net/api/1.0/token'

    token_resp = requests.post(token_url, data={}, auth=(username, password))
    access_token = token_resp.headers.get('Access_token')

    return access_token