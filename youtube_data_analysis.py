import pandas as pd
import numpy as np
import googleapiclient.discovery
import streamlit as st
import datetime
import matplotlib.pyplot as plt
import mysql.connector

conn = mysql.connector.connect(
user='root', password='Jones@1234', host='localhost', database='youtube_db')

# MySQL connection configuration
host = "localhost",
user = "root",
password = "Jones@1234",
database = "youtube_db",
mysql_port = "3306"

# Function to connect to MySQL database
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jones@1234",
            database="youtube_db",
            port="3306"
        )
        print("Connected to youtubedatabase successfully")
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to youtubedatabase :", e)
        return None




def execute_query(query):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jones@1234",
        database="youtube_db",
        port="3306"
    )
    cursor = mydb.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    mydb.close()
    return data


st.title(":red[YOUTUBE CHANNEL ANALYSIS]")
st.text("WELCOME EVERYONE")

Question = st.selectbox(
    " Please select a question:",
    ("1.What are the names of all the videos and their corresponding channels?",
     "2.Which channels have the most number of videos, and how many videos do they have?",
     "3.What are the top 10 most viewed videos and their respective channels?",
     "4.How many comments were made on each video, and what are their corresponding video names?",
     "5.Which videos have the highest number of likes and what are their corresponding channel names?",
     "6.What is the total number of likes for each video and what are their corresponding video names?",
     "7.What is the total number of views for each channel and what are their corresponding channel names?",
     "8.What are the names of all the channels that have published videos in the year 2022?",
     "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
     "10.Which videos have the highest number of comments, and what are their corresponding channel names?"),
    )

if Question == "1.What are the names of all the videos and their corresponding channels?":
     query = '''SELECT C.Channel_Name, V.Title 
        FROM channel_data as C 
        JOIN video_data as V 
        ON C.Channel_Id = V.Channel_Id;
    '''
     result = execute_query(query)
     df1 = pd.DataFrame(result, columns=["Channel_Name","Title"])
     df1.index =df1.index + 1
     st.write(df1)


elif Question == "2.Which channels have the most number of videos, and how many videos do they have?":
        query = '''
            SELECT Channel_Name, Total_videos 
            FROM channel_data
            ORDER BY Total_videos DESC;
        '''
        result = execute_query(query)
        df2 = pd.DataFrame(result, columns=["Channel_Name", "Total_videos"])
        df2.index =df2.index + 1
        st.write(df2)
        st.bar_chart(data=df2,x='Channel_Name',y='Total_videos', color="#ffaa00", width=400, height=400, use_container_width=True)



elif Question == "3.What are the top 10 most viewed videos and their respective channels?":
        query = '''
                select Channel_Name,Title,Views from video_data
                order by Views desc limit 10;
                '''
        result = execute_query(query)
        df3 = pd.DataFrame(result, columns=["Channel_Name", "Title","Views"])
        df3.index =df3.index + 1
        st.write(df3)
        st.bar_chart(data=df3,x='Title',y='Views', color="#fd0", width=400, height=400, use_container_width=True)




elif Question == "4.How many comments were made on each video, and what are their corresponding video names?" :
        query = '''
                select Ch.Channel_Name, V.Title,V.Comments from video_data as V,channel_data as Ch
                where V.Channel_Id=Ch.Channel_Id
                '''
        result = execute_query(query)
        df4 = pd.DataFrame(result, columns=["Channel_Name","Title","Comments"])
        df4.index =df4.index + 1
        st.write(df4)
        st.bar_chart(data=df4,x='Title',y='Comments', color="#f0f", width=400, height=400, use_container_width=True)
        

elif Question == "5.Which videos have the highest number of likes and what are their corresponding channel names?" :
        query = '''
                select Ch.Channel_Name,V.Likes from channel_data as Ch,video_data as V 
                where Ch.Channel_Id=V.Channel_Id 
                ORDER BY V.Likes desc
                '''
        result = execute_query(query)
        df5 = pd.DataFrame(result, columns=["Channel_Name","Likes"])
        df5.index =df5.index + 1
        st.write(df5)
        st.bar_chart(data=df5,x='Channel_Name',y='Likes', color="#f0f", width=400, height=400, use_container_width=True)



elif Question == "6.What is the total number of likes for each video and what are their corresponding video names?":
        query = '''
                select Channel_Name,Title,Likes from video_data 
                ORDER BY Likes desc
                '''
        result = execute_query(query)
        df6 = pd.DataFrame(result, columns=[ "Channel_Name","Title","Likes"])
        df6.index =df6.index + 1      
        st.write(df6)
        st.bar_chart(data=df6,x='Title',y='Likes', color="#f0f", width=400, height=400, use_container_width=True)




elif Question == "7.What is the total number of views for each channel and what are their corresponding channel names?" :
        query = '''
                select Channel_Name,Views from channel_data order by Views desc;
                '''
        result = execute_query(query)
        df7 = pd.DataFrame(result, columns=[ "Channel_Name","Views"])
        df7.index =df7.index + 1
        st.write(df7)
        st.bar_chart(data=df7,x='Channel_Name',y='Views', color="#f0f", width=400, height=400, use_container_width=True)



elif Question == "8.What are the names of all the channels that have published videos in the year 2022?" :
        query = '''
                select Channel_Name from video_data
                where EXTRACT(YEAR FROM Publishdate) = 2022;
                '''
        result = execute_query(query)
        df8 = pd.DataFrame(result, columns=[ "Channel_Name"])
        df8.index =df8.index + 1
        st.write(df8)
        #st.bar_chart(data=df8,x='Title',y='Comments', color="#f0f", width=400, height=400, use_container_width=True)



elif Question == "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?" :
        query = '''
                SELECT c.Channel_Name,ROUND(AVG(Duration), 0) AS Avg_Duration
                FROM channel_data c, video_data v where c.Channel_Id = v.Channel_Id
                GROUP BY c.Channel_Name;;
                '''
        result = execute_query(query)
        df9 = pd.DataFrame(result, columns=[ "Channel_Name","Avg_Duration"])
        df9.index =df9.index + 1
        st.write(df9)
        st.bar_chart(data=df9,x='Channel_Name',y='Avg_Duration', color="#000ff", width=400, height=400, use_container_width=True)


elif Question == "10.Which videos have the highest number of comments, and what are their corresponding channel names?" :
        query = '''
                SELECT c.Channel_Name, v.Title, COUNT(co.Comment_Id) AS Num_Comments
                FROM channel_data c
                JOIN video_data v ON c.Channel_Id = v.Channel_Id
                LEFT JOIN comment_data co ON v.Video_Id = co.Video_Id
                GROUP BY c.Channel_Name, v.Title
                ORDER BY Num_Comments DESC
                LIMIT 10;
                '''
        result = execute_query(query)
        df10 = pd.DataFrame(result, columns=[ "Channel_Name","Title","Num_Comments"])
        df10.index =df10.index + 1
        st.write(df10)
        st.bar_chart(data=df10,x='Channel_Name',y='Num_Comments', color="#04f", width=400, height=400, use_container_width=True)
        