# file libraries
from pytube import YouTube, Playlist, Search
from tqdm import tqdm
import re

# sound manipulation libraries
import librosa
import pydub
import os
import pyrubberband
import soundfile as sf


def download_video(video):
    yt = YouTube(video)

    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=os.getcwd() + "\\data")

    base = os.path.splitext(out_file)[0]
    os.rename(out_file, base + '.wav')


def track_creation(bpm, filename):
    sound = pydub.AudioSegment.from_file("./data/" + filename)
    y, sr = librosa.load(os.getcwd() + "./data/" + filename, sr=None)

    x = input("Do you want to manually enter the bpm? (y/n): ")
    if x == "y":
        tempo = input("Enter the bpm for " + filename + ": ")
    else:
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        print(filename + " has an average bpm of " + str(tempo))

    def speed_change(sound, speed=1.0):
        y_stretched = pyrubberband.time_stretch(y, sr, speed)
        if os.getcwd() + "./adjusted/" + filename in os.listdir(os.getcwd() + "./adjusted/"):
            os.remove(os.getcwd() + "./adjusted/" + filename)
        sf.write(os.getcwd() + "./adjusted/" + filename, y_stretched, sr, format='wav')

    factor = bpm / float(tempo)
    speed_change(sound, factor)

    # y, sr = librosa.load(os.getcwd() + "./adjusted/" + filename, sr=None)
    # tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    # print(filename + " has an adjusted bpm of " + str(tempo))
    print("Track has been adjusted by a factor of " + str(factor) + "\n")


def combine_tracks(bpm):
    metro = Search(str(bpm) + " bpm metronome")

    for i in metro.results:
        if i.length <= 300:
            metro_name = i.title
            metro_url = i.watch_url
            download_video(metro_url)
            break

    metro_name = re.sub('[/?*:|"<>]+', '', metro_name)
    metro_name = metro_name.replace('\\', '')
    mt = pydub.AudioSegment.from_file('./data/' + metro_name + '.wav')
    extract = mt[0:10000]

    if os.getcwd() + "./data/metronome.wav" in os.listdir(os.getcwd()):
        os.remove(os.getcwd() + "./data/metronome.wav")

    extract.export('./data/metronome.wav', format="wav")

    sound = pydub.AudioSegment.from_file("./data/metronome.wav")

    for file in os.listdir(os.getcwd() + "\\adjusted"):
        if file.endswith(".wav"):
            sound += pydub.AudioSegment.from_file("./adjusted/" + file)

    if os.getcwd() + "./combined.wav" in os.listdir(os.getcwd()):
        os.remove(os.getcwd() + "./combined.wav")

    sound.export(os.getcwd() + "./adjusted/combined.wav", format="wav")

    os.remove(os.getcwd() + "./data/" + metro_name + '.wav')
    os.remove(os.getcwd() + "./data/metronome.wav")

    print("Tracks have been combined and saved as combined.wav\n")


if __name__ == '__main__':
    if "data" not in os.listdir(os.getcwd()):
        os.mkdir(os.getcwd() + "\\data")
    if "adjusted" not in os.listdir(os.getcwd()):
        os.mkdir(os.getcwd() + "\\adjusted")

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
            name = '0'
            while name != "q":
                name = input("Enter the name of the song or press 'q' to exit: ")
                if name == "q":
                    print()
                    break

                song = Search(name)

                url = song.results[0].watch_url
                download_video(url)

        elif choice == '4':
            bpm = input("Enter the desired bpm or press 'q' to exit: ")
            if bpm == "q":
                print()
                break

            choice2 = input("Combine tracks? (y/n): ")

            for song in os.listdir(os.getcwd() + "\\data"):
                track_creation(float(bpm), song)

            if choice2 == 'y':
                print()
                combine_tracks(float(bpm))
