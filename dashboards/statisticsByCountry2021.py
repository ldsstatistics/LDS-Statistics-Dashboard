import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Membership by Country 2021')
    col1, col2 = st.columns([1, 4])

    unitTypes = ['Members', 'Percent LDS', 'Wards & Branches', 'Wards', 'Branches', 'Districts', 'Stakes', 'Missions', 'Temples']

    with col1:
        unitTypeSelected = st.radio('Choose Analysis', unitTypes)
        numberOfCountries = st.radio('Number of Countries to Show', [10, 20, 30, 40, 50, 60, 100], index=1)

    df = pd.read_csv('data/Membership by country 2021.csv', thousands=',')
    
    data = df.sort_values(unitTypeSelected, ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data[unitTypeSelected][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        height=700,
        xaxis_title=unitTypeSelected,
        yaxis={'autorange': 'reversed'}
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('See: [The Church of Jesus Christ of Latter-day Saints Membership Statistics](https://newsroom.churchofjesuschrist.org/facts-and-statistics)')