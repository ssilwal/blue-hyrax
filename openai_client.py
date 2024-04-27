from openai import OpenAI
import os
import base64
import requests
import werkzeug 

class OpenAIClient:
    def __init__(self):
        self.api_key = os.environ["OPENAI_API_KEY"]
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
                "content": "You are a proficient AI with a specialty in distilling information into 1 key idea. Your goal is to provide a concise sentence that someone could read to quickly understand what was talked about. If the content contains instructions, propose a solution or a code snippet in python that can solve the problem."
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
        print(f"Received query: {payload['messages']}")#[0]['content'][0]['text']}")

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
        return response.json()

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

