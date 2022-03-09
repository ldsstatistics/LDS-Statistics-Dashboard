import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit.state.session_state import Value

def oneTraceFigure(df, name, timeRange, title=None, yaxis_title=None):
    if title is None:
        title = name
    if yaxis_title is None:
        yaxis_title = name
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df[name], mode='lines', name=name))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title=title, 
        xaxis_title='Year', 
        yaxis_title=yaxis_title, 
        xaxis={'range': timeRange},
    )
    return fig

def app():
    st.title('[Fuller Consideration Analysis](http://www.fullerconsideration.com/membership.php)')
    timeRange = st.slider('Time Range', min_value=1831, max_value=2060, value=[1900, 2020], args=Value)

    df = pd.read_csv('data/Membership Statistics - Data.csv', thousands=',')

    figures = []

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Total Membership'], mode='lines', name='Total'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Active Mormons'], mode='lines', name='Active'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Inactive Mormons'], mode='lines', name='Inactive'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Former Mormons'], mode='lines', name='Former'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Estimated Membership Distribution', 
        xaxis_title='Year', 
        yaxis_title='Membership', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': timeRange}
    )
    figures.append(fig)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Branches'], mode='lines', name='Branches'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Wards'], mode='lines', name='Wards'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Wards and Branches'], mode='lines', name='Combined'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Number of Units', 
        xaxis_title='Year', 
        yaxis_title='Number of Units', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': timeRange}
    )
    figures.append(fig)

    dfWorldPopulation = pd.read_csv('data/world-population.csv')

    membershipChange = df['Total Membership'].diff()
    previousYearMembership = df['Total Membership'] - membershipChange
    df['Membership Growth'] = membershipChange / previousYearMembership * 100

    unitChange = df['Wards and Branches'].diff()
    previousYearUnits = df['Wards and Branches'] - unitChange
    df['Wards and Branches Growth'] = unitChange / previousYearUnits * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Membership Growth'], mode='lines', name='Membership'))
    fig.add_trace(go.Scatter(x=dfWorldPopulation['End of Year'], y=dfWorldPopulation['Annual Growth Rate'], mode='lines', name='World Population'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['Wards and Branches Growth'], mode='lines', name='Wards and Branches'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Growth %', 
        xaxis_title='Year', 
        yaxis_title='Growth %', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': timeRange},
        yaxis={'range': [0, 15]}
    )
    figures.append(fig)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['New Missionaries'], mode='lines', name='Total Missionaries'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['New Male Missionaries'], mode='lines', name='Male'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['New Female Missionaries'], mode='lines', name='Female'))
    fig.add_trace(go.Scatter(x=df['End of Year'], y=df['New Senior Missionaries'], mode='lines', name='Senior'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='New Missionaries', 
        xaxis_title='Year', 
        yaxis_title='New Missionaries Per Year', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': timeRange},
    )
    figures.append(fig)

    figures.append(oneTraceFigure(df, 'Convert Baptisms', timeRange, title='Annual Number of Convert Baptisms'))
    figures.append(oneTraceFigure(df, 'Children of Record', timeRange, title='Children of Record'))

    fig = oneTraceFigure(df, 'Activity Rate', timeRange, yaxis_title='Percentage of Active Members')
    fig.update_layout(margin=dict(l=10, r=10, t=100, b=20), yaxis={'range': [5, 50]})
    figures.append(fig)

    figures.append(oneTraceFigure(df, 'Names Removed', timeRange, title='Annual Number of Names Removed'))
    figures.append(oneTraceFigure(df, 'Mormon Birth Rate', timeRange, title='LDS Birth Rate', yaxis_title='Births per 1000 Members'))

    col1, col2, col3 = st.columns(3)
    col = col1
    for fig in figures:
        with col:
            st.plotly_chart(fig, use_container_width=True)
        if col == col1:
            col = col2
        elif col == col2:
            col = col3
        else:
            col = col1