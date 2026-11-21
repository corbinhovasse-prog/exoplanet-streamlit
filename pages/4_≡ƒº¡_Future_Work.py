"""Future Work page: next steps and reflection on the Lab 4.3 paper prototype."""
import streamlit as st
from utils import sidebar_brand

st.set_page_config(page_title="Future Work | Corbin Hovasse", page_icon="🧭", layout="wide")

st.title("🧭 Future Work")
st.write("Where I would take this project next, and how it changed from my first prototype.")

with st.container(border=True):
    st.subheader("Next steps")
    st.markdown(
        "1. **Automatic data refresh:** pull the newest planets straight from NASA's archive API on a weekly "
        "schedule (GitHub Actions), so the dashboard and its *last refreshed* date update on their own.\n"
        "2. **Habitable zone view:** add each star's brightness and compute which planets orbit where liquid "
        "water could exist, then add a filter for those planets.\n"
        "3. **Measured-only mode:** add a dashboard toggle that hides every calculated radius and mass, so "
        "users can compare the full catalog with the measured-only version side by side.\n"
        "4. **Forecast discoveries:** model discoveries per year by mission to estimate how many planets TESS "
        "may add by 2030, with uncertainty ranges shown on the chart.\n"
        "5. **Accessibility audit:** test the app with a screen reader and a color-blindness simulator, and "
        "add a downloadable data table for every chart."
    )

with st.container(border=True):
    st.subheader("Reflection: from paper prototype to final build")
    st.markdown(
        "- **Kept the layout that worked:** my Lab 4.3 prototype (an online orders dashboard) had sidebar "
        "filters, a KPI row, two main charts side by side, tabs, an insights box, and an *About* expander. "
        "This dashboard keeps that same structure.\n"
        "- **Moved to real, larger data:** I replaced the practice sales file with NASA's catalog of 6,473 "
        "planets, which needed log scales and grouped methods to stay readable.\n"
        "- **Made it look less plain:** feedback said the first version looked basic, so I added a dark "
        "space theme, bordered cards, icons, and one consistent color-blind-safe palette across every page.\n"
        "- **Added honesty about the data:** I found that many planet sizes are calculated rather than "
        "measured, so I added a measured/calculated toggle, a source badge, a last-refreshed date, and a "
        "limitations note that the prototype did not have."
    )

sidebar_brand()
