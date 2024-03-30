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


def data_description(data:pd.DataFrame):
    n_positive = len(data[data['Status'] == 'Positive'])
    n_negative = len(data[data['Status'] == 'Negative'])
    n_others = len(data.query('Status!="Positive" & Status!="Negative"'))
    return f"In the Top :blue[{len(data)}] of the search engine result page at the given date, there are :red[{n_negative}] unfavorable links and :green[{n_positive}] positive. Remaining are :orange[{n_others}] neutral links"

def generate_pie(bfr_data):
    fig = px.pie(
                bfr_data, names="Status", color="Status",
                color_discrete_map={
                    'Positive':Color.green,
                    'Negative':Color.red,
                    'Other':Color.grey,
                    'other':Color.grey,
                })
    return fig

with rank_compare:
    valid_dates = []
    bfr_date = None
    bfr_data = None
    aftr_date = None
    aftr_data = None
    st.header("Rank Compare")
        
    with col1:        
        bfr_date = st.selectbox("Before Date", options=data_sentiment_ranked['Date'].unique(), index=len(data_sentiment_ranked['Date'].unique().tolist())-1)

        if(bfr_date):
            bfr_data = data_sentiment_ranked[data_sentiment_ranked['Date'] == bfr_date][['Position', 'Link', 'Status']]
            st.write("Before")
            st.caption(data_description(bfr_data))
            fig = generate_pie(bfr_data)
            st.plotly_chart(fig,use_container_width=True)
            
            st.dataframe(bfr_data.style.apply(colorize, df=bfr_data), use_container_width=True, hide_index=True)
            
            

    with col2:
        if((bfr_date)):
            valid_date_df = data_sentiment_ranked[data_sentiment_ranked['Date'] > bfr_date]
            valid_dates = valid_date_df['Date'].unique()
            aftr_date = st.selectbox("After Date", options=valid_dates, index=None)
            
            if(aftr_date):
                aftr_data = data_sentiment_ranked[data_sentiment_ranked['Date'] == aftr_date][['Position', 'Link', 'Status']]
                compared_data = compare(aftr_data, bfr_data)                
                st.write("After")
                st.caption(data_description(aftr_data))
                fig = generate_pie(aftr_data)

                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(aftr_data.style.apply(colorize, df=aftr_data), column_order=("Position", "Link","Change"), use_container_width=True, hide_index=True)