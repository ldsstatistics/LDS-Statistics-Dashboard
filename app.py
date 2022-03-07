import app1, app2, app3, app4, app5, app6, app7, app8, app9, app10, app11, app12
import streamlit as st

st.set_page_config(
    page_title="LDS Statistics",
    layout="wide",
)

PAGES = {
    "2019 Statistics by Country": app7,
    "Growth by Country": app8,
    "Membership Comparison": app10,
    "Fuller Consideration Analysis": app1,
    "Units by Country": app2,
    "Units by State": app6,
    "Finances in Canada": app3,
    "Finances in the UK": app4,
    "Temples": app5,
    "Prophets": app11,
    "Plural Marriage": app9,
    "Wealth of Brigham Young": app12,
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()