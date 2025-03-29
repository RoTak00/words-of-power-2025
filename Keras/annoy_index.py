from gensim.models import KeyedVectors
from annoy import AnnoyIndex
import pickle

# Load full model once
word_vectors = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin", binary=True)

# Dimensions of the embeddings
dim = word_vectors.vector_size
index = AnnoyIndex(dim, 'angular')

# Optional: filter to only the 60 game words
target_words = list(word_vectors.index_to_key)  # or use your filtered list

# Add items
word_to_index = {}
for i, word in enumerate(target_words):
    if word in word_vectors:
        index.add_item(i, word_vectors[word])
        word_to_index[word] = i

# Build and save index
index.build(10)
index.save("wordvectors.ann")

# Save the word <-> index mapping
with open("word_to_index.pkl", "wb") as f:
    pickle.dump(word_to_index, f)
