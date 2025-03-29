import requests
import csv
import random
import json

SEEN_FILE = "seen_words.json"

# Load seen words
try:
    with open(SEEN_FILE, "r") as f:
        seen_words = set(json.load(f))
except FileNotFoundError:
    seen_words = set()

with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    labeled_words = {int(k): v for k, v in data.items()}

words = [
    "Candle", "Hammer", "Lion", "Flood", "Tank", "Pandemic", "Mirror", "Compass", "Crown", "Comet",
    "Lantern", "Bridge", "Clock", "Helmet", "Statue", "Jungle", "Thunderstorm", "Machine", "Book", "Ash",
    "Firefly", "Vortex", "Prism", "Lantern", "Planet", "Serpent", "Cave", "Helmet", "Robot", "Galaxy",
    "Meteor", "Storm", "Mountain", "River", "Temple", "Forest", "Dragon", "Castle", "Knight", "Spear",
    "Ghost", "Phoenix", "Beacon", "Canyon", "Sand", "Smoke", "Fog", "Torch", "Crystal", "Bell",
    "Cup", "Chalk", "Dust", "Broom", "Glove"
]

# Open CSV for writing
with open("word_mappings.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "response", "cost", "win"])
    
    for word in words:
        assigned = random.sample(list(labeled_words.items()), 3)
        for idx, elem in assigned:
            writer.writerow([word.title(), elem['text'], elem['cost'], ""])
