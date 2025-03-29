import requests
from time import sleep
import random
import json
import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all logs, 1 = filter INFO, 2 = filter WARNING, 3 = filter ERROR
os.environ['CUDA_VISIBLE_DEVICES'] = ''            # Disable GPU
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'           # Disable OneDNN custom ops

# Load word embeddings
embeddings = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300-SLIM.bin", binary=True)

# Helper to get embedding vector
def get_vector(word):
    try:
        return embeddings[word]
    except KeyError:
        return np.zeros(300)
    
    # Load CSV
df = pd.read_csv("word_mappings4.csv")

# Encode input and response
X = np.stack(df["word"].apply(get_vector))
label_encoder = LabelEncoder()
y_labels = label_encoder.fit_transform(df["response"])
y_encoded = to_categorical(y_labels)

with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    labeled_words = {int(k): v for k, v in data.items()}

model = load_model('my_model.keras')


history = []
# Predict
def predict_response(input_word, labeled_words, model):
    global history
    vec = get_vector(input_word)
    probs = model.predict(np.array([vec]))[0]
    predicted_text = label_encoder.inverse_transform([np.argmax(probs)])[0]

    sorted_indices = np.argsort(probs)
    for idx in sorted_indices:
        predicted_text = label_encoder.inverse_transform([idx])[0]
        for entry in labeled_words:
            if labeled_words[entry]['text'] == predicted_text:
                selected = labeled_words[entry]
                history.append(selected)  # update history here
                return selected
    return None

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5


def play_game(player_id):

    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']

            sleep(0.5)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

            history.append(status.json()['status'])

        word = predict_response(sys_word, labeled_words, model)
        
        print(word)

        # go thourgh labeled words and find word
        idx = None
        for entry in labeled_words:
            if labeled_words[entry]['text'] == word['text']:
                idx = entry
                break

        data = {"player_id": player_id, "word_id": idx, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())

play_game("c(a)t")



