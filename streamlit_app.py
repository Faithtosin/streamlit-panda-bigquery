# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
import pandas_gbq

# Set credentials and project_id.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
project_id = st.secrets["gcp_service_account"]["project_id"]

# Update the in-memory credentials cache (added in pandas-gbq 0.7.0).
pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = project_id



# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)

# Perform query.
def run_query():
    sql = """SELECT * FROM `{0}.sample.shakespeare` LIMIT 10""".format(project_id)
    df = pandas_gbq.read_gbq(sql) 
    return df

data_frame = run_query()

# Print results.
st.write("Some wise words from Shakespeare:")
st.dataframe(data_frame)