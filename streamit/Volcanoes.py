import streamlit as st

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
st.write("hello world")
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Volcano Dashboard 🌋")

# --- Load Data ---
@st.cache_data
def load_data(path):
    v_df = pd.read_csv(path)
    return v_df

v_df = load_data("./streamit/volcano_ds_pop.csv")

if st.checkbox("Show Dataframe"):

    st.subheader("This is my dataset:")
    st.dataframe(data=v_df)

# --- Create two columns for dropdowns ---
col1, col2 = st.columns(2)

# --- Dropdown for Country ---
countries = sorted(v_df["Country"].dropna().unique())
selected_country = col1.selectbox("Select a Country", ["All"] + countries)

# --- Dropdown for Region ---
if selected_country == "All":
    regions = sorted(v_df["Region"].dropna().unique())
else:
    regions = sorted(v_df[v_df["Country"] == selected_country]["Region"].dropna().unique())

selected_region = col2.selectbox("Select a Region", ["All"] + regions)

# --- Filter Data ---
filtered_v_df = v_df.copy()
if selected_country != "All":
    filtered_v_df = filtered_v_df[filtered_v_df["Country"] == selected_country]
if selected_region != "All":
    filtered_v_df = filtered_v_df[filtered_v_df["Region"] == selected_region]

# --- Show Result ---
st.subheader("Filtered Volcano Data")
st.dataframe(filtered_v_df)

if not filtered_v_df.empty:
    # Make sure Elev is positive (no negative bubble sizes)
    filtered_v_df["Elev"] = filtered_v_df["Elev"].abs()

    fig = px.scatter_geo(
        filtered_v_df,
        lat="Latitude",
        lon="Longitude",
        color="Type",  # color by volcano type
        hover_name="Volcano Name",
        size="Elev",
        projection="natural earth",
        title=f"Volcano Types - {selected_country if selected_country != 'All' else 'World'}"
    )
    st.plotly_chart(fig, use_container_width=True)

      # --- Bar Chart: Count of volcanoes by Type ---
    type_counts = filtered_v_df["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]

    bar_fig = px.bar(
        type_counts,
        x="Type",
        y="Count",
        color="Type",
        title="Number of Volcanoes by Type (Log Scale)",
        text="Count",
        log_y=True  # <-- this makes the y-axis logarithmic
    )

    # Make bars thicker
    bar_fig.update_traces(marker_line_width=0, width=0.5)
    bar_fig.update_layout(showlegend=False, bargap=0.3)

    st.plotly_chart(bar_fig, use_container_width=True)
   
else:
    st.warning("No data available for the selected filters.")