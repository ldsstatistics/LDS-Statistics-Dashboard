from os import listdir
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Membership Growth Between 2009 - 2019')
    col1, col2 = st.columns([1, 4])

    with col1:
        analysisSelected = st.radio('Choose Analysis', ['Membership Change', 'Growth Percentage', 'Percentage of Total Growth'])
        numberOfCountries = st.radio('Number of Countries to Show', [10, 20, 30, 40, 50, 60], index=1)
        continent = st.radio('Continent', ['Worldwide', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])

    df = pd.read_csv('data/Membership Growth By Country.csv', thousands=',', keep_default_na=False)
    totalMembershipChange = df['Membership Change'].sum()

    if continent != 'Worldwide':
        df = df.loc[df['Continent'] == continent]

    df['Growth Percentage'] = df['Membership Change'] / df['Membership - 2009'] * 100
    df['Percentage of Total Growth'] = df['Membership Change'] / totalMembershipChange * 100
    
    df['Country'] = df['Country'] + ' ' + df['Footnote']
    data = df.sort_values(analysisSelected, ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data[analysisSelected][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        height=700,
        xaxis_title=analysisSelected,
        yaxis={'autorange': 'reversed'}
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('Notes')
    st.markdown('See Wikipedia: [The Church of Jesus Christ of Latter-day Saints Membership Statistics](https://en.wikipedia.org/wiki/The_Church_of_Jesus_Christ_of_Latter-day_Saints_membership_statistics#Membership_Growth)')
    st.markdown('(a) 2019 Membership information unavailabe. Used 2018 Membership numbers instead.')

    membershipByCountryFiles = listdir('data/Membership By Country')
    countries = [x.split('.')[0] for x in membershipByCountryFiles]

    st.title('Comparison Between Countries')
    defaultCountries = ['United States', 'Brazil', 'Mexico', 'Philippines']
    col1, col2 = st.columns([1, 4])
    with col1:
        analysisSelected = st.radio('Choose Analysis', ['Membership', 'Annual Membership Growth Rate', 'Wards', 'Branches', 'Units', 'Annual Unit Growth Rate', 'Percent Members'])
    countriesSelected = []
    for i in range(len(defaultCountries)):
        with col1:
            countrySelected = st.selectbox('Select Country ' + str(i+1), countries, countries.index(defaultCountries[i]))
            if countrySelected not in countriesSelected:
                countriesSelected.append(countrySelected)
    
    fig = go.Figure()
    for country in countriesSelected:
        df = pd.read_csv('data/Membership By Country/{}.csv'.format(country), thousands=',')
        df = df[df['Year'] >= 1987]
        df['Annual Membership Growth Rate'] = pd.to_numeric(df['Annual Membership Growth Rate'].str.replace('%', ''), errors='coerce')
        df['Annual Unit Growth Rate'] = pd.to_numeric(df['Annual Unit Growth Rate'].str.replace('%', ''), errors='coerce')
        df['Percent Members'] = df['Membership'] / df['Population'] * 100
        df[analysisSelected] = pd.to_numeric(df[analysisSelected], errors='coerce')
        fig.add_trace(go.Scatter(x=df['Year'], y=df[analysisSelected], mode='lines', name=country))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        height=700,
        xaxis_title='Year',
        yaxis_title=analysisSelected,
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='left', x=0),
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)