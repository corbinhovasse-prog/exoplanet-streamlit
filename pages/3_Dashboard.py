"""
Exoplanet Discovery Dashboard.
Sidebar filters -> filtered DataFrame -> KPIs + linked charts all update together.
"""
import altair as alt
import pandas as pd
import streamlit as st
from utils import (load_data, sidebar_brand, METHOD_SCALE, METHOD_ORDER, SIZE_CLASSES,
                   SOURCE_NAME, SOURCE_URL, DATA_TIMESTAMP)

# 1. PAGE CONFIG
st.set_page_config(page_title="Dashboard | Corbin Hovasse", page_icon="📈", layout="wide",
                   initial_sidebar_state="expanded")

# 2. LOAD DATA (cached)
df = load_data()

# 3. SIDEBAR FILTERS
with st.sidebar:
    st.header("🔭 Filters")
    methods = st.multiselect("Discovery method", METHOD_ORDER, default=METHOD_ORDER)
    years = st.slider("Discovery year", int(df["year"].min()), int(df["year"].max()),
                      value=(int(df["year"].min()), int(df["year"].max())))
    sizes = st.multiselect("Planet size class (Earth radii)", SIZE_CLASSES, default=SIZE_CLASSES)

mask = (df["method"].isin(methods)
        & df["year"].between(years[0], years[1])
        & df["size_class"].isin(sizes))
filtered = df[mask]

sidebar_brand()

# 4. HEADER + REPRODUCIBILITY (source badge, link, last refreshed)
st.title("📈 Exoplanet Discovery Dashboard")
st.caption("How, when, and where confirmed exoplanets were found. Every number and chart below follows the sidebar filters.")
st.badge("Data: NASA Exoplanet Archive", icon=":material/public:", color="blue")
st.markdown(f"Source: [{SOURCE_NAME}]({SOURCE_URL}) · **Last refreshed:** {DATA_TIMESTAMP}")

if filtered.empty:
    st.warning("No planets match these filters. Select at least one method and one size class.")
    st.stop()

# 5. KPI ROW (4 equal columns)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Planets found", f"{len(filtered):,}",
          help="Number of confirmed planets that match the filters.")
k2.metric("Host stars", f"{filtered['host_star'].nunique():,}",
          help="Number of different stars these planets orbit.")
med_radius = filtered["radius_earth"].median()     # NaN if no planet in the selection has a radius
med_dist = filtered["distance_pc"].median()
k3.metric("Median radius (Earth radii)", "n/a" if pd.isna(med_radius) else f"{med_radius:.2f}",
          help="Middle planet size; Earth = 1. Includes calculated radii.")
k4.metric("Median distance (parsecs)", "n/a" if pd.isna(med_dist) else f"{med_dist:,.0f}",
          help="Middle distance from Earth. 1 parsec ≈ 3.26 light-years.")

# 6. MAIN ROW: two linked charts (2:1 widths)
left, right = st.columns((2, 1), gap="medium")

