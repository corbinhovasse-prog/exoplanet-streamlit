"""Bio page."""
import streamlit as st
from utils import sidebar_brand, ASSETS_DIR

st.set_page_config(page_title="Bio | Corbin Hovasse", page_icon="📄", layout="wide")

st.title("📄 Bio")
st.caption("Corbin Hovasse · Denver, Colorado · B.S. Data Science & Machine Learning, MSU Denver (May 2027)")

# Header image (wide, so it spans the page)
st.image(
    str(ASSETS_DIR / "sizing_up_exoplanets.jpg"),
    width="stretch",
    caption="Sizing Up Exoplanets (PIA15258), NASA/JPL, 2012",
    alt="NASA/JPL illustration titled Sizing Up Exoplanets, showing the three small planets "
        "of the star KOI-961, discovered with Kepler data in 2012.",
)
st.caption("Image source: [NASA Science](https://science.nasa.gov/image-detail/amf-pia15258/)")

st.subheader("About me")
st.write(
    "I'm a Data Science and Machine Learning student at MSU Denver, graduating in May 2027. "
    "I mostly work with scientific data from space and physics, using Python, pandas, scikit-learn, "
    "and Streamlit. My most recent project collects live solar wind data from three spacecraft "
    "and flags solar storm arrivals. Before school I served in the U.S. Army as an airborne infantry "
    "mortarman with the 1-501st Parachute Infantry Regiment in Alaska."
)

st.subheader("Highlights")
st.markdown(
    "- **Solar wind pipeline:** live data from three spacecraft at the Sun–Earth L1 point, with "
    "anomaly detection ([live dashboard](https://corbinhovasse-prog.github.io/solar-wind-l1/))\n"
    "- **Tools:** Python, pandas, scikit-learn, Altair, Streamlit, Docker, Apache Kafka, GitHub Actions\n"
    "- **Coursework:** Machine Learning, Data Visualization, Probability & Statistics, "
    "Applied Linear Algebra, Database Systems\n"
    "- **Looking for:** data science, ML, and data engineering internships in science, space, "
    "and Earth observation"
)

st.subheader("Visualization philosophy")
st.write(
    "Each chart should answer one question and be readable without someone there to explain it. "
    "That means labeled axes with units, color-blind-safe colors, and tooltips or printed values so "
    "color is never the only way to read a number. I also point out where the data has limits, "
    "such as values that were estimated instead of measured, and I describe patterns without "
    "claiming what caused them."
)

sidebar_brand()
