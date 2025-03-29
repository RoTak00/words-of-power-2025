import requests
from time import sleep
import random
import json

is_p1 = True

def Adaptive(word, labeled_words, history):

    global is_p1

    if len(history) == 0:
        base_idx = len(labeled_words) // 2
        offset = random.randint(-4, 4)
        return labeled_words[max(0, min(len(labeled_words) - 1, base_idx + offset))]

    success_label = 'p1_won' if is_p1 else 'p2_won'
    last_success = history[-1][success_label]
    prev_success = history[-2][success_label] if len(history) > 1 else None

    if prev_success is not None and last_success != prev_success:
        base_idx = len(labeled_words) // 2
    elif last_success == 1:
        labeled_words = labeled_words[:len(labeled_words) // 2]
        base_idx = len(labeled_words) // 2
    else:
        labeled_words = labeled_words[len(labeled_words) // 2 + 1:]
        base_idx = len(labeled_words) // 2

    if not labeled_words:
        return None

    offset = random.randint(-4, 4)
    return labeled_words[max(0, min(len(labeled_words) - 1, base_idx + offset))]


with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    labeled_words = {int(k): v for k, v in data.items()}

#sort labeled words by cost 
labeled_words = sorted(labeled_words.items(), key=lambda x: x[1]['cost'])


host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5


def what_beats(word):
    sleep(random.randint(1, 3))
    return random.randint(1, 60)


history = []

Chosen_Strategy = Adaptive

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

        id, word = Chosen_Strategy(sys_word, labeled_words, history)
        data = {"player_id": player_id, "word_id": id, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())

play_game("c(a)t")