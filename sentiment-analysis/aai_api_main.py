
import requests
import json
import yt_dlp as youtube_dl
from youtube_dl.utils import DownloadError

file_path = ""

API_KEY_ASSEMBLYAI = ''
upload_endpoint = ''
transcript_endpoint = ''

headers_auth_only = {'authorization': API_KEY_ASSEMBLYAI}

headers = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

CHUNK_SIZE = 5_242_880  # 5MB

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

def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=read_file(filename))
    return upload_response.json()['upload_url']

def transcribe(audio_url, sentiment_analysis):
    transcript_request = {
        'audio_url': audio_url,
        'sentiment_analysis': sentiment_analysis
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    return transcript_response.json()['id']

def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_result_url(url, sentiment_analysis):
    transcribe_id = transcribe(url, sentiment_analysis)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
                   
def save_transcript(url, title, sentiment_analysis=False):
    data, error = get_transcription_result_url(url, sentiment_analysis)
    
    if data:
        filename = title + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
             
        if sentiment_analysis:   
            filename = title + '_sentiments.json'
            with open(filename, 'w') as f:
                sentiments = data['sentiment_analysis_results']
                json.dump(sentiments, f, indent=4)
        print('transcript saved')
        return True
    elif error:
        print("error", error)
        return False
    
def save_video_sentiments(url):
    video_info = get_video_info(url)
    url = get_audio_url(video_info)
    if url:
        title = video_info['title']
        title = title.strip(':').replace(" ", "_").replace(':','')
        save_transcript(url, title, sentiment_analysis=True)
def delete_old_transcipts() :

    Queued_list = [     '6cqwsmn0xo-0afd-4732-9828-dc3569d07bc2',
                        '6cqvsq45sj-44d3-4a6d-a8cc-6c833a258ae3', 
                        '6cqnuz5rgc-30b9-4149-9bdd-aee70aa7dd93',	
                        '6cqn3rrap1-6c4e-41df-adcd-0fbe4432a382',	
                        '6cqn62f7ce-9b77-4d98-bfb7-57c0827540e0',	
                        '6cq2vi1woy-9a28-4f12-bc88-019823363bb6',
                        '6cq9f6302t-d6a5-4307-9b0c-f3157381cc80']
    error_list = [      '6cqctyrn46-c911-4c37-8e48-c285760e4f59',	
                        '6cqcym8hn9-9139-4b24-8ad2-066df0398196',	
                        '6cqi0nr4q2-4b5c-4b62-9640-c415acae7073',	
                        '6cqix56fqu-9aa2-4e06-875d-6be0b203399f',	
                        '6cqirc1dj5-8689-4ac9-94ae-73a59003f40a',	
                        '6cqiroczv0-7ac2-4525-be12-86ab19d3c0fb']
    
    for transcript_id in error_list :
        endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

        # response = requests.post(endpoint, headers=headers, json={"queued": True})
        # print(response.json())
        # response = requests.delete(endpoint, headers=headers)
        # print(response.json())
        response = requests.get(endpoint, headers=headers)
        print(response.json())

if __name__ == "__main__":
    # delete_old_transcipts()
    save_video_sentiments("https://youtu.be/e-kSGNzu0hM")

    # with open(f"{file_path}", "r") as f:
    #     data = json.load(f)
    
    # positives = []
    # negatives = []
    # neutrals = []

    # for result in data:
    #     text = result["text"]
    #     if result["sentiment"] == "POSITIVE":
    #         positives.append(text)
    #     elif result["sentiment"] == "NEGATIVE":
    #         negatives.append(text)
    #     elif result["sentiment"] == "NEUTRAL":
    #         neutrals.append(text)
        
    # n_pos = len(positives)
    # n_neg  = len(negatives)
    # n_neut = len(neutrals)
    # r = n_pos / (n_pos + n_neg)

    # print("Num positives:", n_pos)
    # print("Num negatives:", n_neg)
    # print("Num neutrals:", n_neut)
    # print(f"Positive ratio: {r:.3f}")
    