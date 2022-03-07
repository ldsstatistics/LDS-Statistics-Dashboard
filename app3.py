import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Finances in Canada')
    
    df = pd.read_csv('data/LDS Church Finances Canada.csv', thousands=',')

    df5Years = df.tail(5)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df5Years['Year End'], y=df5Years['Cash and bank accounts and short term investments'], name='Cash, bank accounts and short term investments'))
    fig.add_trace(go.Bar(x=df5Years['Year End'], y=df5Years['Revenue - Receipted donations'], name='Donations'))
    fig.add_trace(go.Bar(x=df5Years['Year End'], y=df5Years['Total Revenue'], name='Total Revenue'))
    fig.add_trace(go.Bar(x=df5Years['Year End'], y=df5Years['Expenses - Charitable programs'], name='Expenses - Charitable programs'))
    fig.add_trace(go.Bar(x=df5Years['Year End'], y=df5Years['Expenses - Gifts to other registered charities and qualified donees'], name='Expenses - Gifts to BYU'))
    fig.add_trace(go.Bar(x=df5Years['Year End'], y=df5Years['Expenses - Management and administration'], name='Expenses - Management and administration'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        xaxis_title='Year End', 
        yaxis_title='Amount $', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Total Revenue'], name='Total Revenue'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Total Expenses'], name='Total Expenses'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Revenue and Expenses',
        xaxis_title='Year End', 
        yaxis_title='Amount $', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Total Assets'], name='Total Assets'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Total Assets',
        xaxis_title='Year End', 
        yaxis_title='Amount $', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('See [CRA Registered Charity Information Return](https://apps.cra-arc.gc.ca/ebci/hacc/srch/pub/dsplyRprtngPrd?q.srchNmFltr=Church+of+Jesus+Christ+of+Latter-day+Saints&q.stts=0007&selectedCharityBn=826344632RR0001&dsrdPg=1)')
