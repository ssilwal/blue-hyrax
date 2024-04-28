import requests

def test_img():
    url = 'http://127.0.0.1:5000/img_query'
    files = {'img': open('data/img1.jpg', 'rb'), 'query':'who is she'}
    # files['audio'] = 
    r = requests.post(url, files=files)
    print(r.text)


def test_audio():
    url = 'http://127.0.0.1:5000/audio_query'
    files = {'audio': open('data/recording.webm', 'rb')}
    # files['audio'] = 
    r = requests.post(url, files=files)
    print(r.text)

def test_mm_basic():
    url = 'http://127.0.0.1:5000/mm_query'
    # files = {}
    files = {'img': open('data/screenshot.jpeg', 'rb'),
            'audio': open('data/recording.webm', 'rb')}
    r = requests.post(url, files=files)
    print(r.text)

def test_mm():
    url = 'http://127.0.0.1:5000/mm_query'
    # files = {}
    files = {'img': open('data/interview.png', 'rb'),
            'audio': open('data/recording.webm', 'rb')}
    r = requests.post(url, files=files)
    import pdb
    pdb.set_trace()
    print(r.text)

def test_pitchfork():
    url = 'http://127.0.0.1:5000/mm_query'
    # files = {}
    files = {'img': open('data/pitchfork.png', 'rb'),
            'audio': open('data/recording.webm', 'rb')}
    r = requests.post(url, data={'query':'What does that sound like?'}, files=files)
    import pdb
    pdb.set_trace()
    print(r.text)

test_pitchfork()
# test_img()
# test_audio()
# test_mm()
# curl -X POST http://localhost:5000/upload -F image=@image.jpg