with left:
    with st.container(border=True):
        st.subheader("Discoveries per year by method")
        by_year = filtered.groupby(["year", "method"], as_index=False).size().rename(columns={"size": "planets"})
        bars = alt.Chart(by_year).mark_bar().encode(
            x=alt.X("year:O", title="Discovery year", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("planets:Q", title="Planets discovered (count)"),
            color=alt.Color("method:N", scale=METHOD_SCALE, sort=METHOD_ORDER, title="Discovery method"),
            order=alt.Order("method:N"),
            tooltip=[alt.Tooltip("year:O", title="Year"), alt.Tooltip("method:N", title="Method"),
                     alt.Tooltip("planets:Q", title="Planets", format=",")],
        ).properties(height=360)
        st.altair_chart(bars, width="stretch",
                        alt="Stacked bar chart of planets discovered per year, colored by discovery method.")
        st.caption("Stacked bars: total bar height is all planets that year; colors split it by method.")

with right:
    with st.container(border=True):
        st.subheader("Planets by method")
        by_method = (filtered.groupby("method", as_index=False).size()
                     .rename(columns={"size": "planets"})
                     .sort_values("planets", ascending=False))
        base = alt.Chart(by_method).encode(
            y=alt.Y("method:N", sort=by_method["method"].tolist(), title=None),   # largest bar on top
            # Extra 15% room on the right so the count labels are not cut off
            x=alt.X("planets:Q", title="Planets (count)",
                    scale=alt.Scale(domain=[0, int(by_method["planets"].max() * 1.15)])),
        )
        method_bars = base.mark_bar().encode(
            color=alt.Color("method:N", scale=METHOD_SCALE, legend=None),
            tooltip=[alt.Tooltip("method:N", title="Method"), alt.Tooltip("planets:Q", title="Planets", format=",")],
        )
        labels = base.mark_text(align="left", dx=4, color="#E6EAF2").encode(text=alt.Text("planets:Q", format=","))
        st.altair_chart((method_bars + labels).properties(height=360), width="stretch",
                        alt="Horizontal bar chart of the number of planets found by each discovery method.")
        st.caption("Counts are printed on each bar, so color is never the only cue.")

# 7. TABS: more linked views
tab_fac, tab_data = st.tabs(["🛰️ Top facilities", "📄 Filtered data"])

with tab_fac:
    top_fac = (filtered.groupby("facility", as_index=False).size()
               .rename(columns={"size": "planets"})
               .sort_values("planets", ascending=False).head(10))
    st.dataframe(top_fac, hide_index=True, width="stretch",
                 column_config={
                     "facility": st.column_config.TextColumn("Discovery facility"),
                     "planets": st.column_config.ProgressColumn("Planets", format="%d", min_value=0,
                                                                max_value=int(top_fac["planets"].max())),
                 })

with tab_data:
    show_cols = ["planet", "host_star", "method", "year", "facility", "period_days",
                 "radius_earth", "radius_source", "mass_earth", "star_temp_k", "distance_pc"]
    st.dataframe(filtered[show_cols], hide_index=True, width="stretch")
    st.caption(f"{len(filtered):,} rows. Units: period in days, radius and mass in Earth units, "
               "star temperature in Kelvin, distance in parsecs. Blank cells mean NASA has no value.")

# 8. INSIGHTS (narrative)
with st.container(border=True):
    st.subheader("💡 Insights")
    st.markdown(
        "- **Transit dominates the catalog:** 4,800 of 6,473 planets (74%). Radial Velocity found more planets "
        "than Transit every year from 1995 through 2009, and Transit has found more every year since 2010.\n"
        "- **A few missions drive the totals:** Kepler (2,787 planets), TESS (1,024), and K2 (549) lead the "
        "facility list. Open the *Top facilities* tab and narrow the years to see the leaders change.\n"
        "- **Methods reach different distances:** the median Radial Velocity planet is about 44 parsecs away, "
        "Transit about 459, and Microlensing about 6,270. Select one method at a time to compare.\n"
        "- **Earth-sized planets are a small slice:** selecting only *Earth-sized* leaves 604 planets, "
        "and 562 of them (93%) were found by Transit.\n"
        "- **Limitations:** counts reflect which surveys ran and what each method can detect, not how common "
        "planets really are. About 1,544 radii are calculated from mass rather than measured. These patterns "
        "are descriptive and do not show cause."
    )

with st.expander("About this dashboard"):
    st.write(
        "Data: NASA Exoplanet Archive, Planetary Systems Composite Parameters table (6,473 confirmed planets, "
        "one row per planet). Preprocessing: kept 12 of 325 columns, grouped seven rare discovery methods "
        "(74 planets) into 'Other', filled 6 blank facility names with 'Unknown', added a size class from "
        "radius, and flagged whether each radius was measured or calculated. No rows were removed."
    )
