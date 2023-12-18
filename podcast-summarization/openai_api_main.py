import streamlit as st
import glob
import json
import requests
import json
import pprint
import io
import openai

st.title("Podcast Summaries")

json_files = glob.glob('*.json')

episode_id = st.sidebar.text_input("Episode ID")

API_KEY_LISTENNOTES = ''

listennotes_episode_endpoint = ''

headers_listennotes = {
  'X-ListenAPI-Key': API_KEY_LISTENNOTES,
}

def get_episode_audio_url(episode_id):
    url = listennotes_episode_endpoint + '/' + episode_id
    response = requests.request('GET', url, headers=headers_listennotes)

    data = response.json()
    pprint.pprint(data)

    episode_title = data['title']
    thumbnail = data['thumbnail']
    podcast_title = data['podcast']['title']
    audio_url = data['audio']
    return audio_url, thumbnail, podcast_title, episode_title

def save_transcript(episode_id):
    audio_url, thumbnail, podcast_title, episode_title = get_episode_audio_url(episode_id)
    response = requests.get(audio_url)
    audio_file = io.BytesIO(response.content)
    transcript = openai.Audio.transcribe("whisper-1", audio_file) 
    if transcript:
        filename = episode_id + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])

        filename = episode_id + '_chapters.json'
        with open(filename, 'w') as f:
            chapters = data['chapters']

            data = {'chapters': chapters}
            data['audio_url']=audio_url
            data['thumbnail']=thumbnail
            data['podcast_title']=podcast_title
            data['episode_title']=episode_title
            # for key, value in kwargs.items():
            #     data[key] = value

            json.dump(data, f, indent=4)
            print('transcript saved')
            return True
    else :
        print("error")
        return False
    
def get_clean_time(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
        
    return start_t

if __name__ == "__main__" :

    button = st.sidebar.button("Download Episode summary", on_click=save_transcript, args=(episode_id,))

    if button:
        filename = episode_id + '_chapters.json'
        print(filename)
        with open(filename, 'r') as f:
            data = json.load(f)

        chapters = data['chapters']
        episode_title = data['episode_title']
        thumbnail = data['thumbnail']
        podcast_title = data['podcast_title']
        audio = data['audio_url']

        st.header(f"{podcast_title} - {episode_title}")
        st.image(thumbnail, width=200)
        st.markdown(f'#### {episode_title}')

        for chp in chapters:
            with st.expander(chp['gist'] + ' - ' + get_clean_time(chp['start'])):
                chp['summary']