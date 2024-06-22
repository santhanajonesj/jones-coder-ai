import pandas as pd
import googleapiclient.discovery
import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt


# Api  sample connection details
#Another_api_key = "AIzaSyCdYj4ALbIXmlMyTZ24SLR7m1fZGbdmc1w"
#Api_Key = "AIzaSyDjcDOnrVqFSzMJUqNk53owwiZZr6zsxQQ"
#Api_Name = "youtube"
#Api_Version = "v3"
#sample Channel ID : UC3LD42rjj-Owtxsa6PwGU5Q


  
def get_youtube_api_client():
  api_key= 'AIzaSyB-fo3hqqt32Z5XC1t0zpp0kFElus8xlkY'
  api_service_name = "youtube"
  api_version = "v3"
  youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
  return youtube

youtube = get_youtube_api_client()

# Function to get the channel information
def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()

    channel_information = []
    for channel_info in response["items"]:
        channel_information.append({
            "Channel_Name": channel_info["snippet"]["title"],
            "Channel_Id": channel_info["id"],
            "Subscribers": channel_info["statistics"]["subscriberCount"],
            "Views": channel_info["statistics"]["viewCount"],
            "Total_videos": channel_info["statistics"]["videoCount"],
            "Channel_description": channel_info["snippet"]["description"],
            "Playlist_Id": channel_info["contentDetails"]["relatedPlaylists"]["uploads"]
        })
    return channel_information


#print(get_channel_info(youtube,'UC3LD42rjj-Owtxsa6PwGU5Q'))

def get_playlist_info(youtube, channel_id):
    next_page_token = None
    playlist_info = []
    while True:
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for playlist_information in response['items']:
            data = {
                'Playlist_Id': playlist_information['id'],
                'Title': playlist_information['snippet']['title'],
                'Channel_Id': playlist_information['snippet']['channelId'],
                'Channel_Name': playlist_information['snippet']['channelTitle'],
                'PublishedAt': playlist_information['snippet']['publishedAt'],
                'Video_count': playlist_information['contentDetails']['itemCount']
            }


            playlist_info.append(data)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return playlist_info

#print(get_playlist_info(youtube,'UC3LD42rjj-Owtxsa6PwGU5Q'))



def get_video_ids(youtube, channel_id):
    video_ids = []
    response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
         video_ids.append(item['snippet']['resourceId']['videoId'])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return video_ids

#print(get_video_ids(youtube,'UC3LD42rjj-Owtxsa6PwGU5Q'))

from datetime import timedelta
import datetime
import re
def get_Video_Details(youtube, channel_id):
    Video_data = []
    total_minutes_final=[]
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')
    total_seconds=0

    response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    video_ids = []
    next_page_token = None
    while True:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
         video_ids.append(item['snippet']['resourceId']['videoId'])

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    

    for video_id in video_ids:
      request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id)
      response = request.execute()
        #print(response)

      for item in response['items']:
        Duration=item['contentDetails']['duration']
        #print(Duration)
        hours_parse = hours_pattern.search(Duration)
        minutes_parse = minutes_pattern.search(Duration)
        seconds_parse = seconds_pattern.search(Duration)
        minutes = int(minutes_parse.group(1)) if minutes_parse else 0
        hours  = int(hours_parse.group(1)) if hours_parse else 0
        seconds  = int(seconds_parse.group(1)) if seconds_parse else 0

        videos_seconds=int(timedelta(hours = hours, minutes = minutes, seconds = seconds).total_seconds())
        total_seconds=total_seconds+videos_seconds
        
        #print(total_seconds)

        #hours, minutes, Conversion:
        #minutes,seconds=divmod(total_seconds,60)
        #hours,minutes=divmod(minutes,60)
        #overall_time=(int(hours),int(minutes),int(seconds))

        #publish Data and time Coversion
        publish_date_str = item['snippet']['publishedAt']
        publish_date = datetime.datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')
        formatted_publish_date = publish_date.strftime('%Y-%m-%d %H:%M:%S')

        data = {
                    'Channel_Name': item['snippet']['channelTitle'],
                    'channel_Id': item['snippet']['channelId'],
                    'Video_Id': item['id'],
                    'Title': item['snippet']['title'],
                    'Tags': item['snippet'].get('tags'),
                    'Thumbnail': item['snippet']['thumbnails']['default']['url'],
                    'Description': item['snippet'].get('description'),
                    'Publishdate': formatted_publish_date,
                    'Duration(Sec)': videos_seconds,
                    'Views': item['statistics'].get('viewCount'),
                    'Likes': item['statistics'].get('likeCount'),
                    'Comments': item['statistics'].get('commentCount'),
                    'Favorite_count': item['statistics'].get('favoriteCount'),
                    'Definition': item['contentDetails']['definition'],
                    'Caption_Status': item['contentDetails']['caption']
                }

        Video_data.append(data)


    return Video_data




