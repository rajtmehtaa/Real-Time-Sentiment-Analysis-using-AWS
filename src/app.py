#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit dashboard showing guardian posts and their trend!
"""

import datetime

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder

from lambda_.lambda_function_guardian import get_db_connection


@st.cache(suppress_st_warning=True)
def get_data(start_date: str = '2024-12-04',
             end_date: str = '2024-12-05') -> pd.DataFrame:
    """
    Get data from the database within the specified date range.
    This function is cached for better performance.
    """
    conn = get_db_connection()
    # query the database with start and end data
    sql = f"""SELECT * FROM guardian_posts_analytics
              WHERE timestamp BETWEEN date('{start_date}') AND date('{end_date}')
           """
    print(sql)
    df = pd.read_sql_query(sql, conn)
    return df.copy()  # Returning a copy to prevent mutation issues


def get_local_tz() -> datetime.timezone:
    """Get the local timezone."""
    return datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


@st.cache(suppress_st_warning=True)
def process_data(df: pd.DataFrame,
                 keyword: str,
                 start_date: str,
                 end_date: str) -> pd.DataFrame:
    """
    Process the dataframe by filtering based on keyword and converting to the local timezone.
    """
    local_tz = get_local_tz()
    df = df.copy()  # Avoid mutating the cached dataframe
    df['timestamp'] = df['timestamp'].dt.tz_convert(local_tz)
    if keyword:
        df = df[df['text'].str.contains(keyword, case=False, na=False)]

    # Avoid displaying 10 decimal places
    df['sentiment_score'] = df['sentiment_score'].round(2)
    df = df.reindex(columns=['timestamp', 'sentiment_score', 'text'])

    return df


def display_table(df: pd.DataFrame) -> None:
    """
    Display the dataframe in an interactive table using st-aggrid.
    """
    # this is some javascript code
    # to color cells
    # positive -> green, neuter -> white negative -> red
    sentiment_score_style = JsCode("""
    function(params) {
        if (params.value < 0) {
            return {
                'color': 'black',
                'backgroundColor': 'darkred'
            }
        } else if (params.value == 0) {
            return {
                'color': 'black',
                'backgroundColor': 'gray'
            }
        } else {
            return {
                'color': 'black',
                'backgroundColor': 'green'
            }
        }
    };
    """)
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("sentiment_score", cellStyle=sentiment_score_style)

    AgGrid(df, height=500, width='100%', gridOptions=gb.build(), allow_unsafe_jscode=True)


st.set_page_config(layout="wide")

print('If this is printed and the app is not running on the public IP, check port mappings and security group inbound rules')
if __name__ == "__main__":

    # Here we define the layout of the sidebar
    st.title('Guardian Posts Analytics Sentiment Score Dashboard')
    view_name = st.sidebar.radio("Choose View", ('View Posts', 'Analytics'))
    keyword = st.sidebar.text_input("Keyword Filter", "")
    start_date = st.sidebar.date_input("Starting Date", datetime.date(2024, 12, 4))
    end_date = st.sidebar.date_input("End Date", datetime.date(2024, 12, 5))
    
    st.sidebar.subheader('Explanation')
    st.sidebar.markdown('''
                        **Sentiment score indicates a positive sentiment
                        when the sentiment is positive and conversely,
                        when the score is negative the sentiment is also negative.**  
                        ***Consider that scores above 0.2 or below -0.2 are a
                         small part and can therefore be seen as very positive 
                         or very negative.***
                         ''')

    # Fetch and process data
    df = get_data(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
    df = process_data(df, keyword=keyword, start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))

    # Error handling for no data
    if df.empty:
        st.error('Your search parameters resulted in no data!')
    else:
        if view_name == 'View Posts':
            display_table(df)
        else:
            # Analytics view
            st.markdown(f"**Sentiment Score Over Time**")
            keyword_info = f"Keyword: {keyword}" if keyword else ""
            st.markdown(f"{keyword_info}, Start Date: {start_date}, End Date: {end_date}")
            
            # Plot sentiment over time
            df = df.set_index('timestamp')
            st.line_chart(df['sentiment_score'])
