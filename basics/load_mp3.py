from pydub import AudioSegment
import pydub
import os
# print(os.path.exists("C:/Users/dngvm/AppData/Local/ffmpegio/ffmpeg-downloader/ffmpeg/bin/ffmpeg.exe"))
pydub.AudioSegment.converter = "C:/Users/dngvm/AppData/Local/ffmpegio/ffmpeg-downloader/ffmpeg/bin/ffmpeg.exe"

audio = AudioSegment.from_wav("Speech_Recognition/basics/output.wav")
# audio = AudioSegment.from_mp3("")

audio = audio + 20

audio = audio * 2

audio = audio.fade_in(2000)

audio.export("Speech_Recognition/basics/mashup.mp3", format="mp3")