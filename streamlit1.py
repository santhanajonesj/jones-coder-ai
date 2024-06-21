import streamlit as st
import pandas as pd

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
st.title(":red[YOUTUBE CHANNEL COLLECTION]")
st.title("CREATED BY SANTHANA JONES J")
st.write("This can collect channel information by using channel id  and retrieve all the channel details,playlist details,comment details & video details")
with st.sidebar:
    st.title(":red[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
    st.header("SKILLS TAKE AWAY")
    st.caption("PYTHON SCRIPTING")
    st.caption("DATA COLLECTION ")
    st.caption("MySQL")
    st.caption("API INTEGRATON")
    st.caption("DATA MANAGEMENT USING")
    st.write("## :orange[Select any question to get Insights]")
    st.selectbox('Questions',
    ['Click the question that you would like to query',
    '1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])
    

channel_id_input_placeholder = 'channel_id_input'
channel_id = st.text_input('Enter your Channel ID', key=channel_id_input_placeholder)


if len(channel_id)>0:
    
    if st.button("Import Youtube Channel Details"):
        # Retrieving data from YouTube API
        playlist_info =get_playlist_info (youtube, channel_id)
        Video_data = get_video_ids(youtube,channel_id)
        comment_data = get_comment_Details(youtube, Video_data)
        video2 = get_Video_Details(youtube,channel_id)
        channel_data = get_channel_info(youtube, channel_id)
        
       
       
       
    if questions == '1. What are the names of all the videos and their corresponding channels?':
        mycursor.execute("""SELECT title AS Video_Title, channel_name AS Channel_Name FROM videos ORDER BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        mycursor.execute("""SELECT channel_name 
        AS Channel_Name, total_videos AS Total_Videos
                            FROM channels
                            ORDER BY total_videos DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Number of videos in each channel :]")
        #st.bar_chart(df,x= mycursor.column_names[0],y= mycursor.column_names[1])
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, title AS Video_Title, views AS Views 
                            FROM videos
                            ORDER BY views DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most viewed videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT a.video_id AS Video_id, a.title AS Video_Title, b.Total_Comments
                            FROM videos AS a
                            LEFT JOIN (SELECT video_id,COUNT(comment_id) AS Total_Comments
                            FROM comments GROUP BY video_id) AS b
                            ON a.video_id = b.video_id
                            ORDER BY b.Total_Comments DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
          
    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name,title AS Title,likes AS Likes_Count 
                            FROM videos
                            ORDER BY likes DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most liked videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT title AS Title, likes AS Likes_Count
                            FROM videos
                            ORDER BY likes DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
         
    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, views AS Views
                            FROM channels
                            ORDER BY views DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Channels vs Views :]")
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        mycursor.execute("""SELECT channel_name AS Channel_Name
                            FROM videos
                            WHERE published_date LIKE '2022%'
                            GROUP BY channel_name
                            ORDER BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name, 
                        SUM(duration_sec) / COUNT(*) AS average_duration
                        FROM (
                            SELECT channel_name, 
                            CASE
                                WHEN duration REGEXP '^PT[0-9]+H[0-9]+M[0-9]+S$' THEN 
                                TIME_TO_SEC(CONCAT(
                                SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'H', 1), 'T', -1), ':',
                            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'M', 1), 'H', -1), ':',
                            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'M', -1)
                            ))
                                WHEN duration REGEXP '^PT[0-9]+M[0-9]+S$' THEN 
                                TIME_TO_SEC(CONCAT(
                                '0:', SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'M', 1), 'T', -1), ':',
                                SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'M', -1)
                            ))
                                WHEN duration REGEXP '^PT[0-9]+S$' THEN 
                                TIME_TO_SEC(CONCAT('0:0:', SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'S', 1), 'T', -1)))
                                END AS duration_sec
                        FROM videos
                        ) AS subquery
                        GROUP BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names
                          )
        st.write(df)
        st.write("### :green[Average video duration for channels :]")
        # get_channel_info

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
            


