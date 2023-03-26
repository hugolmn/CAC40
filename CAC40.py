import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import gspread
from google.oauth2 import service_account

st.title('CAC40')

scope = ['https://www.googleapis.com/auth/drive.readonly']
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)

gc = gspread.authorize(credentials)
sh = gc.open_by_key('1Qz17RZKBO-iHOI_sJ6lAYkUPdyq_00I6dxeQqMMjKlo')

df = pd.DataFrame(sh.worksheet('Data').get_all_records())
df = df[df.Scope == 'Per employee']

profit_sharing = pd.pivot_table(df, index=['Company', 'Year'], columns='Type', values='Value').reset_index()

st.altair_chart(
    alt.Chart(profit_sharing).mark_bar().encode(
        x=alt.X('Year:O'),
        y=alt.Y('Participation:Q'),
        color=alt.Color('Year:O'),
        column=alt.Column('Company:N', header=alt.Header(title=None, labelOrient='bottom'))
    )
)
