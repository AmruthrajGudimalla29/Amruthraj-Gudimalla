import streamlit as st

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

# First some MPG Data Exploration
v_df_raw = load_data(path="volcano_ds_pop.csv")
v_df = deepcopy(v_df_raw)

