import requests
from time import sleep
import random
import csv

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5


def what_beats(word):
    sleep(random.randint(1, 3))
    return random.randint(1, 60)

def play_game(player_id):

    fieldnames = ["p1_total_cost", "p2_total_cost", "p1_word_cost", "p2_word_cost", "p1_word", "p2_word", "p1_won", "p2_won", "system_word", "round", "game_over"]

    with open("saved_data.csv", mode = "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if f.tell() == 0:
            writer.writeheader()

        for round_id in range(1, NUM_ROUNDS+1):
            round_num = -1
            while round_num != round_id:
                response = requests.get(get_url)
                print(response.json())
                sys_word = response.json()['word']
                round_num = response.json()['round']

                sleep(0.05)

            if round_id > 1:
                status = requests.get(status_url)
                rdata = status.json() 
                print("status")
                print(rdata)
                if "status" in rdata:
                    print("status is in data")
                    print(rdata['status'])
                    writer.writerow(rdata['status'])
                    f.flush()
                print(status.json())

            choosen_word = what_beats(sys_word)
            data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
            response = requests.post(post_url, json=data)
            print(response.json())

while True:
    play_game("c(a)t")