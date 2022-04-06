import streamlit as st
from dashboards import statisticsByCountry2021, statisticsByCountry2019, growthByCountry, membershipComparison
from dashboards import fullerConsiderationAnalysis, unitsByCountry, unitsByState
from dashboards import financesInAustralia, financesInCanada, financesInTheUK, financesInThe1900s
from dashboards import temples, prophets, pluralMarriage, wealthOfBrighamYoung

st.set_page_config(
    page_title="LDS Statistics",
    layout="wide",
)

pages = {
    '2021 Statistics by Country': statisticsByCountry2021,
    '2019 Statistics by Country': statisticsByCountry2019,
    'Growth by Country': growthByCountry,
    'Membership Comparison': membershipComparison,
    'Fuller Consideration Analysis': fullerConsiderationAnalysis,
    'Units by Country': unitsByCountry,
    'Units by State': unitsByState,
    'Finances in Australia': financesInAustralia,
    'Finances in Canada': financesInCanada,
    'Finances in the UK': financesInTheUK,
    'Finances in the 1900s': financesInThe1900s,
    'Temples': temples,
    'Prophets': prophets,
    'Plural Marriage': pluralMarriage,
    'Wealth of Brigham Young': wealthOfBrighamYoung,
}

st.sidebar.title('LDS Data Dashboard')
pageTitle = st.sidebar.radio('Go To', pages.keys())
pages[pageTitle].app()

st.sidebar.title('Other Resources')
st.sidebar.markdown('[Fuller Consideration Membership Statistics](http://www.fullerconsideration.com/membership.php)')
st.sidebar.markdown('[Fuller Consideration Daily Statistics](http://www.fullerconsideration.com/units.php)')
st.sidebar.markdown('[Cumorah Project](https://www.cumorah.com/countries)')
st.sidebar.markdown('[LDS Statistics](http://ldsstatistics.com)')
st.sidebar.markdown('[Latter Data Saints](https://latterdatasaints.com/)')
st.sidebar.markdown('[LDS Finances - The Widow\'s Mite Report](https://widowsmitereport.wordpress.com)')
st.sidebar.markdown('[Temples](https://churchofjesuschristtemples.org)')
st.sidebar.markdown('[Apostles - ThreeStory](http://threestory.com/apostles/apostles_all.html)')
