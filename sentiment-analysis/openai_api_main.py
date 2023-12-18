import json
import yt_dlp as youtube_dl
from youtube_dl.utils import DownloadError
import openai
import requests
import io

openai.api_key = ''

url = ""
file_path = ""

ydl = youtube_dl.YoutubeDL()

def get_video_info(url):
    with ydl:
        try:
            result = ydl.extract_info(
                url,
                download=False
            )
        except DownloadError:
            return None

    if result :
        video = result
    if "entries" in result :
        video = result["entries"][0]
    return video

def get_audio_url(video):
    for f in video['formats']:
        if f['ext'] == 'm4a':
            return f['url']
                   
def save_transcript(url, title, sentiment_analysis=False):
    response = requests.get(url)
    audio_file = io.BytesIO(response.content)
    transcript = openai.Audio.transcribe("whisper-1", audio_file)    
    if transcript:
        filename = title + '.txt'
        with open(filename, 'w') as f:
            f.write(transcript["text"])
             
        if sentiment_analysis:   
            rates = transcript["text"].split(".")
            json_sentiments = {}
            for rate in rates :
                if rate not in json_sentiments.key() :
                    json_sentiments[f"{rate}"] = ""                

            for rate in rates :
                response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"{rate}. What is the sentiment, answer using only possitive, neutral, negative ?",
                temperature=0.5,
                max_tokens=8
                )
                result = response.choices[0].text.strip(".").upper()
                json_sentiments[f"{rate}"] = result.strip("\n\n")

            json_sentiments = json_sentiments = json.dumps(json_sentiments)
            filename = title + "_sentiment.json"

            with open(filename, 'w') as f :
                f.write(json_sentiments)
            
            positives = []
            negatives = []
            neutrals  = []

            for rate in rates:
                TEXT = json_sentiments[f"{rate}"]
                if json_sentiments[f"{rate}"] == "POSITIVE":
                    positives.append(TEXT)
                elif json_sentiments[f"{rate}"] == "NEGATIVE":
                    negatives.append(TEXT)
                elif json_sentiments[f"{rate}"] == "NEUTRAL":
                    neutrals.append(TEXT)
                
            n_pos = len(positives)
            n_neg  = len(negatives)
            n_neut = len(neutrals)
            r = n_pos / (n_pos + n_neg + n_neut)

            print("Num positives:", n_pos)
            print("Num negatives:", n_neg)
            print("Num neutrals:", n_neut)
            print(f"Positive ratio: {r:.3f}")
            

        print('transcript saved')
        return True
    else :
        print("error")
        return False
    
def save_video_sentiments(url, video_info):
    title = video_info['title']
    name = title.split("/")
    name = name[-1]
    name = name.split(".")
    name = name[0]
    name = name.replace(" ", "_")
    title = name.strip(':').replace(" ", "_").replace(':','')
    save_transcript(url, title, sentiment_analysis=True)

if __name__ == "__main__":
    video_info = get_video_info(url)
    url = get_audio_url(video_info)
    save_video_sentiments(url, video_info)