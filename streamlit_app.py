import streamlit as st
import webops_api
import datetime
import surgery_dates

st.title("Stryker Kit Checklist")

now = datetime.datetime.now()
d = st.date_input(
    "Select surgery dates",
    (surgery_dates.previous_sunday, surgery_dates.next_saturday),
    format="MM/DD/YYYY",
)

# handle empty dates
picker_start_date = d[0]
try:
    picker_end_date = d[1]
except:
    picker_end_date = picker_start_date

# api request
if picker_end_date:
    df_results = webops_api.webops_api_request(picker_start_date, picker_end_date)
    df_results