import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

def app():
    st.title('LDS Prophets and Apostles')
    df = pd.read_csv('data/Prophets.csv', thousands=',', keep_default_na=False)

    df['Birth'] = pd.to_datetime(df['Birth'])
    df['Ordination'] = pd.to_datetime(df['Ordination'])
    df['Death'] = pd.to_datetime(df['Death'])

    data = {'start': [], 'end': [], 'type': [], 'President': []}
    def addRow(start, end, type, president):
        data['start'].append(start)
        data['end'].append(end)
        data['type'].append(type)
        data['President'].append(president)
    
    for i, row in df.iterrows():
        deathDate = row['Death']
        if pd.isnull(deathDate):
            deathDate = date.today()
        addRow(row['Birth'], deathDate, 'Lifespan', row['President'])
        addRow(row['Ordination'], deathDate, 'Tenure', row['President'])

    data = pd.DataFrame(data)

    fig = px.timeline(data, x_start='start', x_end='end', y='President', color='type')

    for i, d in enumerate(fig.data):
        if d.name == 'Tenure':
            d.width = 0.4

    fig.update_traces(hovertemplate='%{y}<extra></extra>')
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(
        yaxis_title='',
        title='LDS Presidents',
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1, 'title': ''},
    )
    
    st.plotly_chart(fig, use_container_width=True)

    df = pd.read_csv('data/Current Prophets.csv', keep_default_na=False)
    df['Birth'] = pd.to_datetime(df['Birth'])
    df['Ordination'] = pd.to_datetime(df['Ordination'])

    df['Age'] = (pd.to_datetime(date.today()) - df['Birth']) / np.timedelta64(1, 'Y')
    df['Tenure'] = (pd.to_datetime(date.today()) - df['Ordination']) / np.timedelta64(1, 'Y')

    st.markdown('Current First Presidency and 12 Apostles')

    col1, col2 = st.columns(2)

    df = df.sort_values('Age', ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Age'], y=df['Name'], orientation='h', name='Age'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        xaxis_title='Age',
        yaxis={'autorange': 'reversed'}
    )
    with col1:
        st.plotly_chart(fig, use_container_width=True)

    df = df.sort_values('Tenure', ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Tenure'], y=df['Name'], orientation='h', name='Tenure'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        xaxis_title='Apostolic Tenure (Years)',
        yaxis={'autorange': 'reversed'}
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    