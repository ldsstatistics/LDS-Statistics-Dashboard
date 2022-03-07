import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title('Wealth of Brigham Young')

    df = pd.read_csv('data/Wealth of Leaders/GA Assets at Death.csv', thousands=',')
    
    fig = go.Figure()
    text = df['Name'] + '<br>' + df['Position'] + '<br>'
    text += 'Year: ' + df['Year'].astype(str) + '<br>'
    text += 'Net Value: $' + df['Net Value'].astype(int).astype(str) + '<br>'
    text += '2010 Value: $' + df['2010'].astype(str) + '<br>'
    hovertemplate = '%{text}<extra></extra>'
    fig.add_trace(go.Bar(x=df['2010'], y=df['Name'], orientation='h', hovertemplate=hovertemplate, text=text))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        height=700,
        title='General Authority Assets at Death in US Dollars',
        xaxis_title='US Dollars in 2010 Valuation',
        yaxis={'autorange': 'reversed'}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write('''
        Brigham Young's death-year value ($1.6 million) is given as the formal appraisal of his estate, 
        which was 88 percent higher than the value ultimately agreed upon. The valuation of $361170 was 
        a reduction demanded by John Taylor as new trustee-in-trust for the church, and was eventually 
        accepted by Young's litigious heirs. Taylor privately threatened to drop from the Quorum of the
        Twelve the three apostles who were the estate's formally appointed trustees if they did not agree
        to this compromise. Taylor's demand was 40 percent lower than Young's 1875 concession of being 
        worth something under $600000 during his divorce proceedings with Ann Eliza Webb Young. \n
        -- D. Michael Quinn, The Mormon Hierarchy: Wealth and Corporate Power, Appendix 4
    ''')

    df = pd.read_csv('data/Wealth of Leaders/Brigham Young Income 1862-1871.csv', thousands=',')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Year'], y=df['Brigham Young'], name='Brigham Young'))
    fig.add_trace(go.Bar(x=df['Year'], y=df['Non-hierarchy\'s top 15 average'], name='Non-hierarchy\'s top 15 average'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        height=700,
        xaxis_title='Year',
        yaxis_title='Income US Dollars',
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='left', x=0),
    )

    st.plotly_chart(fig, use_container_width=True)

    yearOptions = []
    for year in range(1862, 1872):
        if year != 1869:
            yearOptions.append(str(year) + ' General Authority Income Comparison')
    yearSelected = st.selectbox('', yearOptions)

    df = pd.read_csv('data/Wealth of Leaders/{} Incomes.csv'.format(yearSelected[0:4]), thousands=',')
    
    fig = go.Figure()
    text = df['Name'] + '<br>' + df['Position'] + '<br>'
    text += 'Income: $' + df['Income'].astype(int).astype(str) + '<br>'
    hovertemplate = '%{text}<extra></extra>'
    fig.add_trace(go.Bar(x=df['Income'], y=df['Name'], orientation='h', hovertemplate=hovertemplate, text=text))
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=20),
        height=700,
        xaxis_title='US Dollars',
        yaxis={'autorange': 'reversed'}
    )

    st.plotly_chart(fig, use_container_width=True)


    st.write('''
        Incomes are rounded here to the nearest dollar, but not adjusted for 2010. "Average" means the arithmetical mean.
        "Non-hierarchy" includes non-Mormons, lay Mormons, and future and former general authorities not serving as such 
        during that year. To provide a consistent basis of comparison, the average income for non-hierarchy consists of 
        Utah's top fifteen taxpayers for each year. The annual report of March 1870, covering 1869, is missing from 
        manuscripts acquired by the Bancroft Library.\n
        Brigham Young's massive increase in personal income in 1870 was due to his lucrative contracts with the Union 
        Pacific Railroad, which he defined as personal income. Money he earned simultaneously as trustee-in-trust for the
        LDS Church from 1868-71 was first recorded in the annual report of March 1872. The jump in non-hierarchy average 
        income for 1871 was due solely to Salt Lake City's non-LDS banker and mining magnate Warren G. Hussey, whose annual
        income increased from $10000 in 1870 to $261392 in 1871.\n
        -- D. Michael Quinn, The Mormon Hierarchy: Wealth and Corporate Power, Appendix 2
    ''')

    st.write('''
        There were huge disparities from 1862 to 1871. Always at the top, Brigham Young's annual income started out as four 
        times that of his regular counselors, Heber C. Kimball and Daniel H. Wells, and at least nine times their income from 
        1866 onward. Only his counselor-son Joseph A. Young (secretly ordained in 1864 and never publicly acknowledged) had 
        income anywhere close to the church president's, and that was only in 1866. Brigham Young's $10,000 income dwarfed 
        apostle Wilford Woodruff's $380 in 1862, as well as apostle John Taylor's $330. Likewise for the next three years, 
        when apostolic incomes in the hundreds of dollars contrasted with Brigham's ten grand. By the time his annual income 
        reached $111,081 in 1870 (equal to $1,911,000 in today's purchasing power), only one apostle had taxable income. That 
        disparity had nothing to do with Brigham Young's role as trustee-in-trust, which generated a separate income twenty-two 
        times lower than his personal income that year.\n
        Of further interest may be how the general authorities compared with Utah's fifteen highest income earners among Utah's 
        residents. From 1862 to 1871, only Brigham Young exceeded the average of the wealthiest, except in 1866 when secret 
        counselor Joseph A. Young and Seventy's president Horace S. Eldredge outperformed the average fifteen richest men in the 
        territory. In 1871 the non-hierarchy's wealthiest men averaged 12 percent more than Brigham Young, nearly five times more 
        than Eldredge, and nearly twelve times more than Joseph A. Young.\n
        -- [D. Michael Quinn, The Mormon Hierarchy: Wealth and Corporate Power, Chapter 1](https://www.overdrive.com/media/5618976/the-mormon-hierarchy)
    ''')

    st.write('''
        About 95% of Utah's income-earners received an income of less than $600 per year, excluding, of course, 
        their own farm and garden produce consumed during the year. Of those 5% who were above the $600 level, more than 70%, 
        on the average, received incomes of less than $1,000, and more than 90% earned less than $2,000.\n
        -- [Leonard J. Arrington, Taxable Income in Utah, 1862-1872](https://issuu.com/utah10/docs/volume_24_1956/s/95990)
    ''')

    