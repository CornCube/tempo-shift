import librosa
import pydub
import os
import pyrubberband
import soundfile as sf

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
