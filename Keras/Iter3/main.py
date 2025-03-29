import pandas as pd
import numpy as np
import csv
from gensim.models import KeyedVectors
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical
import json

with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    labeled_words = {int(k): v for k, v in data.items()}

print(labeled_words)

# Load CSV
df = pd.read_csv("../word_mappings5.csv")
df = df.dropna(subset=['win'])  # removes rows where 'win' is NaN
df = df[~df["response"].isin(["Entropy", "Supermassive Black Hole"])]

# Calculate true cost
df["true_cost"] = df["cost"] + 30 * (1 - df["win"])


# Load word embeddings
embeddings = KeyedVectors.load_word2vec_format("../GoogleNews-vectors-negative300-SLIM.bin", binary=True)

# Helper to get embedding vector
def get_vector(word):
    try:
        return embeddings[word]
    except KeyError:
        return np.zeros(300)

# Encode input and response
X = np.stack(df["word"].apply(get_vector))
label_encoder = LabelEncoder()
y_labels = label_encoder.fit_transform(df["response"])
y_encoded = to_categorical(y_labels)

# Sample weights based on cost
sample_weights = 1 / df["true_cost"].values

# Build model
model = Sequential([
    Input(shape=(300,)),
    Dense(128, activation="relu"),
    Dense(len(label_encoder.classes_), activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train
model.fit(X, y_encoded, epochs=60, batch_size=32, sample_weight=sample_weights)

# Predict
history = []
# Predict
def predict_response(input_word, labeled_words, model):
    global history
    vec = get_vector(input_word)
    probs = model.predict(np.array([vec]))[0]
    predicted_text = label_encoder.inverse_transform([np.argmax(probs)])[0]
    
    
    recent_texts = set(h['text'] for h in history[-5:])

    sorted_indices = np.argsort(probs)
    for idx in sorted_indices:
        predicted_text = label_encoder.inverse_transform([idx])[0]
        if predicted_text not in recent_texts:
            for entry in labeled_words:
                if labeled_words[entry]['text'] == predicted_text:
                    selected = labeled_words[entry]
                    history.append(selected)  # update history here
                    return selected
    return None


# Example

model.save("my_model2.keras")  # Saves the full model (architecture + weights + optimizer)

while(True):

    word = input("Enter a word: ")
    response = predict_response(word, labeled_words, model)
    print(f"Predicted response: {response}")

    if(response == None):
        continue
    
    success = input("Was the response correct? (1/0): ")
    with open('../word_mappings5.csv', mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([word, response['text'], response['cost'], success])

        #find the cost of the word inserted if it exists
        cost = None 
        for entry in labeled_words:
            if labeled_words[entry]['text'] == word:
                cost = labeled_words[entry]['cost']
                break
        if cost is not None:
            writer.writerow([response['text'], word, cost, 1 - int(success)])
        f.flush()



