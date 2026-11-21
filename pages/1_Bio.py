"""Bio page: professional summary, highlights, and visualization philosophy."""
import streamlit as st
from utils import sidebar_brand, ASSETS_DIR

st.set_page_config(page_title="Bio | Corbin Hovasse", page_icon="📄", layout="wide")

st.title("📄 Bio")
st.caption("Corbin Hovasse · Denver, Colorado · B.S. Data Science & Machine Learning, MSU Denver (May 2027)")

left, right = st.columns((1, 2), gap="large")

# ---- Left column: image with alt-text and caption ----
with left:
    # Use my profile photo if it is in assets/, otherwise the project banner
    photo = ASSETS_DIR / "profile.jpg"
    if photo.exists():
        st.image(str(photo), width="stretch",
                 caption="Corbin Hovasse",
                 alt="Headshot photo of Corbin Hovasse")
    else:
        st.image(str(ASSETS_DIR / "banner.png"), width="stretch",
                 caption="Every dot is a confirmed exoplanet, colored by discovery method.",
                 alt="Dark star-field style chart in which each of about 6,000 dots is a confirmed "
                     "exoplanet, placed by orbital period and planet size and colored by discovery method.")

# ---- Right column: summary, highlights, philosophy ----
with right:
    st.subheader("Professional summary")
    st.write(
        "I am a Data Science & Machine Learning student at MSU Denver who builds data pipelines and "
        "machine learning models for messy, real-world scientific data. I am drawn to data from the "
        "physical world, such as space, physics, and geology, where measurements are hard to get. "
        "I work mainly in Python with pandas, scikit-learn, and Streamlit, and I focus on turning raw "
        "data into clear visuals that people can act on. Before school I served in the U.S. Army as an "
        "airborne infantry mortarman, where precise calculation and clear communication under pressure "
        "had real consequences."
    )

    st.subheader("Highlights")
    st.markdown(
        "- **Featured project:** a real-time solar wind pipeline that compares three spacecraft at the "
        "Sun–Earth L1 point ([live dashboard](https://corbinhovasse-prog.github.io/solar-wind-l1/)).\n"
        "- **Tools:** Python, pandas, scikit-learn, Altair, Streamlit, Docker, Apache Kafka, GitHub Actions.\n"
        "- **Coursework:** Machine Learning, Data Visualization, Probability & Statistics, "
        "Applied Linear Algebra, Database Systems.\n"
        "- **Open to:** data science, ML, and data engineering roles and internships in science, "
        "space, and Earth observation."
    )

st.subheader("My visualization philosophy")
st.write(
    "A chart should answer one clear question, and a viewer should be able to read it without me in the room. "
    "I aim for **clarity** (labeled axes, units, and plain-language titles), **accessibility** (color-blind-safe "
    "palettes, strong contrast, and values or tooltips so color is never the only cue), and **ethics** "
    "(honest scales, stated data limitations, and no claims of cause when the data only shows a pattern). "
    "I would rather show where the data stops being trustworthy than let a chart look more certain than it is."
)

sidebar_brand()
