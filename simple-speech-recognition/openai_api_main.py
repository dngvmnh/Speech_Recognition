import requests
import openai

openai.api_key = ''

filename = "Speech_Recognition/simple-speech-recognition/Natural Language Processing Short.m4a"
name = filename.split("/")
name = name[-1]
name = name.split(".")
name = name[0]
name = name.replace(" ", "_")

def openai_transcript(filename, title) :
    audio_file= open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    if transcript:
        filename = title + '.txt'
        with open(filename, 'w') as file:
            file.write(transcript["text"])
        print('transcript saved')
    else:
        print("error")

if __name__ == "__main__" :
    openai_transcript(filename, name)
