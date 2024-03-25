import streamlit as st
import pandas as pd
import plotly.express as px
from helper import Color, make_table, compare, colorize


data_sentiment_ranked = pd.read_csv("sentiment_ranked.csv", index_col=False)
data_sentiment_ranked['Date'] = pd.to_datetime(data_sentiment_ranked['Date']).dt.strftime('%Y-%m-%d')


data_created_profiles = pd.read_csv("created_profiles.csv", index_col=False)
data_ranked_profiles = pd.read_csv("ranked_profiles.csv", index_col=False) 


st.set_page_config(layout="wide")


plotly  = st.container()
left, right = st.columns(2)
scatter = st.container()
rank_compare = st.container()
col1, col2 = st.columns(2)


with plotly:
    with left:     
        st.header("Create Profiles")
        st.dataframe(data_created_profiles, hide_index=True)
    with right:
        st.header("Ranked Profiles")
        st.dataframe(data_ranked_profiles, hide_index=True)


with rank_compare:
    valid_dates = []
    b_date = None
    b_data = None
    a_date = None
    a_data = None
    st.header("Rank Compare")
        
    with col1:        
        b_date = st.selectbox("Before Date", options=data_sentiment_ranked['Date'].unique(), index=len(data_sentiment_ranked['Date'].unique().tolist())-1)

        if(b_date):
            b_data = data_sentiment_ranked[data_sentiment_ranked['Date'] == b_date][['Position', 'Link', 'Status']]
            st.dataframe(b_data.style.apply(colorize, df=b_data), use_container_width=True, hide_index=True)
            st.write("Before")
            fig = px.pie(
                b_data, names="Status", color="Status",
                color_discrete_map={
                    'Positive':Color.green,
                    'Negative':Color.red,
                    'Other':Color.grey,
                    'other':Color.grey,
                    })
            st.plotly_chart(fig,use_container_width=True)

    with col2:
        if((b_date)):
            valid_date_df = data_sentiment_ranked[data_sentiment_ranked['Date'] > b_date]
            valid_dates = valid_date_df['Date'].unique()
            a_date = st.selectbox("After Date", options=valid_dates, index=None)
            
            if(a_date):
                a_data = data_sentiment_ranked[data_sentiment_ranked['Date'] == a_date][['Position', 'Link', 'Status']]
                compared_data = compare(a_data, b_data)
                st.dataframe(a_data.style.apply(colorize, df=a_data), column_order=("Position", "Link","Change"), use_container_width=True, hide_index=True)
                st.write("After")
                fig = px.pie(a_data, names="Status",color="Status",
                             color_discrete_map={
                                 'Positive':Color.green,
                                 'Negative':Color.red,
                                 'Other':Color.grey,
                                 'other':Color.grey,
                                 })
                st.plotly_chart(fig,use_container_width=True)

