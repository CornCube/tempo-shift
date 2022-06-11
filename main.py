# file libraries
from pytube import YouTube, Playlist, Search
from tqdm import tqdm

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

    tempo = input("Enter the bpm of " + filename + " or press 'n' to accept an average: ")
    if tempo == "n":
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
    print("Track has been adjusted by a factor of " + str(factor))

    if choice3 == "n":
        x = input("Add metronome throughout the song to stay on beat? (y/n): ")
        if x == "y":
            os.chdir("./adjusted")
            y, sr = librosa.load(filename)
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = librosa.frames_to_time(beats, sr=sr)
            if "metronome.wav" in os.listdir(os.getcwd()):
                os.remove("metronome.wav")
            sf.write('metronome.wav', librosa.clicks(times=beat_times, sr=sr), sr, format='wav')

            sound1 = pydub.AudioSegment.from_file(filename)
            sound2 = pydub.AudioSegment.from_file("metronome.wav")

            with_metronome = sound1.overlay(sound2)

            if filename in os.listdir(os.getcwd()):
                os.remove(filename)
            with_metronome.export(filename, format="wav")

            os.remove("metronome.wav")

            print("Track has been created with metronome overlay")

            os.chdir('..')

        else:
            print("Track has been created without metronome overlay")

    else:
        print("Track has been created without metronome overlay")


def combine_tracks(bpm):
    os.chdir('./adjusted')

    if "combined.wav" in os.listdir(os.getcwd()):
        os.remove(os.getcwd() + "\\combined.wav")

    sound = pydub.AudioSegment.from_file(os.listdir(os.getcwd())[0])

    for file in os.listdir(os.getcwd())[1:]:
        if file.endswith(".wav"):
            sound += pydub.AudioSegment.from_file(file)

    sound.export("combined.wav", format="wav")

    if choice3 == "y":
        y, sr = librosa.load('combined.wav')
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        sf.write('metronome.wav', librosa.clicks(times=beat_times, sr=sr), sr, format='wav')

        sound1 = pydub.AudioSegment.from_file("combined.wav")
        sound2 = pydub.AudioSegment.from_file("metronome.wav")

        with_metronome = sound1.overlay(sound2)

        os.remove("combined.wav")
        os.remove("metronome.wav")
        with_metronome.export("combined.wav", format="wav")

        os.chdir('..')

    print("Tracks have been combined and saved as 'combined.wav'\n")


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
            choice3 = 'n'

            if choice2 == 'y':
                choice3 = input("Add metronome to entire track? (y/n): ")

            for song in tqdm(os.listdir(os.getcwd() + "\\data")):
                track_creation(float(bpm), song)

            if choice2 == 'y':
                print()
                combine_tracks(float(bpm))
