import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import atleto_model as am
from datetime import datetime

st.markdown( "# Annual")
st.sidebar.markdown( "# Annual")

runs = am.model(alldata=True)
runs['Date'] = pd.to_datetime(runs['Date'], format='%Y-%m-%d')
minyear = runs['Date'].min().year
maxyear = runs['Date'].max().year

years = st.sidebar.slider('Select year range', minyear, maxyear, (minyear, maxyear))

years = range(years[0], years[1] + 1, 1)
distances = []
paces = []

for y in years:
    startdate = datetime( y, 1, 1, 0, 0, 0)
    enddate = datetime( y, 12, 31, 0, 0, 0)
    mask = (runs['Date'] >= startdate) & (runs['Date'] <= enddate)
    yr = runs.loc[mask]
    d = round(yr['Distance'].sum() * 0.001)
    t = yr['Time'].sum()
    p = datetime.strptime( '2000-01-01 00:' + am.pace( t, d), '%Y-%m-%d %H:%M:%S').time()
    distances.append( d)
    paces.append( p)

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Bar(x=[*years], y=distances, name="Distance"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=[*years], y=paces, name="Pace"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Distance and Pace per year"
)

# Set x-axis title
#fig.update_xaxes(title_text="xaxis title")

# Set y-axes titles
fig.update_yaxes(title_text="Distance", secondary_y=False)
fig.update_yaxes(title_text="Pace", secondary_y=True)

st.plotly_chart(fig)




