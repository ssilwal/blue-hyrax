from flask import Flask, request, current_app
from requests.models import Response

from openai import OpenAI
import openai_client
import os


app = Flask(__name__)
agent = openai_client.OpenAIClient()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/imgquery", methods=["POST"])
def img_query():
    img_file = request.files['img']
    img_filepath = 'uploads/' + img_file.filename
    img_file.save(img_filepath)


    user_msg = request.files['query']
    response = agent.query_img(img_filepath,"what is in the image?")

    return response

@app.route("/audio_query", methods=["POST"])
def audio_query():
    audio_file = request.files['audio']
    return agent.speech_to_text(audio_file)
	
@app.route("/mm_query", methods=["POST"])
def multimodal_query():
    audio_file = request.files['audio']

    img_file = request.files['img']
    img_filepath = 'uploads/' + img_file.filename
    img_file.save(img_filepath)


    transcribed_speech = agent.speech_to_text(audio_file)
    response = agent.query_img(img_filepath, transcribed_speech)
    print(response)
    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()