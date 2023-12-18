import pyaudio
import time
import openai
import wave

seconds = 5

API_KEY_OPENAI = ''

openai.api_key = API_KEY_OPENAI

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
 
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

def ask_gpt(prompt):
    res = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens = 1024
    )
    return res["choices"][0]["text"]

def real_time_chat() :
    try :
        while True :
            frames = []

            print(f"listening for {seconds} seconds ...")

            for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
                data = stream.read(FRAMES_PER_BUFFER)
                frames.append(data)

            wf = wave.open("Speech_Recognition/basics/output.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            audio_file= open("Speech_Recognition/basics/output.wav", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            prompt = transcript["text"]

            if prompt :
                print("User : ", prompt)
                answer = ask_gpt(prompt)
                print("Chat Bot : ", answer)

            time.sleep(2)

    except KeyboardInterrupt: 
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        
      
if __name__ == "__main__" :
     real_time_chat()