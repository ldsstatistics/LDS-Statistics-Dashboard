import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Membership Comparison')

    col1, col2 = st.columns(2)

    lds = pd.read_csv('data/Membership Statistics - Data.csv', thousands=',', keep_default_na=False)
    jw = pd.read_csv('data/JW statistics.csv', thousands=',', keep_default_na=False)
    sda = pd.read_csv('data/7th Day Adv statistics.csv', thousands=',', keep_default_na=False)

    lds = lds[lds['End of Year'] < 2022]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=lds['End of Year'], y=lds['Total Membership'], mode='lines', name='LDS Membership'))
    fig.add_trace(go.Scatter(x=sda['Year'], y=sda['Members'], mode='lines', name='7th Day Adv. Membership'))
    fig.add_trace(go.Scatter(x=jw['Service Year'], y=jw['Peak Pub\'s'], mode='lines', name='JW Peak Publishers'))
    fig.add_trace(go.Scatter(x=jw['Service Year'], y=jw['Memorial'], mode='lines', name='JW Memorial Attendance'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        height=500,
        title='Membership Comparison', 
        xaxis_title='Year', 
        yaxis_title='Membership', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': [1960, 2021]}
    )
    with col1:
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=lds['End of Year'], y=lds['Wards and Branches'], mode='lines', name='LDS Wards & Branches'))
    fig.add_trace(go.Scatter(x=sda['Year'], y=sda['Churches'], mode='lines', name='7th Day Adv. Churches'))
    fig.add_trace(go.Scatter(x=sda['Year'], y=sda['Companies'], mode='lines', name='7th Day Adv. Companies'))
    fig.add_trace(go.Scatter(x=jw['Service Year'], y=jw['Congs'], mode='lines', name='JW Congregations'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=100, b=20),
        height=500,
        title='Congregations Comparison', 
        xaxis_title='Year', 
        yaxis_title='Units', 
        legend={'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        xaxis={'range': [1960, 2021]}
    )
    with col2:
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([1, 4])

    with col1:
        numberOfCountries = st.radio('Number of Countries to Show', [10, 20, 30, 40, 50, 60], index=0)
        comparisonType = st.radio('Comparison Type', ['Membership', 'Congregations'], index=1)
        if comparisonType == 'Membership':
            sortBy = st.radio('Sort Membership By', ['Latter-Day Saint', '7th Day Adventist', 'JW Memorial Attendance', 'JW Peak Publishers'])
        else:
            sortBy = st.radio('Sort Congregations By', ['Latter-Day Saint', '7th Day Adv. Churches', '7th Day Adv. Companies', 'Jehovah Witness'])

    df = pd.read_csv('data/Membership by country 2019.csv', thousands=',', keep_default_na=False)
    jw = pd.read_csv('data/JW statistics by country 2019.csv', thousands=',', keep_default_na=False)
    sda = pd.read_csv('data/7th Day Adv statistics by country.csv', thousands=',', keep_default_na=False)

    sda['7th Day Adv. Congregations'] = sda['Churches 2019'] #+ sda['Companies 2019']

    df = df.merge(jw, left_on='Country', right_on='Country or Territory')
    df = df.merge(sda, left_on='Country', right_on='Country or Area of the World')
    
    df['Country'] = df['Country'] + ' ' + df['Footnote']

    if comparisonType == 'Membership':
        if sortBy == '7th Day Adventist':
            data = df.sort_values('Church Membership 2019', ascending=False)
        elif sortBy == 'JW Memorial Attendance':
            data = df.sort_values('Memorial Attendance', ascending=False)
        elif sortBy == 'JW Peak Publishers':
            data = df.sort_values('2019 Peak Pubs.', ascending=False)
        else:
            data = df.sort_values('Members', ascending=False)
    else:
        if sortBy == 'Latter-Day Saint':
            data = df.sort_values('Wards & Branches', ascending=False)
        elif sortBy == '7th Day Adv. Churches':
            data = df.sort_values('Churches 2019', ascending=False)
        elif sortBy == '7th Day Adv. Companies':
            data = df.sort_values('Companies 2019', ascending=False)
        elif sortBy == 'Jehovah Witness':
            data = df.sort_values('No. of Congs.', ascending=False)

    fig = go.Figure()
    if comparisonType == 'Membership':
        fig.add_trace(go.Bar(x=data['Members'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='LDS'))
        fig.add_trace(go.Bar(x=data['Church Membership 2019'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='7th Day Adv.'))
        fig.add_trace(go.Bar(x=data['Memorial Attendance'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='JW Memorial Attendance'))
        fig.add_trace(go.Bar(x=data['2019 Peak Pubs.'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='JW Peak Publishers'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=20),
            height=700,
            xaxis_title='Members',
            yaxis={'autorange': 'reversed'}
        )
    else:
        fig.add_trace(go.Bar(x=data['Wards & Branches'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='LDS Wards & Branches'))
        fig.add_trace(go.Bar(x=data['Churches 2019'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='7th Day Adv. Churches'))
        fig.add_trace(go.Bar(x=data['Companies 2019'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='7th Day Adv. Companies'))
        fig.add_trace(go.Bar(x=data['No. of Congs.'][0:numberOfCountries], y=data['Country'][0:numberOfCountries], orientation='h', name='JW Congregations'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=40, b=20),
            height=700,
            title='2019 Comparison by Country', 
            xaxis_title='Number of Congregations',
            yaxis={'autorange': 'reversed'}
        )
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('Notes')
    st.markdown('See Wikipedia: [The Church of Jesus Christ of Latter-day Saints Membership Statistics](https://en.wikipedia.org/wiki/The_Church_of_Jesus_Christ_of_Latter-day_Saints_membership_statistics#Countries)')
    st.markdown('See [Seventh-day Adventist Annual Statistical Report](https://documents.adventistarchives.org/Statistics/ASR/ASR2020A.pdf)')
    st.markdown('See [JW 2019 Service Year Report](https://www.jw.org/en/library/books/2019-service-year-report/2019-country-territory/)')
    st.markdown('(b) 2019 Membership not released for country or territory. Estimated 2015 Membership information was used instead.')
    st.markdown('(c) 2019 Membership not released for country or territory. 2018 Membership and Congregational information was used instead.')
    st.markdown('(d) An estimated mid-year 2018 membership and congregational information was used for Mainland China.')
    st.markdown('(e) 2019 Membership not released for country or territory. 2017 Membership and Congregational information was used instead.')
    st.markdown('(f) 2016 Membership data and population was used for Russia, the last year the church released membership data for the country.')