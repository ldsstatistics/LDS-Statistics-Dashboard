import streamlit as st
from dashboards import statisticsByCountry2019, growthByCountry, membershipComparison
from dashboards import fullerConsiderationAnalysis, unitsByCountry, unitsByState
from dashboards import financesInAustralia, financesInCanada, financesInTheUK
from dashboards import temples, prophets, pluralMarriage, wealthOfBrighamYoung

st.set_page_config(
    page_title="LDS Statistics",
    layout="wide",
)

pages = {
    '2019 Statistics by Country': statisticsByCountry2019,
    'Growth by Country': growthByCountry,
    'Membership Comparison': membershipComparison,
    'Fuller Consideration Analysis': fullerConsiderationAnalysis,
    'Units by Country': unitsByCountry,
    'Units by State': unitsByState,
    'Finances in Australia': financesInAustralia,
    'Finances in Canada': financesInCanada,
    'Finances in the UK': financesInTheUK,
    'Temples': temples,
    'Prophets': prophets,
    'Plural Marriage': pluralMarriage,
    'Wealth of Brigham Young': wealthOfBrighamYoung,
}

st.sidebar.title('LDS Data Dashboard')
pageTitle = st.sidebar.radio('Go To', pages.keys())
pages[pageTitle].app()
