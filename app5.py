import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Temples')
    
    df = pd.read_csv('data/temples.csv', thousands=',')

    event = {
        'date': [],
        'type': []
    }
    for i in range(df.shape[0]):
        for type in ['Announcement', 'Groundbreaking', 'Dedication']:
            if not pd.isna(df[type][i]):
                event['date'].append(df[type][i])
                event['type'].append(type)

    dfEvent = pd.DataFrame(event)
    dfEvent.sort_values('date', inplace=True, ignore_index=True)

    data = {
        'date': [],
        'announced': [],
        'constructing': [],
        'completed': [] 
    }
    i = 0
    numAnnounced = 0
    numConstructing = 0
    numCompleted = 0
    for i in range(dfEvent.shape[0]):
        if dfEvent['type'][i] == 'Announcement':
            numAnnounced += 1
        elif dfEvent['type'][i] == 'Groundbreaking':
            numAnnounced -= 1
            numConstructing += 1
        elif dfEvent['type'][i] == 'Dedication':
            numConstructing -= 1
            numCompleted += 1
        
        data['date'].append(dfEvent['date'][i])
        data['announced'].append(numAnnounced)
        data['constructing'].append(numConstructing)
        data['completed'].append(numCompleted)

    dfData = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfData['date'], y=dfData['announced'], mode='lines', name='Announced'))
    fig.add_trace(go.Scatter(x=dfData['date'], y=dfData['constructing'], mode='lines', name='Under Construction'))
    fig.add_trace(go.Scatter(x=dfData['date'], y=dfData['completed'], mode='lines', name='Completed'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Temple Status',
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': ['1980-01-01', '2022-01-01']},
    )
    st.plotly_chart(fig, use_container_width=True)

    dataForTheYear = {
        'date': range(1832, 2023),
        'dateStr': [],
        'announced': [],
        'completed': [],
    }

    for date in dataForTheYear['date']:
        dataForTheYear['dateStr'].append(str(date) + '-01-01')
        dataForTheYear['announced'].append(((dfEvent['type'] == 'Announcement') & (dfEvent['date'] >= str(date)) & (dfEvent['date'] < str(date + 1))).sum())
        dataForTheYear['completed'].append(((dfEvent['type'] == 'Dedication') & (dfEvent['date'] >= str(date)) & (dfEvent['date'] < str(date + 1))).sum())

    dfDataForTheYear = pd.DataFrame(dataForTheYear)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfData['date'], y=dfData['announced'] + dfData['constructing'], mode='lines', name='Cumulative Incomplete Temples'))
    fig.add_trace(go.Scatter(x=dfDataForTheYear['dateStr'], y=dfDataForTheYear['announced'], mode='lines', name='Announced That Year'))
    fig.add_trace(go.Scatter(x=dfDataForTheYear['dateStr'], y=dfDataForTheYear['completed'], mode='lines', name='Completed That Year'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Temple Building Backlog',
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': ['1980-01-01', '2022-01-01']},
    )
    st.plotly_chart(fig, use_container_width=True)