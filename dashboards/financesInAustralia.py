import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    charities = {
        'The Church Of Jesus Christ Of Latter-day Saints Australia': 'df8937d2-38af-e811-a95e-000d3ad24c60',
        'LDS Charities Australia': '30f0a550-3aaf-e811-a963-000d3ad24077',
        'The Trustee For The L.D.S. Fast Offering Fund': 'd6e7cd3e-38af-e811-a95e-000d3ad24c60',
        'The Trustee For L.D.S. Educational Building Fund': '4ebff745-38af-e811-a960-000d3ad24282',
        'L.D.S. Charitable Trust Fund': '357ae4a8-38af-e811-a962-000d3ad24a0d',
    }
    charityName = st.selectbox('Select Registered Charity', charities.keys())
    st.title(charityName)
    
    df = pd.read_csv('data/Finances/{}.csv'.format(charityName), thousands=',')

    fig = go.Figure()
    for column in df.columns:
        if 'Revenue-' in column:
            fig.add_trace(go.Bar(x=df['Year'], y=df[column], name=column.split('-')[1]))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Revenue',
        xaxis_title='Year', 
        yaxis_title='Amount $', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        barmode='stack',
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    for column in df.columns:
        if 'Expenses-' in column:
            fig.add_trace(go.Bar(x=df['Year'], y=df[column], name=column.split('-')[1]))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Expenses',
        xaxis_title='Year', 
        yaxis_title='Amount $', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        barmode='stack',
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Total Revenue']-df['Total Expenses'], name='Income'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Profit/Loss (Revenue - Expenses)',
        xaxis_title='Year', 
        yaxis_title='Amount $', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    )
    st.plotly_chart(fig, use_container_width=True)

    if 'Trust' in charityName:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Year'], y=df['Total Trust Funds'], name='Total Trust Funds'))
        fig.update_layout(
            margin=dict(l=10, r=10, t=100, b=20),
            title='Total Trust Funds',
            xaxis_title='Year', 
            yaxis_title='Amount $', 
            legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('See [Australian Charities and Not-for-profits Commission](https://www.acnc.gov.au/charity/charities/{}/profile)'.format(charities[charityName]))
