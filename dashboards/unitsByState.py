import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Units by State')
    col1, col2 = st.columns([1, 3])

    years = ['2021', '2020', '2019', '2018']
    unitTypes = ['Wards & Branches', 'Wards', 'Branches', 'Districts', 'Stakes', 'Missions', 'Temples']

    with col1:
        yearSelected = st.radio('Year', years)
        unitTypeSelected = st.radio('Unit Type', unitTypes)

    df = {}
    for year in years:
        df[year] = pd.read_csv('data/Units by state/Units by State {}.csv'.format(year), thousands=',')
    
    data = df[yearSelected].sort_values(unitTypeSelected, ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data[unitTypeSelected][0:15], y=data['State'][0:15], orientation='h'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        xaxis_title=unitTypeSelected,
        yaxis={'autorange': 'reversed'}
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    if yearSelected != years[-1]:
        states = df[yearSelected]['State']
        for i in range(len(years)):
            if yearSelected == years[i]:
                dfPrev = df[years[i+1]]
        df[yearSelected]['Unit Growth'] = 0
        df[yearSelected]['Unit Growth Percentage'] = 0
        for state in states:
            growth = 0
            selectedNumOfUnits = int(df[yearSelected].loc[df[yearSelected]['State'] == state, unitTypeSelected])
            if (dfPrev['State'] == state).any():
                previousNumOfUnits = int(dfPrev.loc[dfPrev['State'] == state, unitTypeSelected])
                if previousNumOfUnits > 0:
                    growth = (selectedNumOfUnits - previousNumOfUnits)
                    growthPerc = growth / previousNumOfUnits * 100
                    df[yearSelected].loc[df[yearSelected]['State'] == state, 'Unit Growth'] = growth
                    df[yearSelected].loc[df[yearSelected]['State'] == state, 'Unit Growth Percentage'] = growthPerc
        
        col1, col2 = st.columns(2)

        data = df[yearSelected].sort_values('Unit Growth', ascending=False)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['Unit Growth'][0:15], y=data['State'][0:15], orientation='h'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=20),
            xaxis_title=unitTypeSelected + ' Growth',
            yaxis={'autorange': 'reversed'}
        )
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        
        data = df[yearSelected].sort_values('Unit Growth Percentage', ascending=False)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['Unit Growth Percentage'][0:15], y=data['State'][0:15], orientation='h'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=20),
            xaxis_title=unitTypeSelected + ' Growth %',
            yaxis={'autorange': 'reversed'}
        )
        with col2:
            st.plotly_chart(fig, use_container_width=True)

        data = df[yearSelected].sort_values('Unit Growth')
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['Unit Growth'][0:15], y=data['State'][0:15], orientation='h'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=20),
            xaxis_title=unitTypeSelected + ' Decline',
            yaxis={'autorange': 'reversed'}
        )
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        
        data = df[yearSelected].sort_values('Unit Growth Percentage')
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['Unit Growth Percentage'][0:15], y=data['State'][0:15], orientation='h'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=20),
            xaxis_title=unitTypeSelected + ' Decline %',
            yaxis={'autorange': 'reversed'}
        )
        with col2:
            st.plotly_chart(fig, use_container_width=True)
