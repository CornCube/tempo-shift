import streamlit as st
import os
from pytube import YouTube, Playlist, Search
import time
import librosa
import pydub
import soundfile as sf

# Create directories if they don't exist
def create_dirs():
    if "data" not in os.listdir(os.getcwd()):
        os.mkdir(os.getcwd() + "/data")
    if "adjusted" not in os.listdir(os.getcwd()):
        os.mkdir(os.getcwd() + "/adjusted")

# Download the audio from a YouTube video
def download_video(video):
    yt = YouTube(video)
    video_stream = yt.streams.filter(only_audio=True).first()
    out_file = video_stream.download(output_path=os.getcwd() + "/data")
    base = os.path.splitext(out_file)[0]
    new_base = base + '_' + str(int(time.time()))
    os.rename(out_file, new_base + '.wav')

# Download the audio from a YouTube playlist
def download_playlist(url):
    playlist = Playlist(url)
    progress_bar = st.progress(0)
    for idx, vid in enumerate(playlist.video_urls):
        with st.spinner('Downloading audio files...'):
            download_video(vid)
            time.sleep(0.1)
        progress_bar.progress((idx + 1) / len(playlist.video_urls))

# Download the audio from a song name
def download_song(name):
    song = Search(name)
    url = song.results[0].watch_url
    download_video(url)

# Create the tracks
def track_creation(bpm):
    song_files = os.listdir(os.getcwd() + "/data")
    tempo = st.text_input("Enter the tempo of the song:")
    progress_bar = st.progress(0)
    for idx, filename in enumerate(song_files):
        y, sr = librosa.load(os.getcwd() + "/data/" + filename, sr=None)
        factor = bpm / float(tempo)
        y_fast = librosa.effects.time_stretch(y, factor)
        sf.write(os.getcwd() + "/adjusted/" + filename, y_fast, sr)
        progress_bar.progress((idx + 1) / len(song_files))

# Combine tracks into one file
def combine_tracks():
    adjusted_dir = 'adjusted'
    combined_filename = os.path.join(adjusted_dir, "combined.mp3")
    if os.path.exists(combined_filename):
        os.remove(combined_filename)
    file_list = [f for f in os.listdir(adjusted_dir) if f.endswith(".wav")]

    if not file_list:
        st.error("No WAV files found in the adjusted directory.")
        return

    combined_audio = pydub.AudioSegment.empty()

    progress_bar = st.progress(0)

    for idx, file in enumerate(file_list):
        with st.spinner('Processing audio files...'):
            combined_audio += pydub.AudioSegment.from_file(os.path.join(adjusted_dir, file))
            time.sleep(0.1)
        progress_bar.progress((idx + 1) / len(file_list))

    combined_audio.export(combined_filename, format="mp3") 

# Streamlit Interface
def main():
    st.title("YouTube Downloader + Tempo Shift")

    st.markdown("""
    This app allows you to download audio from YouTube videos, adjust the tempo to match a desired BPM, 
    and combine adjusted tracks into one file.
    """)

    create_dirs()

    st.subheader("Step 1: Download songs from YouTube")
    st.markdown("""
    These songs will be saved in the `\\data` folder. If you already have songs downloaded, make sure they are in `.wav` format and put them in the `\\data` folder.
    """)
                
    method = st.radio(
        "Download Method:",
        ["Enter a YouTube playlist link", "Enter YouTube video links", "Enter song names"]
    )

    if method == "Enter a YouTube playlist link":
        st.markdown("Download a song using a YouTube playlist link")
        url = st.text_input("Enter the URL of the playlist (must be public):")
        if st.button("Download Playlist"):
            download_playlist(url)

    elif method == "Enter YouTube video links":
        st.markdown("Download a song using a YouTube video link")
        url = st.text_input("Enter the URL of the video:")
        if st.button("Download Video"):
            download_video(url)

    elif method == "Enter song names":
        st.markdown("Download a song using a song name (first result from YouTube)")
        name = st.text_input("Enter the name of the song:")
        if st.button("Search and Download Song"):
            download_song(name)
    st.caption(f"Current working directory: {os.getcwd()}")

    st.subheader("Step 2: Create adjusted tracks")
    st.markdown("""
    Create tracks from the downloaded audio files inside of the data folder.
    The tracks will be saved in the `\\adjusted` folder.
    You will need the bpm of each song, which can be found online or at one of these websites:
    - [GetSongBPM](https://getsongbpm.com/search)
    - [Tunebat Analyzer](https://tunebat.com/Analyzer)
    - [Beats Per Minute Online](https://www.beatsperminuteonline.com/)
    - [SongBPM](https://songbpm.com/)
                
    If the tempo of the song in question is much higher/lower than the tempo that you are shifting to, 
                it is better to use a halved/doubled tempo to avoid distorting the original song too 
                much. For example, 'The Top' by Ken Blast is 160 bpm. If we are shifting it to 88 bpm, 
                use 80 bpm as the actual value instead of 160 bpm to prevent the song from being slowed 
                by ~50%.

    This process works best with songs that are 1) similar in tempo to the desired tempo and 2) have a fairly consistent rhythm.
    """)
    
    bpm = st.text_input("Enter the desired BPM:")
    if st.button("Create Tracks"):
        track_creation(bpm)

    st.subheader("Step 3: Combine adjusted tracks")
    st.markdown("""
    Combine the tracks in the adjusted folder into one file.
    """)
    
    if st.button("Combine Tracks"):
        combine_tracks()

if __name__ == "__main__":
    main()