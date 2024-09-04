import streamlit as st
import webops_api

st.title("Stryker Kit Checklist")

st.dataframe(webops_api.df_results, use_container_width=True)