import streamlit as st
import webops_cases, webops_branches
import datetime
import surgery_dates

# title
st.title("Stryker Kit Checklist")

# date picker
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

# cases request
if picker_end_date:
    df_results = webops_cases.webops_cases_request(picker_start_date, picker_end_date)
    
    if type(df_results) is int:
        if df_results == -1:
            st.success('All kits have been completed!')
        else:
            'unknown response code'
    else:
        df_results

# branches request
df_branch = webops_branches.webops_branches_request()
df_branch 