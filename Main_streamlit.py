import streamlit as st
import base64
import pandas as pd
import googleapiclient.discovery 


st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzdobHdmZTYwbDZpM256OTNieG55NGUyNmxvOGx2cGw0d2ZrNnVuaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/13Nc3xlO1kGg3S/giphy.webp")
st.title(":red[YOUTUBE DATA HARVESTING AND WAREHOUSING USING STREAMLIT]")
st.write("YouTube Data Harvesting and Warehousing project - Provide you the youtube channel details,playlist details,video details and comment details")
 
if st.button(":movie_camera: Youtube Channel Data Collection"):
    st.switch_page("pages/Youtube_Data_Harvesting_Warehousing.py")
if st.button(":question:&:pencil: Queries & Result"):
    st.write("***Analyze Based on the Given Question***")
    st.switch_page("pages/Youtube_Channel_Query_Analysis.py")
