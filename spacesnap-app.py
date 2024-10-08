import requests
import pandas as pd
import streamlit as st
import random
import os
import base64

# NASA APOD API URL
APOD_URL = "https://api.nasa.gov/planetary/apod"

# API key
API_KEY = "6x1BFJezktd34g2615qORdf3FfOpIo0g3NcTX2tZ"

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Display the APOD and its information
st.set_page_config(page_title="SpaceSnap: NASA Astronomy Picture of the Day")

st.title("SpaceSnap: NASA Astronomy Picture of the Day 🔭")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
set_background(f"{BASE_DIR}/img/bg.jpeg")

# Fetch APOD data
def fetch_apod_data():
    response = requests.get(f"{APOD_URL}?api_key={API_KEY}")
    data = response.json()
    return data

def fetch_apod_data_date(date):
    response = requests.get(f"{APOD_URL}?api_key={API_KEY}&date={date}")
    data = response.json()
    return data

def display_apod(data):
    st.title(data['title'])
    st.image(data["url"], use_column_width=True)
    st.write(f"**Date:** {data['date']}")
    st.write(f"**Explanation:** \n\n{data['explanation']}")

# Get APOD
apod_data = fetch_apod_data()
display_apod(apod_data)

today = pd.Timestamp.today().strftime("%Y-%m-%d")

# Allow users to browse previous APODs
st.sidebar.title("Browse APODs")
selected_date = st.sidebar.date_input("Select date", pd.Timestamp.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")
if selected_date_str != today:
    apod_data = fetch_apod_data_date(selected_date_str)
    display_apod(apod_data)

import random

# Random APOD generator
st.sidebar.title("Random APOD")
if st.sidebar.button("Show random APOD"):
    # Generate a random date between June 16, 1995 (APOD launch date) and today
    start_date = pd.to_datetime("1995-06-16")
    end_date = pd.Timestamp.today()
    random_date = pd.to_datetime(random.randint(start_date.value, end_date.value))
    random_date_str = random_date.strftime("%Y-%m-%d")

    # Fetch and display the APOD for the random date
    apod_data = fetch_apod_data_date(random_date_str)
    display_apod(apod_data)
