import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

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
        xaxis={'range': ['1980-01-01', '2022-11-01']},
    )
    st.plotly_chart(fig, use_container_width=True)

    dataForTheYear = {
        'date': range(1832, 2023),
        'dateStr': [],
        'announced': [],
        'completed': [],
    }

    for year in dataForTheYear['date']:
        dataForTheYear['dateStr'].append(str(year) + '-01-01')
        dataForTheYear['announced'].append(((dfEvent['type'] == 'Announcement') & (dfEvent['date'] >= str(year)) & (dfEvent['date'] < str(year + 1))).sum())
        dataForTheYear['completed'].append(((dfEvent['type'] == 'Dedication') & (dfEvent['date'] >= str(year)) & (dfEvent['date'] < str(year + 1))).sum())

    dfDataForTheYear = pd.DataFrame(dataForTheYear)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfData['date'], y=dfData['announced'] + dfData['constructing'], mode='lines', name='Cumulative Incomplete Temples'))
    fig.add_trace(go.Scatter(x=dfDataForTheYear['dateStr'], y=dfDataForTheYear['announced'], mode='lines', name='Announced That Year'))
    fig.add_trace(go.Scatter(x=dfDataForTheYear['dateStr'], y=dfDataForTheYear['completed'], mode='lines', name='Completed That Year'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Temple Building Backlog',
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': ['1980-01-01', '2022-11-01']},
    )
    st.plotly_chart(fig, use_container_width=True)

    dfPresidents = pd.read_csv('data/Prophets.csv')
    dfPresidents['Ordination'] = pd.to_datetime(dfPresidents['Ordination'])
    dfPresidents['Death'] = pd.to_datetime(dfPresidents['Death'])
    df['Announcement'] = pd.to_datetime(df['Announcement'])
    df['Dedication'] = pd.to_datetime(df['Dedication'])

    templeStatusCount = {'President': [], 'Announced': [], 'Completed': [], 'Announced and Completed': []}

    for i, row in dfPresidents.iterrows():
        templeStatusCount['President'].append(row['President'])
        isAnnounced = df['Announcement'] > row['Ordination']
        isDedicated = df['Dedication'] > row['Ordination']
        if not pd.isnull(row['Death']):
            isAnnounced &= df['Announcement'] < row['Death']
            isDedicated &= df['Dedication'] < row['Death']
        else:
            isAnnounced &= df['Announcement'] < pd.to_datetime(date.today())
            isDedicated &= df['Dedication'] < pd.to_datetime(date.today())
        templeStatusCount['Announced'].append(len(df[isAnnounced]))
        templeStatusCount['Completed'].append(len(df[isDedicated]))
        templeStatusCount['Announced and Completed'].append(len(df[isAnnounced & isDedicated]))

    templeStatusCount = pd.DataFrame(templeStatusCount)
    templeStatusCount = templeStatusCount.sort_values(by=['Announced'], ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=templeStatusCount['Announced'][:6], y=templeStatusCount['President'][:6], orientation='h', name='Announced'))
    fig.add_trace(go.Bar(x=templeStatusCount['Completed'][:6], y=templeStatusCount['President'][:6], orientation='h', name='Completed'))
    fig.add_trace(go.Bar(x=templeStatusCount['Announced and Completed'][:6], y=templeStatusCount['President'][:6], orientation='h', name='Announced and Completed', offset=-0.15, width=0.3))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Number of Temples Announced and Completed During Tenure as President',
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        yaxis={'autorange': 'reversed'},
        xaxis_title='Number of Temples',
        barmode='group',
    )
    st.plotly_chart(fig, use_container_width=True)
    