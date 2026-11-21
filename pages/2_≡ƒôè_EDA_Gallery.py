"""EDA Gallery: four chart types, each with a question, a reading guide, and observations."""
import altair as alt
import streamlit as st
from utils import load_data, sidebar_brand, source_caption, METHOD_SCALE, METHOD_ORDER

st.set_page_config(page_title="EDA Gallery | Corbin Hovasse", page_icon="📊", layout="wide")
df = load_data()

st.title("📊 EDA Gallery")
st.write("Four views of NASA's catalog of 6,473 confirmed exoplanets. Each chart answers one question, "
         "explains how to read it, and lists what the data shows. Hover over any chart for exact values.")


def guide_and_notes(how_to_read, observations):
    """Show the 'How to read' bullets and the 'Observations' bullets side by side."""
    a, b = st.columns(2, gap="large")
    with a:
        st.markdown("**How to read this chart**")
        st.markdown("\n".join(f"- {line}" for line in how_to_read))
    with b:
        st.markdown("**Observations**")
        st.markdown("\n".join(f"- {line}" for line in observations))


# =====================================================================
# CHART 1: LINE CHART — discoveries per year (interactive tooltips)
# =====================================================================
with st.container(border=True):
    st.subheader("1. Discoveries per year (line chart)")
    st.markdown("**Question:** How has the number of confirmed exoplanet discoveries changed each year since 1992?")

    per_year = df.groupby("year", as_index=False).size().rename(columns={"size": "planets"})

    line = alt.Chart(per_year).mark_line(point=True, color="#56B4E9").encode(
        x=alt.X("year:O", title="Discovery year", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("planets:Q", title="Planets discovered (count)"),
        tooltip=[alt.Tooltip("year:O", title="Year"), alt.Tooltip("planets:Q", title="Planets", format=",")],
    )
    # Annotations for the two Kepler peaks
    peak_2014 = per_year[per_year["year"] == 2014].assign(label="2014: 872 (784 Kepler)")
    peak_2016 = per_year[per_year["year"] == 2016].assign(label="2016: 1,504 (1,276 Kepler)")
    note_2014 = alt.Chart(peak_2014).mark_text(align="right", dx=-10, color="#E6EAF2", fontSize=12).encode(
        x="year:O", y="planets:Q", text="label:N")
    note_2016 = alt.Chart(peak_2016).mark_text(align="left", dx=10, color="#E6EAF2", fontSize=12).encode(
        x="year:O", y="planets:Q", text="label:N")
    notes = note_2014 + note_2016

    st.altair_chart((line + notes).properties(height=380, title="Confirmed exoplanets discovered per year, 1992–2026"),
                    width="stretch",
                    alt="Line chart of planets discovered per year. Counts stay under 100 until 2010, "
                        "spike to 872 in 2014 and 1,504 in 2016, then stay between about 150 and 560 per year.")
    source_caption()

    guide_and_notes(
        [
            "The horizontal axis is the year a planet was announced; the vertical axis is how many planets were confirmed that year.",
            "Each dot is one year. Hover over a dot to see the exact count.",
            "Labels mark the two tallest peaks and how many of those planets came from NASA's Kepler mission.",
        ],
        [
            "Discoveries grew slowly at first: only 405 planets (about 6%) were found before 2010.",
            "Two years stand out: 2014 (872 planets) and 2016 (1,504). Both peaks are credited mostly to the Kepler mission.",
            "About 86% of all known planets were confirmed in 2014 or later.",
            "From 2017 to 2026 the yearly count stays between 152 and 564, averaging about 303 per year.",
            "2026 already has 383 planets, and 286 of them come from NASA's TESS mission, up from 3 TESS planets in 2018.",
        ],
    )

# =====================================================================
# CHART 2: HISTOGRAM — planet sizes (interactive: toggle + tooltips)
# =====================================================================
with st.container(border=True):
    st.subheader("2. Planet sizes (histogram)")
    st.markdown("**Question:** Are most known exoplanets Earth-sized, or larger like Neptune and Jupiter?")

    show_calc = st.toggle("Include calculated radii (estimated from mass, not measured)", value=True)
    sizes = df.dropna(subset=["radius_earth"])
    sizes = sizes[sizes["radius_earth"] <= 30]          # 4 planets above 30 Earth radii are left out for readability
    if not show_calc:
        sizes = sizes[sizes["radius_source"] == "Measured"]

    hist = alt.Chart(sizes).mark_bar().encode(
        x=alt.X("radius_earth:Q", bin=alt.Bin(step=0.5), title="Planet radius (Earth radii, Earth = 1)"),
        y=alt.Y("count():Q", title="Number of planets", stack=True),
        color=alt.Color("radius_source:N", title="Radius value",
                        scale=alt.Scale(domain=["Measured", "Calculated"], range=["#56B4E9", "#E69F00"])),
        tooltip=[alt.Tooltip("radius_earth:Q", bin=alt.Bin(step=0.5), title="Radius range (Earth radii)"),
                 alt.Tooltip("radius_source:N", title="Radius value"),
                 alt.Tooltip("count():Q", title="Planets", format=",")],
    )
    # Reference lines so viewers have a familiar scale
    refs = alt.Chart(
        alt.Data(values=[{"x": 1, "name": "Earth"}, {"x": 3.9, "name": "Neptune"}, {"x": 11.2, "name": "Jupiter"}])
    )
    ref_lines = refs.mark_rule(color="#E6EAF2", strokeDash=[4, 4]).encode(x="x:Q")
    ref_text = refs.mark_text(align="left", dx=4, y=12, color="#E6EAF2", fontSize=12).encode(x="x:Q", text="name:N")

    st.altair_chart((hist + ref_lines + ref_text).properties(height=380, title="Distribution of exoplanet radius"),
                    width="stretch",
                    alt="Histogram of planet radius from 0 to 30 Earth radii. The tallest bars are between 1 and 3 "
                        "Earth radii. A second, mostly orange (calculated) peak sits near 12 to 14 Earth radii.")
    st.caption(f"Showing {len(sizes):,} planets. 61 planets have no radius and 4 planets larger than 30 Earth radii "
               "are not shown. Dashed lines mark Earth, Neptune, and Jupiter.")
    source_caption()

    guide_and_notes(
        [
            "The horizontal axis is planet size in Earth radii; dashed lines mark Earth (1), Neptune (3.9), and Jupiter (11.2) for scale.",
            "Each bar covers a 0.5-wide size range, and its height is how many planets fall in that range.",
            "Blue means NASA measured the radius; orange means NASA calculated it from the planet's mass. Use the toggle to hide calculated values.",
        ],
        [
            "Most known planets fall between Earth and Neptune in size: 3,128 planets are between 1 and 3 Earth radii.",
            "The median radius is 2.86 Earth radii, a size with no match in our own solar system.",
            "Only 604 planets (about 9%) are Earth-sized or smaller (1.25 Earth radii or less).",
            "A second peak sits near Jupiter's size (12–14 Earth radii, 1,144 planets), but 79% of those radii are calculated, not measured.",
            "Turning off calculated radii removes most of that second peak, so it should be read with caution.",
        ],
    )

# =====================================================================
# CHART 3: SCATTER PLOT — period vs. radius (interactive: zoom, pan, tooltips)
# =====================================================================
with st.container(border=True):
    st.subheader("3. Orbit length vs. planet size (scatter plot)")
    st.markdown("**Question:** How does planet radius relate to orbital period, and are there distinct clusters of planets?")

    pts = df.dropna(subset=["period_days", "radius_earth"])

    scatter = alt.Chart(pts).mark_circle(size=22, opacity=0.7).encode(
        x=alt.X("period_days:Q", scale=alt.Scale(type="log"), title="Orbital period (days, log scale)"),
        y=alt.Y("radius_earth:Q", scale=alt.Scale(type="log"), title="Planet radius (Earth radii, log scale)"),
        color=alt.Color("method:N", scale=METHOD_SCALE, sort=METHOD_ORDER, title="Discovery method"),
        tooltip=[alt.Tooltip("planet:N", title="Planet"),
                 alt.Tooltip("method:N", title="Method"),
                 alt.Tooltip("period_days:Q", title="Period (days)", format=",.2f"),
                 alt.Tooltip("radius_earth:Q", title="Radius (Earth radii)", format=".2f"),
                 alt.Tooltip("radius_source:N", title="Radius value"),
                 alt.Tooltip("year:O", title="Discovered")],
    ).properties(height=450, title="Orbital period vs. planet radius, colored by discovery method").interactive()

    st.altair_chart(scatter, width="stretch",
                    alt="Scatter plot with log axes of orbital period versus planet radius. Blue transit planets "
                        "cluster at short periods and small sizes; orange radial velocity planets form a flat band "
                        "near 12 to 14 Earth radii at longer periods.")
    st.caption(f"Showing {len(pts):,} planets that have both a period and a radius. Scroll to zoom, drag to pan, "
               "double-click to reset.")
    source_caption()

    guide_and_notes(
        [
            "Each dot is one planet: farther right means a longer orbit (a longer 'year'), higher means a bigger planet.",
            "Both axes use a log scale, so each gridline step is a multiplication (1, 10, 100 days), not an equal addition.",
            "Color shows how the planet was found (color-blind-safe palette). Hover for the planet's name and values.",
        ],
        [
            "Transit planets (blue) crowd the left side: their median orbit is 8 days, compared with 315 days for Radial Velocity planets.",
            "A cluster of large planets on very short orbits stands out: 761 planets orbit in under 10 days and are more than 8 times Earth's radius ('hot Jupiters').",
            "Radial Velocity planets form a flat horizontal band near 12–14 Earth radii because 1,133 of their 1,204 radii are calculated. That band reflects how the values were filled in, not a real limit.",
            "Only 12 of the 296 Microlensing planets have an orbital period, so that method barely appears here.",
            "The lower-right area (small planets with long orbits) is nearly empty. The data alone cannot tell us whether such planets are rare or just hard to detect.",
        ],
    )

# =====================================================================
# CHART 4: BOX PLOT — host star temperature by method (tooltips)
# =====================================================================
with st.container(border=True):
    st.subheader("4. Host star temperature by discovery method (box plot)")
    st.markdown("**Question:** Do different discovery methods find planets around different types of stars?")

    box_methods = ["Transit", "Radial Velocity", "Imaging"]
    stars = df[df["method"].isin(box_methods)].dropna(subset=["star_temp_k"])

    # Horizontal boxes so the method names read left to right
    box = alt.Chart(stars).mark_boxplot(extent=1.5, size=45).encode(
        y=alt.Y("method:N", sort=box_methods, title="Discovery method"),
        x=alt.X("star_temp_k:Q", title="Host star temperature (Kelvin)"),
        color=alt.Color("method:N", scale=METHOD_SCALE, legend=None),
    )
    sun = alt.Chart(alt.Data(values=[{"x": 5772, "label": "Sun (5,772 K)"}]))
    sun_line = sun.mark_rule(color="#E6EAF2", strokeDash=[4, 4]).encode(x="x:Q")
    sun_text = sun.mark_text(align="left", dx=4, y=-8, color="#E6EAF2", fontSize=12).encode(x="x:Q", text="label:N")

    st.altair_chart((box + sun_line + sun_text).properties(height=300, title="Host star temperature by discovery method"),
                    width="stretch",
                    alt="Box plot of host star temperature for Transit, Radial Velocity, and Imaging. Transit has "
                        "the highest median near 5,600 K, Radial Velocity is near 5,300 K, and Imaging has the lowest "
                        "median near 4,400 K with the widest spread.")
    st.caption("Transit: 4,778 stars · Radial Velocity: 1,201 · Imaging: 90. Microlensing is left out because only 7 of "
               "its 296 host stars have a temperature; the rare 'Other' methods are left out because they mix many techniques.")
    source_caption()

    guide_and_notes(
        [
            "Each box shows the middle 50% of host star temperatures for one method; the line inside is the median.",
            "Whiskers reach the typical range; dots beyond them are unusual stars (outliers). Hover over a box for its values.",
            "The dashed line marks our Sun's temperature (5,772 K) for comparison. Hotter stars are farther right.",
        ],
        [
            "Transit hosts have the highest median temperature of the three methods (5,593 K), close to the Sun's.",
            "Radial Velocity hosts are slightly cooler (median 5,256 K), and the two boxes overlap heavily.",
            "Imaging hosts have the lowest median (4,386 K) but by far the widest range: the middle 50% spans 3,511 to 7,098 K.",
            "Imaging also has the most extreme stars, from 415 K to 21,700 K, even though it has only 90 stars with a temperature.",
            "Because each method favors different stars, the whole catalog is not a random sample of all stars.",
        ],
    )

sidebar_brand()
