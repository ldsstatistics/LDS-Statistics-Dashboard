import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Church Finances in the 1900s')
    
    df = pd.read_csv('data/Finances/Expenditures 1900s.csv', thousands=',')

    fig = go.Figure()
    for column in df.columns:
        if column != 'Year':
            fig.add_trace(go.Bar(x=df['Year'], y=df[column], name=column))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Expenditures from Church General Funds, 1914-1958', 
        xaxis_title='Year', 
        barmode='stack',
        yaxis_tickprefix='$',
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('[Samuel D. Brunson, Dialogue, The Present, Past, and Future of LDS Financial Transparency](https://www.dialoguejournal.com/wp-content/uploads/sbi/articles/4804_taxdaysb.pdf)')

    col1, col2, col3 = st.columns([1, 4, 1])

    fig = go.Figure(data=[go.Pie(
        labels=['From Business Losses', 'From Anti-Polygamy Government Actions'], 
        values=[2068961, 99051], 
        texttemplate=['<b>From Business Losses<br>$2,068,961<b>', 'From Anti-Polygamy<br>Government Actions<br>$99,051']
    )])
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Church Debt 1899',
        showlegend=False,
    )
    with col1:
        st.plotly_chart(fig, use_container_width=True)

    df = pd.read_csv('data/Finances/Tithing and Expenditures 1943-1960.csv', thousands=',')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Tithing'], name='Tithing'))
    fig.add_trace(go.Bar(x=df['Year'], y=df['Expenditures'], name='Expenditures', width=0.6))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        title='Church Tithing and Expenditures in US Dollars', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis_title='Year', 
        yaxis_tickprefix='$',
        barmode='overlay',
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=['1962'], y=[-32717660], name='Deficit in 1962', marker_color='#d62728'))
    fig.add_trace(go.Bar(x=['1969'], y=[29500000], name='Surplus in 1969', marker_color='#2ca02c'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis_title='Year', 
        yaxis_tickprefix='$',
        barmode='overlay',
    )
    with col3:
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('-- D. Michael Quinn, The Mormon Hierarchy: Wealth and Corporate Power, Chapter 3')
