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
    st.markdown('(a) 2019 Membership information unavailable. Used 2018 Membership numbers instead.')

    membershipByCountryFiles = listdir('data/Membership by Country')
    countries = [x.split('.')[0] for x in membershipByCountryFiles]
    countries.sort()

    st.title('Membership Growth')
    defaultCountry = 'United States'
    country = st.selectbox('Select Country', countries, countries.index(defaultCountry))

    col1, col2 = st.columns(2)

    df = pd.read_csv('data/Membership by Country/{}.csv'.format(country), thousands=',')
    df = df[df['Year'] >= 2000]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Membership'], name=country))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20), xaxis_title='Year', yaxis_title='Membership')
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Wards'], name='Wards'))
    fig.add_trace(go.Bar(x=df['Year'], y=df['Branches'], name='Branches'))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20), xaxis_title='Year', yaxis_title='Units', barmode='stack', legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'left', 'x': 0})
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Membership'].diff() / df['Year'].diff(), name=country))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20), xaxis_title='Year', yaxis_title='Annual Membership Growth')
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Units'].diff() / df['Year'].diff(), name=country))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20), xaxis_title='Year', yaxis_title='Annual Unit Growth', barmode='stack', legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'left', 'x': 0})
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Membership'] / df['Units'], name=country))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20), xaxis_title='Year', yaxis_title='Members Per Congregation')
    with col1:
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Membership'] / df['Population'] * 100, name=country))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=20), xaxis_title='Year', yaxis_title='Percent Members')
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    st.title('Comparison Between Countries')
    defaultCountries = ['United States', 'Brazil', 'Mexico', 'Philippines']
    col1, col2 = st.columns([1, 4])
    with col1:
        analysisSelected = st.radio('Choose Analysis', ['Membership', 'Annual Membership Growth', 'Annual Membership Growth Rate', 'Wards', 'Branches', 'Units', 'Annual Unit Growth', 'Annual Unit Growth Rate', 'Percent Members'])
    countriesSelected = []
    for i in range(len(defaultCountries)):
        with col1:
            countrySelected = st.selectbox('Select Country ' + str(i+1), countries, countries.index(defaultCountries[i]))
            if countrySelected not in countriesSelected:
                countriesSelected.append(countrySelected)
    
    fig = go.Figure()
    for country in countriesSelected:
        df = pd.read_csv('data/Membership by Country/{}.csv'.format(country), thousands=',')
        df = df[df['Year'] >= 1987]
        df['Annual Membership Growth'] = df['Membership'].diff() / df['Year'].diff()
        df['Annual Membership Growth Rate'] = df['Annual Membership Growth'] / (df['Membership'] - df['Membership'].diff()) * 100
        df['Annual Unit Growth'] = df['Units'].diff() / df['Year'].diff()
        df['Annual Unit Growth Rate'] = df['Annual Unit Growth'] / (df['Units'] - df['Units'].diff()) * 100
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