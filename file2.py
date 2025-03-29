import json

with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    data = {int(k): v for k, v in data.items()}

# Example usage
print(data[1]['text'])  # if keys are integers