def get_comment_Details(youtube, video_ids):
    Comment_data = []
    try:
        for video_id in video_ids:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100
            )
            response = request.execute()

            for item in response['items']:
                publish_date_str = item['snippet']['topLevelComment']['snippet']['publishedAt']
                publish_date = datetime.datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M:%SZ')
                formatted_publish_date = publish_date.strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'Comment_id': item['snippet']['topLevelComment']['id'],
                    'Video_id': item['snippet']['topLevelComment']['snippet']['videoId'],
                    'Comment_text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'Comment_Author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'Comment_Published':  formatted_publish_date
                }
                Comment_data.append(data)
    except Exception as e:
        print("Error retrieving comments:", e)
    return Comment_data




#mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE youtubedatabase")
#mycursor.execute("SHOW DATABASES")
#for x in mycursor:
#  print(x)


#MySQL connection configuration
host = "localhost"
user = "root"
password = "Jones@1234"
database = "youtube_db"
port = "3306"  


# Function to MySQL database
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
           host = "localhost",
           user = "root",
           password = "Jones@1234",
           database = "youtube_db",
           port = "3306"  
        )
        print("Connected to MySQL database successfully")
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None

#print(connect_to_mysql())

#conn = mysql.connector.connect(
# user='sqluser', password='password', host='localhost', database='youtubedatabase')

# Function to create tables in MySQL
def create_tables(conn):
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
     # Table creation queries
    channel_table_query = """
    CREATE TABLE IF NOT EXISTS channel_data (
        Channel_Name VARCHAR(255),
        Channel_Id VARCHAR(255) NOT NULL,
        Subscribers INT,
        Views INT,
        Total_videos INT,
        Channel_description TEXT,
        Playlist_Id VARCHAR(255),
        PRIMARY KEY(Channel_Id)
    )
    """
    video_table_query = """
    CREATE TABLE IF NOT EXISTS video_data (
        Channel_Name VARCHAR(255),
        Channel_Id VARCHAR(255),
        Video_Id VARCHAR(255),
        Title VARCHAR(255),
        Tags TEXT,
        Thumbnail TEXT,
        Description TEXT,
        Publishdate DATETIME,
        Duration INT,
        Views INT,
        Likes INT,
        Comments INT,
        Favorite_count INT,
        Definition VARCHAR(255),
        Caption_Status VARCHAR(255),
        PRIMARY KEY(Video_Id)
    )
    """
    comment_table_query = """
    CREATE TABLE IF NOT EXISTS comment_data (
        Comment_id VARCHAR(255),
        Video_id VARCHAR(255),
        Comment_text TEXT,
        Comment_Author VARCHAR(255),
        Comment_Published DATETIME,
        PRIMARY KEY (Comment_id)
    )
    """
    playlist_table_query = """
    CREATE TABLE IF NOT EXISTS playlist_data (
        Playlist_Id VARCHAR(255),
        Title VARCHAR(255),
        Channel_Id VARCHAR(255),
        Channel_Name VARCHAR(255),
        PublishedAt DATETIME,
        Video_count INT
    )
    """
    try:
        # Execute table creation queries
        cursor.execute(channel_table_query)
        cursor.execute(video_table_query)
        cursor.execute(comment_table_query)
        cursor.execute(playlist_table_query)

        conn.commit()
        print("Tables created successfully in MySQL")
    except mysql.connector.Error as e:
        print("Error creating tables in MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()

#Testing
#print(create_tables(conn))
#cursor = conn.cursor()
#cursor.execute("DROP TABLE IF EXISTS channel_data ")

# Test the below functions
conn = connect_to_mysql()
if conn is not None:
    create_tables(conn)
    conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jones@1234",
    database="youtube_db",
    port="3306"
)


