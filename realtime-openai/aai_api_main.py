import pyaudio
import websockets
import asyncio
import base64
import json
import openai

API_KEY_ASSEMBLYAI = ''
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

print(p.get_default_input_device_info())

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

def ask_computer(prompt):
    # return "This is my answer"
    res = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens = 1024
    )
    return res["choices"][0]["text"]

async def send_receive():
    print(f'Connecting websocket to url ${URL}')
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", API_KEY_ASSEMBLYAI),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")
        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data":str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)
          
            return True
      
        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)
                    prompt = result['text']
                    if prompt and result['message_type'] == 'FinalTranscript':
                        print("Me:", prompt)
                        answer = ask_computer(prompt)
                        print("Chat Bot", answer)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
      
        send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())