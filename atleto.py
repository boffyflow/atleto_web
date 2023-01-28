import streamlit as st
import jdutil as jd
from datetime import time
import sqlite3
import math
import pandas as pd

class aveHR:
    def __init__(self):
        self.tdist = 0
        self.hr = 0

    def step(self, hr, dist):
        self.hr += hr * dist
        self.tdist += dist

    def finalize(self):
        return self.hr / self.tdist

def jdate(day):

    datet = jd.jd_to_datetime(day)
    return datet.strftime( '%Y-%m-%d')

def pace(t, dist):
    secs = t / (dist * 0.001)
    mins = math.floor( secs / 60)
    secs = secs - mins * 60
    if round(secs) > 59:
        secs = 0
        mins = mins + 1    
    
    timet = time( 0, mins, round(secs))
    return timet.strftime( '%M:%S')

def main():

    st.sidebar.markdown( "# Summary")
    nruns = st.sidebar.number_input(min_value=1,max_value=50,value=20,label='Number of runs:')
    tablefontsize = st.sidebar.number_input(min_value=10,max_value=30,value=16,label='Table font size:')

    st.markdown( "# Overall Stats")
    st.markdown( "# Last " + str(nruns) + " Runs")

    st.markdown( "<style scoped> table {font-size:" + str(tablefontsize) + "px;} </style>", unsafe_allow_html=True)

    conn = sqlite3.connect("atleto_data.atl")
    conn.create_function('jdate', 1, jdate)
    conn.create_function('pace', 2, pace)
    conn.create_aggregate('avehr', 2, aveHR)

    sqlite3.enable_callback_tracebacks(True) 

    runs = pd.read_sql_query("SELECT jdate(day) AS Date,SUM(dist) AS Distance,\
                                SUM(t) AS Time,PACE(SUM(t),SUM(dist)) AS Pace,\
                                AVEHR(hr,dist) AS Heartrate\
                                FROM run_splits\
                                INNER JOIN runs\
                                ON runs.id=run_splits.run_id\
                                GROUP BY run_splits.run_id\
                                ORDER BY day ASC", conn)
    runs.set_index('Date',inplace=True)

    st.table(runs[-nruns:][::-1])
    st.markdown( 'Number of runs: **:blue[' + str(runs.size) + ']**, Last run on: ')
    st.text( '\xA9 2022 Robert Uebbing')

if __name__ == '__main__':
    main() 



