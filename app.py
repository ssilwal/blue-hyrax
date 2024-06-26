from flask import Flask, request
from flask_cors import CORS  # Import CORS

from openai import OpenAI
import openai_client
import os
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and methods
agent = openai_client.OpenAIClient()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/imgquery", methods=["POST"])
def img_query():
    img_file = request.files['img']
    img_filename = str(uuid.uuid4())+ request.files['img'].filename # Generate UUID for image filename
    img_filepath = os.path.join('uploads', img_filename)
    img_file.save(img_filepath)

    user_msg = request.files['query']
    response = agent.query_img(img_filepath, "what is in the image?")
    return response

@app.route("/audio_query", methods=["POST"])
def audio_query():
    audio_file = request.files['audio']
    return agent.speech_to_text(audio_file)
	
@app.route("/mm_query", methods=["POST"])
def multimodal_query():
    audio_file = request.files['audio']
    img_file = request.files['img']
    img_filepath = 'uploads/' + str(uuid.uuid4()) + img_file.filename
    img_file.save(img_filepath)

    transcribed_speech = agent.speech_to_text(audio_file)
    response = agent.query_img(img_filepath, transcribed_speech)
    return response['choices'][0]['message']['content']

@app.route("/test_spotify", methods=["POST"])
def test_spotify():
    audio_file = request.files['audio']
    img_file = request.files['img']
    img_filepath = 'uploads/' + str(uuid.uuid4()) + img_file.filename
    img_file.save(img_filepath)

    # transcribed_speech = agent.speech_to_text(audio_file)
    transcribed_speech = "Can you play that song?"
    response = agent.get_spotify_agent(img_filepath, transcribed_speech)
    return response


if __name__ == '__main__':
    app.run()
