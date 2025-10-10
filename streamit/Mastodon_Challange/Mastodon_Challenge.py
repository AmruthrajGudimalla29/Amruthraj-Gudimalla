
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# --- Logo and Title ---
#st.image("mastodon_logo.png", width=100)
st.title("./Mastodon_Challange/Mastodon Challenge")

#####################################################################
#Sentiment
sentiment_df = pd.read_csv("./Mastodon_Challange/combined_sentiment_results.csv")

#remove japanese hashtags

hashtags = sentiment_df['hashtag'].unique()
for item in [hashtags[12],hashtags[18], hashtags[19]]:
    sentiment_df = sentiment_df[sentiment_df['hashtag'] != item]


#Sentiment plot

# Map sentiment values using logic operators
sentiment_df['sentiment_category'] = np.where(sentiment_df['sentiment'] > 0, 'Positive',
                                     np.where(sentiment_df['sentiment'] < 0, 'Negative', 'Neutral'))


#####################################################################
# Plotting the TimeSeries
df = pd.read_csv("final_df.csv")

df = df.rename(columns={"Unnamed: 0":"date"})

hashtag_lst = df.columns
hashtag_lst = hashtag_lst.drop('date')

hashtag = st.selectbox("Select a hashtag", hashtag_lst)


fig = go.Figure()
# --- Show filtered dataframe ---
check_bool = st.checkbox("Show All Data")
if check_bool:
    for hashtag in hashtag_lst:
        fig.add_trace(go.Scatter(x=df['date'],
                                y=df[hashtag],
                                name=hashtag))  

 

else:   
    st.subheader("Filtered Dataset")
    fig.add_trace(go.Scatter(x=df['date'],
                             y=df[hashtag],
                             name=hashtag))

#hover
fig.update_layout(hovermode="x unified",
                 paper_bgcolor="lightgray",
                 plot_bgcolor="white",
                 title="Performance of trending hashtags over the past 3 months",
                 xaxis_title="date (m-d)",
                 yaxis_title="number of posts",
                 xaxis_title_font=dict(size=18),
                 yaxis_title_font=dict(size=18),
                 xaxis=dict(nticks=10)
                 )

st.plotly_chart(fig)

#st.header("Barplot")
st.subheader("Sentiment Analysis")

if check_bool:
    # Summarize sentiment counts
    sentiment_counts = sentiment_df.groupby(['hashtag', 'sentiment_category']).size().reset_index(name='count') 

        # Create the grouped bar plot
    sentiment_fig = px.bar(sentiment_counts, 
                x='hashtag', 
                y='count', 
                color='sentiment_category', 
                barmode='group',
                labels={'hashtag': 'Hashtag', 'count': 'Count'},
                title='Sentiment Count by Hashtag')

else:
    sentiment_counts = sentiment_df[sentiment_df['hashtag']==hashtag].groupby('sentiment_category').size().reset_index(name='count')

    # Create the grouped bar plot
    sentiment_fig = px.bar(sentiment_counts, 
                x='sentiment_category', 
                y='count', 
                color='sentiment_category', 
                barmode='group',
                labels={'hashtag': 'Hashtag', 'count': 'Count'},
                title='Sentiment Count by Hashtag')

st.plotly_chart(sentiment_fig)