# Function to insert channel details into MySQL database
def insert_channel_info_to_mysql(conn, channel_info):
    cursor = conn.cursor()
    try:
        for info in channel_info:
            
            insert_query = """
            INSERT INTO channel_data (Channel_Name, Channel_Id, Subscribers, Views, Total_videos, Channel_description, Playlist_Id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the query with data from the channel_info list
            cursor.execute(insert_query, (info["Channel_Name"], info["Channel_Id"], info["Subscribers"], info["Views"], info["Total_videos"], info["Channel_description"], info["Playlist_Id"]))
        
        conn.commit()
        return "Success"
    except mysql.connector.Error as e:
        return "Duplicate"
        conn.rollback()
    finally:
        cursor.close()


# Function to insert video data into MySQL database
def insert_video_data_to_mysql(conn, video_data):
    cursor = conn.cursor()
    try:
        for data in video_data:
            tags = data.get('Tags', [])
            if not isinstance(tags, list):
                tags = [tags]  
            tags = [tag for tag in tags if tag is not None]
            insert_query = """
            INSERT INTO Video_data (Channel_Name, Channel_Id, Video_Id, Title, Tags, Thumbnail, Description, Publishdate, Duration, Views, Likes, Comments, Favorite_count, Definition, Caption_Status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the query with data from the video_data list
            cursor.execute(insert_query, (
                data['Channel_Name'],
                data['channel_Id'],
                data['Video_Id'],
                data['Title'],
                ",".join(tags),  
                data['Thumbnail'],
                data.get('Description', ''),
                data['Publishdate'],
                data['Duration(Sec)'],
                data['Views'],
                data.get('Likes', 0),  
                data.get('Comments', 0),  
                data.get('Favorite_count', 0),  
                data['Definition'],
                data['Caption_Status']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Video data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting video data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()


# Function to insert comment data into MySQL database
def insert_comment_data_to_mysql(conn, comment_data):
    cursor = conn.cursor()
    try:
        for data in comment_data:
            insert_query = """
            INSERT INTO comment_data (Comment_id, Video_id, Comment_text, Comment_Author, Comment_Published) 
            VALUES (%s, %s, %s, %s, %s)
            """
            # Execute the query with data from the comment_data list
            cursor.execute(insert_query, (
                data['Comment_id'],
                data['Video_id'],
                data['Comment_text'],
                data['Comment_Author'],
                data['Comment_Published']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Comment data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting comment data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()

# Function to insert playlist data into MySQL database
def insert_playlist_data_to_mysql(conn, playlist_data):
    cursor = conn.cursor()
    try:
        for data in playlist_data:
            insert_query = """
            INSERT INTO playlist_data (Playlist_Id, Title, Channel_Id, Channel_Name, PublishedAt, Video_count) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # print(data['PublishedAt'].replace("T", " ").replace("Z", " "))
            # Execute the query with data from the playlist_data list
            cursor.execute(insert_query, (
                data['Playlist_Id'],
                data['Title'],
                data['Channel_Id'],
                data['Channel_Name'],
                data['PublishedAt'].replace("T", " ").replace("Z", " "),
                # format(data['PublishedAt'],"yyyy-mm-dd-hh-mm"),
                data['Video_count']
            ))
        
        # Commit the changes to the database
        conn.commit()
        print("Playlist data inserted into MySQL successfully!")
    except mysql.connector.Error as e:
        print("Error inserting playlist data into MySQL:", e)
        conn.rollback()
    finally:
        cursor.close()


st.title(":red[YOUTUBE CHANNEL COLLECTION]")
st.write("This can collect channel information by using channel id  and retrieve all the channel details,playlist details,comment details & video details")
                    
youtube = get_youtube_api_client()

channel_id_input_placeholder = 'channel_id_input'
channel_id = st.text_input('Enter your Channel ID', key=channel_id_input_placeholder)

if len(channel_id)>0:
    
    if st.button("Import Youtube Channel Details"):
        # Retrieving data from YouTube API
        playlist_data =get_playlist_info (youtube, channel_id)
        Video_data = get_video_ids(youtube,channel_id)
        comment_data = get_comment_Details(youtube, Video_data)
        video2 = get_Video_Details(youtube,channel_id)
        channel_data = get_channel_info(youtube, channel_id)
        
        # get_channel_info

        # '''
        # "Channel_Name": i["snippet"]["title"],
        # "Channel_Id": i["id"],
        # "Subscribers": i["statistics"]["subscriberCount"],
        # "Views": i["statistics"]["viewCount"],
        # "Total_videos": i["statistics"]["videoCount"],
        # "Channel_description": i["snippet"]["description"],
        # "Playlist_Id": i["contentDetails"]["relatedPlaylists"]["uploads"]
        # '''
        # Establishing connection to MySQL database
        conn = connect_to_mysql()

        # Creating tables if they don't exist
        if conn is not None:
            create_tables(conn)

            # Inserting data into MySQL tables
            result = insert_channel_info_to_mysql(conn, channel_data)
            if result == "Success":
                insert_video_data_to_mysql(conn, video2)
                insert_comment_data_to_mysql(conn, comment_data)
                insert_playlist_data_to_mysql(conn, playlist_data)
                st.write("Youtube Channel Data migrated to MySQL successfully!")
            else:
                st.write("Youtube Channel Details Already Available, Try to give Alternate Channel ID")

            # Closing the MySQL connection
            conn.close()

            # Displaying success message
            
