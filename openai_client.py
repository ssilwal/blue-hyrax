from openai import OpenAI
import os
import base64
import requests
import werkzeug 
import json
from io import StringIO
import contextlib
import sys

class SpotifyAgent:
    def __init__(self):
        self.api_key = os.environ["SPOTIFY_API"]

    def play_song(self, artist_name, album_name,song_name=None):
        search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(search_url, headers=headers)
        artists = json.loads(response.text)
        # print()


        for a in artists['artists']['items']:
            if a['name'] == artist_name:
                artist_id = a['id']
        artist_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        response = requests.get(artist_url, headers=headers)
        artist_albums = json.loads(response.text)

        track_id = None
        for album in artist_albums['items']:
            if track_id is not None:
                break
            if album['name'] == album_name:
                album_id = album['id']
                album_tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
                response = requests.get(album_tracks_url, headers=headers)
                tracks = response.json()['items']
                if song_name ==None:
                    track_id = tracks[0]['id'] #hard-coded to first song not song name
                else:
                    for track in tracks:
                        if track['name'].lower() == song_name.lower():
                            track_id = track['id']
                            break
        if track_id:
            play_url = "https://api.spotify.com/v1/me/player/play"
            payload = {"uris": [f"spotify:track:{track_id}"]}
            response = requests.put(play_url, headers=headers, json=payload)
            if response.status_code == 204:
                print(f"Playing '{song_name}' by {artist_name}")
                return(f"Playing '{song_name}' by {artist_name}")
            else:
                print(response)
                print(response.status_code)
                print(response.json())
                return response.text
        else:
            print(f"Could not find '{song_name}' by {artist_name}")
            return(f"Could not find '{song_name}' by {artist_name}")
        print('failed')
        return "Failed"

class OpenAIClient:
    def __init__(self):
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.actions = {}
        self.spotify_agent = SpotifyAgent()
        self.client = OpenAI()


    # Function to encode the image
    def encode_image(self, img_file_storage):
        if isinstance(img_file_storage,str):
          with open(img_file_storage, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        elif isinstance(img_file_storage,werkzeug.datastructures.FileStorage):
            return base64.b64encode(img_file_storage.read()).decode('utf-8')

    ''' Accepts audio file and returns string.'''
    def process_audio(self,audio_file):
        audio_filepath = 'uploads/' + audio_file.filename
        audio_file.save(audio_filepath)
        return audio_filepath


    def query_img(self, img, text):
        # Getting the base64 string
        base64_image = self.encode_image(img)

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {self.api_key}"
        }

        
        payload = {
          "model": "gpt-4-vision-preview",
          # "model": "gpt-4-0613",
          # "model": "gpt-3.5-turbo",
          "messages": [
            {
                "role": "system",
                "content": "You are a proficient AI with a specialty in distilling information into 1 key idea. Your goal is to be as concise and specific as possible and give 1 sentence that someone could read quickly. If the content contains instructions, propose a solution or a code snippet in python that can solve the problem."
            },
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": text
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        #TODO CHECK IF YOU NEED TO DO AN ACTION
        follow_up_payload = {
          "model": "gpt-4-vision-preview",
          # "model": "gpt-4-0613",
          # "model": "gpt-3.5-turbo",
          "messages": [
            {
                "role": "system",
                "content": "Answer in 1 word, does this have to do with music?"
            },
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "Does this have to do with music?"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }
        follow_up_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=follow_up_payload)
        print(f"Follow up response: {follow_up_response.json()['choices'][0]['message']['content'].lower()}")
        # print(follow_up_response.json()['choices'][0]['message']['content'].lower())
        if 'yes' in follow_up_response.json()['choices'][0]['message']['content'].lower():
            print(self.get_spotify_agent(img,"Who is the artist and album? Help me call self.spotify_agent()"))
        else:
            print('Not related to music')
        return response.json()

    def get_spotify_agent(self,img,text):
        # Getting the base64 string
        base64_image = self.encode_image(img)

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {self.api_key}"
        }

        
        payload = {
          "model": "gpt-4-vision-preview",
          # "model": "gpt-4-0613",
          # "model": "gpt-3.5-turbo",
          "messages": [
            {
                "role": "system",
                "content": "You are a proficient AI helping the user make calls to play a specific song. \n Please respond in 1 line with the artist and allbum in the picture and use quotes for them and format your response like this: \n self.spotify_agent.play_song(artist_name, album_name)"
            },
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": text
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_text = response.json()['choices'][0]['message']['content']
        # response_text= "self.spotify_agent.play_song(\"Iron & Wine\", \"Light Verse\")"
        print(f"gpt_response to execute: {response_text}")

        @contextlib.contextmanager
        def stdoutIO(stdout=None):
            old = sys.stdout
            if stdout is None:
                stdout = StringIO()
            sys.stdout = stdout
            yield stdout
            sys.stdout = old

       
        with stdoutIO() as s:
            exec(response_text)
        # exec(response_text)
        output = s.getvalue()
        print(output)
        return output


    def speech_to_text(self,audio_file):
        # audio_file= open("sample.webm", "rb")
        audio = self.process_audio(audio_file)
        transcription = self.client.audio.transcriptions.create(
          model="whisper-1", 
          file=open(audio,'rb')
        )
        response = transcription.text
        # response = "What am I looking at?"
        print(f"client.speech_to_text:: {response}")
        return response

