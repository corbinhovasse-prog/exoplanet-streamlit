"""
Home page of my Streamlit portfolio: Exploring Exoplanets.
Run from this folder with:  streamlit run Home.py
The pages/ folder adds the Bio, EDA Gallery, Dashboard, and Future Work pages.
"""
import streamlit as st
from utils import load_data, sidebar_brand, source_caption

# 1. PAGE CONFIG (must be the first Streamlit command)
st.set_page_config(page_title="Corbin Hovasse | Exoplanet Portfolio", page_icon="🪐", layout="wide")

# 2. DATA (cached in utils.load_data)
df = load_data()

# 3. HEADER / BRANDING
st.title("🪐 Exploring Exoplanets")
st.subheader("A data visualization portfolio by Corbin Hovasse")
st.markdown("Data Science & Machine Learning student at MSU Denver · "
            "[LinkedIn](https://www.linkedin.com/in/corbin-h-923318107/) · "
            "[GitHub](https://github.com/corbinhovasse-prog) · "
            "[Website](https://corbinhovasse-prog.github.io/)")

st.write("")
st.markdown(
    "More than 6,000 planets have been confirmed outside our solar system. This app explores "
    "NASA's catalog of those planets: **how they were found, when, and what they are like** — "
    "and how the way we search shapes what we find."
)

# 4. QUICK FACTS (full dataset)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Confirmed planets", f"{len(df):,}")
c2.metric("Host stars", f"{df['host_star'].nunique():,}")
c3.metric("Discovery years", f"{df['year'].min()}–{df['year'].max()}")
c4.metric("Discovery methods", df["method_detail"].nunique())

# 5. PAGE CARDS (navigation)
st.write("")
st.markdown("#### Explore the app")
a, b, c, d = st.columns(4)
with a:
    with st.container(border=True):
        st.markdown("**📄 Bio**")
        st.caption("Who I am, my tools, and my visualization philosophy.")
        st.page_link("pages/1_📄_Bio.py", label="Open Bio")
with b:
    with st.container(border=True):
        st.markdown("**📊 EDA Gallery**")
        st.caption("Four chart types, each with a guide and observations.")
        st.page_link("pages/2_📊_EDA_Gallery.py", label="Open Gallery")
with c:
    with st.container(border=True):
        st.markdown("**📈 Dashboard**")
        st.caption("Filter the catalog and watch the KPIs and charts update.")
        st.page_link("pages/3_📈_Dashboard.py", label="Open Dashboard")
with d:
    with st.container(border=True):
        st.markdown("**🧭 Future Work**")
        st.caption("Next steps and what changed from my prototype.")
        st.page_link("pages/4_🧭_Future_Work.py", label="Open Future Work")

st.write("")
source_caption()
sidebar_brand()
