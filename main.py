# file libraries
import urllib.request
from pytube import YouTube, Playlist
import re
import webbrowser
from tqdm import tqdm

# sound manipulation libraries
import librosa
import pydub
import os
import pyrubberband
import soundfile as sf

playlist = "playlist.txt"


# with open(playlist, "r") as file:
#     next(file)
#     for line in tqdm(file):
#         search_keyword = line
#         html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
#         video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
#         playlistids = playlistids + video_ids[0] + ","
#         count += 1
#         print("https://www.youtube.com/watch?v=" + video_ids[0])  # individual links
#         if (count % 50 == 0):
#             webbrowser.open("https://www.youtube.com/watch_videos?video_ids=" + playlistids)
#             playlistids = ""
#
# playlistids = playlistids.rstrip(",")
# webbrowser.open("https://www.youtube.com/watch_videos?video_ids=" + playlistids)

def download_video(url):
    yt = YouTube(vid)

    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path="./data")

    base, ext = os.path.splitext(out_file)
    new_file = base + '.wav'

    os.replace(out_file, new_file)


def track_creation():
    sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\asgard.mp3")
    sound.export(os.getcwd() + "\\asgard.wav", format="wav")
    filename = "asgard.wav"

    sound = pydub.AudioSegment.from_file(filename)

    def speed_change(sound, speed=1.0):
        y, sr = librosa.load(os.getcwd() + "\\asgard.wav", sr=None)
        y_stretched = pyrubberband.time_stretch(y, sr, speed)
        sf.write(os.getcwd() + "\\asgard.wav", y_stretched, sr, format='wav')

    speed_change(sound, 1.5)

    # y, sr = librosa.load(filename)
    #
    # tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    #
    # print(tempo)


if __name__ == '__main__':
    # todo: clear playlist first
    choice = '0'
    while choice != '5':
        print("1. Enter a link to a youtube playlist")
        print("2. Enter links to youtube videos")
        print("3. Enter song names (there may be errors in searching)")
        print("4. Continue to track creation")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            url = input("Enter the url of the playlist (must be public) or press 'q' to exit: ")
            if url == 'q':
                break
            playlist = Playlist(url)
            for vid in tqdm(playlist.video_urls, total=len(playlist.video_urls)):
                download_video(vid)

        elif choice == '2':
            url = '0'
            while url != "q":
                url = input("Enter the url of the video or press 'q' to exit: ")
                if url == "q":
                    print()
                    break

                download_video(url)

        elif choice == '3':
            # FIXME
            url = input("Enter the url of the song: ")

        elif choice == '4':
            track_creation()
