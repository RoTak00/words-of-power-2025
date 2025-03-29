
import json 
import requests 
import random

def Lowest_Cost(word, labeled_words, history):
    return labeled_words[0]

def Highest_Cost(word, labeled_words, history):
    return labeled_words[-1]

def Adaptive(word, labeled_words, history):
    if len(history) == 0:
        base_idx = len(labeled_words) // 2
        offset = random.randint(-4, 4)
        return labeled_words[max(0, min(len(labeled_words) - 1, base_idx + offset))]

    last_success = history[-1]['success']
    prev_success = history[-2]['success'] if len(history) > 1 else None

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


NO_ROUNDS = 5

words = [
    "Candle", "Hammer", "Lion", "Flood", "Tank", "Pandemic", "Mirror", "Compass", "Crown", "Comet",
    "Lantern", "Bridge", "Clock", "Helmet", "Statue", "Jungle", "Thunderstorm", "Machine", "Book", "Ash",
    "Firefly", "Vortex", "Prism", "Lantern", "Planet", "Serpent", "Cave", "Helmet", "Robot", "Galaxy",
    "Meteor", "Storm", "Mountain", "River", "Temple", "Forest", "Dragon", "Castle", "Knight", "Spear",
    "Ghost", "Phoenix", "Beacon", "Canyon", "Sand", "Smoke", "Fog", "Torch", "Crystal", "Bell",
    "Spaceship", "Starship", "Blaster", "Teleport", "Clone", "Cybernetic", "Nanobot", "Neural Net",
    "AI", "Drone", "Hologram", "Android", "Singularity", "Quantum Core", "Fusion Reactor", "Wormhole",
    "Dark Matter", "Event Horizon", "Void", "Nebula", "Plasma", "Laser", "Cryostasis", "Mech", "Orbital",
    "Antigrav", "Starbase", "Space Station", "Exosuit", "Warp Drive", "Gravity Well", "Moonbase",
    "Time Rift", "Alien", "Mutant", "Probe", "Synthetics", "Hyperdrive", "Power Core", "Command Deck",
    "Control Panel", "Energy Cell", "Neutrino", "Asteroid", "Colony", "Terraformer",
    "Chimera", "Golem", "Witch", "Wizard", "Rune", "Scroll", "Spell", "Cauldron", "Portal", "Griffin",
    "Pegasus", "Hydra", "Titan", "Oracle", "Seer", "Throne", "Obelisk", "Sanctum", "Relic", "Amulet",
    "Wand", "Staff", "Elixir", "Talisman", "Fountain", "Shrine", "Celestial", "Constellation",
    "Starlight", "Astral Gate", "Eclipse", "Solar Flare", "Lighthouse", "Chronosphere", "Soulstone",
    "Dreamscape", "Eternium", "Void Crystal", "Mana Core", "Time Crystal", "Mind Gate", "Cosmic Seed"
]

words = random.sample(words, 5)

total_cost = 0

history = []

Chosen_Strategy = Adaptive

for i in range(NO_ROUNDS):
    print(f"Round {i + 1} of {NO_ROUNDS}")

    print(f"Word: {words[i]}")

    id, word = Chosen_Strategy(words[i], labeled_words, history)

    text = word['text']
    cost = int(word['cost'])

    print(word['text'])
    wins = int(input("1/0 w/l"))

    if(wins == 1):
        new_cost = cost
        total_cost += new_cost
    else: 
        new_cost = cost + 30
        total_cost += new_cost

    history.append({"word": words[i], "success": wins, "cost": new_cost, "choice": id})

print(total_cost)

    