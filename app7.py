import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Membership by Country 2019')
    col1, col2 = st.columns([1, 4])

    unitTypes = ['Members', 'Percent LDS', 'Wards & Branches', 'Wards', 'Branches', 'Districts', 'Stakes', 'Missions', 'Temples']

    with col1:
        unitTypeSelected = st.radio('Choose Analysis', unitTypes)
        numberOfCountries = st.radio('Number of Countries to Show', [10, 20, 30, 40, 50, 60, 100], index=1)

    df = pd.read_csv('data/Membership by country 2019.csv', thousands=',', keep_default_na=False)
    
    df['Country'] = df['Country'] + ' ' + df['Footnote']
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
    
    st.markdown('Notes')
    st.markdown('See Wikipedia: [The Church of Jesus Christ of Latter-day Saints Membership Statistics](https://en.wikipedia.org/wiki/The_Church_of_Jesus_Christ_of_Latter-day_Saints_membership_statistics#Countries)')
    st.markdown('(b) 2019 Membership not released for country or territory. Estimated 2015 Membership information was used instead.')
    st.markdown('(c) 2019 Membership not released for country or territory. 2018 Membership and Congregational information was used instead.')
    st.markdown('(d) An estimated mid-year 2018 membership and congregational information was used for Mainland China.')
    st.markdown('(e) 2019 Membership not released for country or territory. 2017 Membership and Congregational information was used instead.')
    st.markdown('(f) 2016 Membership data and population was used for Russia, the last year the church released membership data for the country.')