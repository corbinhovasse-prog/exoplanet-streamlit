"""
Shared helpers used by every page:
- load_data(): reads and prepares the exoplanet CSV (cached)
- METHOD_COLORS: one color-blind-safe color per discovery method (Okabe-Ito palette)
- sidebar_brand(): the same name/contact block in every sidebar
"""
from pathlib import Path
import altair as alt
import pandas as pd
import streamlit as st

# Build file paths from this file's folder, so the app works no matter which
# folder `streamlit run` is started from
APP_DIR = Path(__file__).parent
DATA_PATH = APP_DIR / "data" / "exoplanets.csv"
ASSETS_DIR = APP_DIR / "assets"
SOURCE_URL = ("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/"
              "nph-tblView?app=ExoTbls&config=PSCompPars")
SOURCE_NAME = "NASA Exoplanet Archive (Planetary Systems Composite Parameters)"
DATA_REFRESHED = "November 20, 2026"   # date the CSV was downloaded from NASA
DATA_TIMESTAMP = "2026-11-20 21:27"    # timestamp written in the header of NASA's download file

# The four main discovery methods; the seven rare methods (74 planets) are grouped as "Other"
MAIN_METHODS = ["Transit", "Radial Velocity", "Microlensing", "Imaging"]

# Okabe-Ito palette: designed to stay distinguishable for color-blind viewers
METHOD_COLORS = {
    "Transit": "#56B4E9",          # sky blue
    "Radial Velocity": "#E69F00",  # orange
    "Microlensing": "#009E73",     # green
    "Imaging": "#CC79A7",          # pink
    "Other": "#F0E442",            # yellow
}
METHOD_ORDER = list(METHOD_COLORS.keys())

# Planet size classes used by the dashboard filter
SIZE_CLASSES = ["Earth-sized (≤1.25)", "Super-Earth (1.25–2)", "Sub-Neptune (2–6)", "Giant (>6)", "Unknown"]
METHOD_SCALE = alt.Scale(domain=METHOD_ORDER, range=list(METHOD_COLORS.values()))


@st.cache_data
def load_data(path=DATA_PATH):
    """Read the CSV once and cache it, so filters don't re-read the file on every rerun."""
    df = pd.read_csv(path)

    # Friendlier column names for charts and tables
    df = df.rename(columns={
        "pl_name": "planet",
        "hostname": "host_star",
        "sy_pnum": "planets_in_system",
        "discoverymethod": "method_detail",
        "disc_year": "year",
        "disc_facility": "facility",
        "pl_orbper": "period_days",
        "pl_rade": "radius_earth",
        "pl_rade_source": "radius_source",   # "Measured" or "Calculated" (added during prep)
        "pl_bmasse": "mass_earth",
        "pl_eqt": "planet_temp_k",
        "st_teff": "star_temp_k",
        "sy_dist": "distance_pc",
    })

    # Group the rare methods so charts stay readable
    df["method"] = df["method_detail"].where(df["method_detail"].isin(MAIN_METHODS), "Other")

    # Fill the 6 blank facility names instead of dropping those planets
    df["facility"] = df["facility"].fillna("Unknown")

    # Size classes from radius (Earth radii); planets with no radius become "Unknown"
    df["size_class"] = pd.cut(
        df["radius_earth"],
        bins=[0, 1.25, 2, 6, 1000],
        labels=SIZE_CLASSES[:-1],
    ).cat.add_categories("Unknown").fillna("Unknown").astype(str)
    return df


def sidebar_brand():
    """Name and contact links shown at the bottom of every sidebar (consistent branding)."""
    with st.sidebar:
        st.divider()
        st.markdown("**Corbin Hovasse**  \nData Science & ML · MSU Denver")
        st.markdown(
            "[LinkedIn](https://www.linkedin.com/in/corbin-h-923318107/) · "
            "[GitHub](https://github.com/corbinhovasse-prog) · "
            "[Website](https://corbinhovasse-prog.github.io/) · "
            "[Email](mailto:corbinhovasse@gmail.com)"
        )


def source_caption():
    """One-line data source caption placed under charts."""
    st.caption(f"Source: [{SOURCE_NAME}]({SOURCE_URL}), downloaded {DATA_REFRESHED}.")
