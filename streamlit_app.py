import streamlit as st
import webops_cases, webops_branches
import datetime
import surgery_dates

# title
st.title("Stryker Kit Checklist")

# branches request
df_branches = webops_branches.webops_branches_request()

options = st.multiselect(
    "Select branch",
    list(df_branches['branchName'])
)

branch_ids = list(df_branches[df_branches['branchName'].isin(options)]['branchId'])

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

# Refresh button to maintain selections
if st.button('Refresh'):
    st.rerun()

# cases request
if picker_start_date and picker_end_date and branch_ids:

    df_results = webops_cases.webops_cases_request(picker_start_date, picker_end_date, branch_ids)
    
    if type(df_results) is int:
        if df_results == 0:
            st.success('All kits have been completed!')
        else:
            'unknown response code'
    else:
        df_results