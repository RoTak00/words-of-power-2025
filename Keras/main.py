import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical

# Load CSV
df = pd.read_csv("word_mappings2.csv")
df = df.dropna(subset=['win'])  # removes rows where 'win' is NaN
df = df[~df["response"].isin(["Entropy", "Supermassive Black Hole"])]

# Calculate true cost
df["true_cost"] = df["cost"] + 30 * (1 - df["win"])


# Load word embeddings
embeddings = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)

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
model.fit(X, y_encoded, epochs=20, batch_size=32, sample_weight=sample_weights)

# Predict
def predict_response(word):
    vec = get_vector(word)
    probs = model.predict(np.array([vec]))[0]
    response_idx = np.argmin(probs / (np.arange(len(probs)) + 1))  # optional: weighted lowest
    return label_encoder.inverse_transform([np.argmax(probs)])[0]

# Example

model.save("my_model.h5")  # Saves the full model (architecture + weights + optimizer)

while(True):

    word = input("Enter a word: ")
    response = predict_response(word)
    print(f"Predicted response: {response}")
    

