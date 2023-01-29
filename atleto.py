import streamlit as st
import jdutil as jd
from datetime import time
import sqlite3
import math
import pandas as pd
import atleto_model as am

def main():

    # General page and sidebar

    st.markdown( "# Welcome to Atleto Reports")
    nruns = st.sidebar.slider(min_value=1,max_value=50,value=20,label='Number of most recent runs:')
    st.markdown( "<style scoped> table {font-size:15px;} </style>", unsafe_allow_html=True)

    # data model

    runs = am.model(alldata=True)
    runs.drop(['Heartrate','run_id','id','endtime'], axis=1, inplace=True)
    runs.rename( columns= {'TimeOfDay': 'Time of day'}, inplace=True)
    runs['Distance'] = runs['Distance'].apply(am.meter2km)
    runs['Time'] = runs['Time'].apply(am.sec2hms)
    runs['Pace'] = runs['Pace'].apply(am.trimpace)

    # first row and index colume from display
    hide_table_row_index = """
                <style>
                thead tr {display:none}
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Stats table

    st.markdown( "### Overall Stats")

    stats = {
        'Number of runs': len(runs.index),
        'Total distance': 132223.2,
        'Total time spent running': '111 days 3 hours 9 minutes 16 seconds',
        'Average pace': '5:03 min/km',
        'Average distance per run': '11.2 km',
        'Average time per run': '0 hours 56 minutes 44 seconds'
    }
    st.table(stats.items())

    # Last runs

    st.markdown( "### Last " + str(nruns) + " Runs")
    st.table(runs[-nruns:][::-1])

    # Footer

    st.markdown( 'Number of runs: **:blue[' + str(len(runs.index)) + 
                    ']**, last run on: **:blue[' + runs['Date'].max() + ']**')
    st.text( '\xA9 2022 Robert Uebbing')


if __name__ == '__main__':
    main() 



