import streamlit as st
import sqlite3
import time
import os
from PIL import Image

# Function to initialize the database with sample comments
def initialize_database():
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    
    # Create comments table if it doesn't exist
    c.execute('''
              CREATE TABLE IF NOT EXISTS comments
              (id INTEGER PRIMARY KEY,
              media_id TEXT,
              username TEXT,
              comment TEXT)
              ''')
    
    # Add sample comments for different media types
    sample_comments = [
        ('image_1', 'alice', 'Great photo! Looks like you had fun.'),
        ('image_1', 'bob', 'Nice shot! Did you use a drone?'),
        ('image_1', 'carol', 'Amazing view! Where is this?'),
        ('video_1', 'dave', 'Haha, this reel is hilarious!'),
        ('video_1', 'eve', 'I can’t stop laughing! Great job.'),
        ('video_1', 'frank', 'Best video I’ve seen all week!'),
        ('audio_1', 'grace', 'This song is so catchy! Love it.'),
        ('audio_1', 'heidi', 'I can’t get this tune out of my head.'),
        ('audio_1', 'ivan', 'Is this on Spotify? I want to add it to my playlist.'),
    ]
    
    c.executemany('INSERT INTO comments (media_id, username, comment) VALUES (?, ?, ?)', sample_comments)
    conn.commit()
    conn.close()

# Function to fetch comments from the database
def get_comments(media_id):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('SELECT id, username, comment FROM comments WHERE media_id = ?', (media_id,))
    comments = c.fetchall()
    conn.close()
    return comments

# Function to add a comment to the database
def add_comment(media_id, username, comment):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('INSERT INTO comments (media_id, username, comment) VALUES (?, ?, ?)', (media_id, username, comment))
    conn.commit()
    conn.close()

# Function to delete a comment from the database
def delete_comment(comment_id):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    conn.commit()
    conn.close()


# Function to delete all comments from the database for a specific media_id
def delete_all_comments(media_id):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('DELETE FROM comments WHERE media_id = ?', (media_id,))
    conn.commit()
    conn.close()

# Example media identifiers
media_ids = {
    'Image': 'image_1',
    'Video Reel': 'video_1',
    'Audio File': 'audio_1'
}

# Streamlit UI
st.title('Meme Ayush')

# Media selection
media_type = st.selectbox('Select Media Type', list(media_ids.keys()))
media_id = media_ids[media_type]

# Initialize the database (only run once)
if 'initialized' not in st.session_state:
    if os.path.isfile("comments.db"):
        open('comments.db', 'w').close()
    initialize_database()
    st.session_state['initialized'] = True

if media_type == 'Image':
    img=Image.open('Ayush-Meme/Ayush_pic.jpg')
    st.image(img)
    st.write('''Picture karo Amitabh Bachchan, Bollywood ke baap, ek dial-up modem ke saamne ulta seedha dekhte hue. Caption hai, "Jab se WiFi connect karne laga, lag raha hai KBC ke agle sawal ka intezaar kar rahe hain!" 💻

Agle scene mein, Big B ek bade keyboard pe josh se type kar rahe hain. Caption: "Nephew ke Netflix account se logout kaise karein, yeh samajhne ki koshish!" 🤔🔍

Aur haan, woh timeless classic: "Jab grandma ne is hafte 37th WhatsApp chain bheji." 📱👵

Kyun ki jab Amitabh Bachchan internet se milti hai, yeh sirf ek meme nahi, balki ek box-office hit hai! 🎬''')
elif media_type == 'Video Reel':
    vid=open('Ayush-Meme/Ayush_vid.mp4','rb')
    st.video(vid)
    st.write('''Oh, Rahul Gandhi ka "Speaker Madam" wala moment Lok Sabha mein, woh toh meme-worthy hai hi! Imagine scene: Rahul Gandhi, poori seriousness ke saath, Speaker ko "Speaker Madam" bolte hue, jaise ki koi quirky sitcom ka shuruwaat ka dialogue ho.

Caption karte hain: "Jab class mein teacher ko 'Mom' keh daalo by mistake." 😅🎤

Ya fir yeh: "Woh awkwad moment jab parliamentary protocol ko family dynamics se mix kar lo." 🏛️🤦‍♂️

Kyunki jab Rahul Gandhi "Speaker Madam" bolte hain, politics se comedy gold ho jata hai! 🎭
             ''')
elif media_type =='Audio File':
    voice=open('Ayush-Meme/pani.mp3','rb')
    st.video(voice)
    st.write('''
                Ek mast meme hai jisme Uncle ji paani offer kar rahe hain! Imagine karo: Uncle ji, muskurahat ke saath, ek glass paani haath mein lekar jaise zindagi ka amrit de rahe ho.

Caption hoga: "Jab memes scroll karte karte Uncle ji aakar paani pilaane lagte hain." 🥤😄

Ya phir: "Uncle ji ka hydration service: Jab bhi memes dekhne mein dehydration lagti hai." 💧📱

Kyunki jab Uncle ji meme mein paani pilate hain, woh bas refreshing hi nahi, meme-orable bhi hota hai! 💦🌟
             ''')
# Option to manually refresh comments and delete all comments
if st.button('Report all Comments'):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.1)
        my_bar.empty()
    
    delete_all_comments(media_id)

    st.experimental_rerun()
    

# Display comments
st.header('Comments')
comments = get_comments(media_id)
#print(comments) 
if comments==[]:
    st.success("All comments are reported I will take a look at it soon!",icon="✌")
    voice=open('Ayush-Meme/Ayush_voice.mp3','rb')
    st.video(voice)
for comment in comments:

    st.write(f"**{comment[1]}**: {comment[2]}")
    if st.button('Report comment!', key=comment[0]):
        with st.spinner('Sending Report...'):
            time.sleep(5)
            st.success('Done!')
        delete_comment(comment[0])
        st.experimental_rerun()

# Add a comment
st.header('Add a Comment')
username = st.text_input('Username')
comment = st.text_area('Comment')
if st.button('Submit'):
    if username and comment:
        add_comment(media_id, username, comment)
        st.success('Comment added!')
        st.experimental_rerun()  # Refresh the comments list to include the new comment
    else:
        st.error('Please provide a username and a comment.')
