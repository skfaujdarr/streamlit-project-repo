import os
os.environ["STREAMLIT_USE_PYARROW"] = "0"

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Spotify Dashboard", layout="wide")

# ---------------- DARK STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #111827;
}
h1, h2, h3 {
    color: #00FFAA;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🎧 Spotify & YouTube Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    data = pd.read_csv("Spotify Youtube Dataset.csv")
    data.drop(columns=['Unnamed: 0', 'Url_spotify', 'Uri', 'Url_youtube'], inplace=True)
    data['Likes'] = data['Likes'].fillna(0)
    data['Comments'] = data['Comments'].fillna(0)
    data.dropna(inplace=True)
    return data

data = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", width=100)
st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "Top Artists",
        "Top Tracks",
        "Album Distribution",
        "Top Channels"
    ]
)

st.sidebar.markdown("---")

# FILTER
selected_artist = st.sidebar.selectbox(
    "Filter by Artist",
    ["All"] + sorted(data['Artist'].unique().tolist())
)

if selected_artist != "All":
    data = data[data['Artist'] == selected_artist]

# ---------------- OVERVIEW ----------------
if option == "Overview":

    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Tracks", len(data))
    col2.metric("Artists", data['Artist'].nunique())
    col3.metric("Channels", data['Channel'].nunique())

    st.markdown("---")
    st.subheader("Dataset Sample")

    st.dataframe(data.head())  # FIXED

# ---------------- TOP ARTISTS ----------------
elif option == "Top Artists":

    st.subheader("🔥 Top 10 Artists by Views")

    artist_views = (
        data.groupby('Artist')['Views']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.dataframe(artist_views.reset_index())  # FIXED

    with col2:
        fig, ax = plt.subplots()
        sns.barplot(x=artist_views.values, y=artist_views.index, ax=ax)
        ax.set_title("Top Artists", color="white")
        ax.set_facecolor("#0E1117")
        fig.patch.set_facecolor("#0E1117")
        st.pyplot(fig)

# ---------------- TOP TRACKS ----------------
elif option == "Top Tracks":

    st.subheader("🎵 Top 10 Tracks")

    top_tracks = (
        data[['Track', 'Stream']]
        .sort_values(by='Stream', ascending=False)
        .head(10)
    )

    st.dataframe(top_tracks)  # FIXED

# ---------------- ALBUM DISTRIBUTION ----------------
elif option == "Album Distribution":

    st.subheader("📀 Album Distribution")

    album_counts = data['Album_type'].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(album_counts.reset_index())  # FIXED

    with col2:
        fig, ax = plt.subplots()
        ax.pie(
            album_counts,
            labels=album_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )
        fig.patch.set_facecolor("#0E1117")
        st.pyplot(fig)

# ---------------- TOP CHANNELS ----------------
elif option == "Top Channels":

    st.subheader("📺 Top Channels")

    channel_views = (
        data.groupby('Channel')['Views']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.dataframe(channel_views.reset_index())  # FIXED

    with col2:
        fig, ax = plt.subplots()
        sns.barplot(x=channel_views.values, y=channel_views.index, ax=ax)
        ax.set_title("Top Channels", color="white")
        ax.set_facecolor("#0E1117")
        fig.patch.set_facecolor("#0E1117")
        st.pyplot(fig)