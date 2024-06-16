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
            
