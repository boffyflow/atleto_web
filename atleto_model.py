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

    if round(dist) == 0:
        return "00:00"

    mins = math.floor( secs / 60)
    secs = secs - mins * 60
    if round(secs) > 59:
        secs = 0
        mins = mins + 1
    
    return time( 0, mins, round(secs)).strftime( '%M:%S')


def sec2hms( t):

    hours = math.floor( t / 3600)
    mins = math.floor(( t - hours * 3600)/60)
    secs = t - hours * 3600 - mins * 60

    timet = time( hours, mins, round(secs))

    s = timet.strftime( '%M:%S m:s') if hours == 0 else timet.strftime( '%H:%M:%S h:m:s')

    if s.startswith( '0'):
        s = s[1:]

    return s


def trimpace(p):

    s = str(p)
    if s.startswith('0'):
        s = s[1:]
    
    return s + ' min/km'


def roundtime(t):

    timet = time.fromisoformat( t)
    return timet.strftime( 'at %H:%M')


def meter2km(x):
    return str(round(x * 0.001, 1)) + ' km'


def model(alldata=True, startdate='2000-01-01', enddate='2010-12-31'):

    conn = sqlite3.connect("atleto_data.atl")
    conn.create_function('jdate', 1, jdate)
    conn.create_function('pace', 2, pace)
    conn.create_aggregate('avehr', 2, aveHR)

    sqlite3.enable_callback_tracebacks(True) 

    splits = pd.read_sql_query("SELECT jdate(day) AS Date,SUM(dist) AS Distance,\
                                SUM(t) AS Time, pace(SUM(t),SUM(dist)) AS Pace,\
                                AVEHR(hr,dist) AS Heartrate, run_splits.run_id\
                                FROM run_splits\
                                INNER JOIN runs\
                                ON runs.id=run_splits.run_id\
                                GROUP BY run_splits.run_id\
                                ORDER BY day ASC", conn)

    run_meta = pd.read_sql_query( "SELECT runs.id, locations.name AS Location, run_types.name AS Effort, starttime AS TimeOfDay, endtime FROM runs\
                                INNER JOIN locations ON runs.location_id=locations.id\
                                INNER JOIN run_types ON runs.runtype_id=run_types.id", conn)

    runs = pd.merge(splits, run_meta, left_on='run_id', right_on='id')
    runs['TimeOfDay'] = runs['TimeOfDay'].apply(roundtime)

#    print(runs.tail(20))

    return runs