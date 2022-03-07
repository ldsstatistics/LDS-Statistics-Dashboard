import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Finances in the UK')
    
    df = pd.read_csv('data/LDS Church Finances UK.csv', thousands=',')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Tithing'], name='Tithing'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Fast Offering Fund Donations'], name='Fast Offerings', visible='legendonly'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Missionary Suport Fund'], name='Missionary Suport Fund', visible='legendonly'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Book of Mormon Fund Donations'], name='Book of Mormon Fund Donations', visible='legendonly'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Temple Construction Fund Donations'], name='Temple Construction Fund Donations', visible='legendonly'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Humanitarian Aid Fund'], name='Humanitarian Aid Fund', visible='legendonly'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Perpetual Education Fund Donations'], name='Perpetual Education Fund Donations', visible='legendonly'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        xaxis_title='Year End', 
        yaxis_title='Amount £', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Humanitarian Aid Fund Balance'], name='Humanitarian Aid Fund Balance'))
    fig.add_trace(go.Bar(x=df['Year End'], y=df['Humanitarian Aid Fund'], name='Humanitarian Aid Fund'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        xaxis_title='Year End', 
        yaxis_title='Amount £', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('See [Charity Commission For England And Wales](https://register-of-charities.charitycommission.gov.uk/charity-search/-/charity-details/242451/charity-overview)')
    st.markdown('See [data collected by u/kristmace](https://1drv.ms/x/s!Ar4OFnzpFMxC4V6DRuN3NR-p-MCH)')
