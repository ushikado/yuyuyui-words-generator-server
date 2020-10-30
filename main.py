import os
import re
import json
import pickle
import markovify


def main(request):
    if request.method == "OPTIONS":
        return process_options(request)
    if request.method == "POST":
        return process_post(request)
        
    return process_default(request)


def process_options(request):
    headers = {
        'Access-Control-Allow-Origin': 'https://ushikado.github.io',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }
    return ('', 204, headers)


def process_post(request):
    headers = {
        'Content-Type':'application/json',
        'Access-Control-Allow-Origin': 'https://ushikado.github.io',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    try:
        request_dict = request.get_json(silent=True)
        character = request_dict["character"]
        assert type(character) is str
        model_path = "models/" + character + ".pkl"
        assert os.path.isfile(model_path)
    except:
        # Bad Request
        return ("", 400, headers)

    with open(model_path, 'rb') as fp:
        model = markovify.NewlineText.from_dict(pickle.load(fp))
    
    sentence = model.make_short_sentence(max_chars=120, min_words=1, tries=100)
    text = "".join(sentence.split())
     
    # make response
    response = [character, text]

    return (json.dumps(response), 200, headers)


def process_default(request):
    return


if __name__ == "__main__":
    
    class TestRequest:
        def __init__(self, character):
            self.character = character
            self.method = "POST"
        def get_json(self, silent=True):
            return {"character": self.character}

    print(main(TestRequest("結城 友奈")))
