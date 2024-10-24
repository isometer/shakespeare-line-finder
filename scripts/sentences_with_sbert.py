from sentence_transformers import SentenceTransformer
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')

def get_embeddings(sentences: str | list[str]):
    return model.encode(sentences)

query = input("Submit your query: ")

query_embedding = get_embeddings(query)


def extract_sentences_from_file(file_path):
    sentences = []

    with open(file_path, 'r') as f:
        text = f.read()  # Read the entire file content
        sentences = sent_tokenize(text)  # Tokenize the text into sentences

    return sentences

# Example usage:
file_path = "../corpus/a-midsummer-nights-dream_TXT_FolgerShakespeare.txt"  # Update the path as needed
sentences = extract_sentences_from_file(file_path)

sentence_embeddings = np.array([embedding.flatten() for embedding in get_embeddings(sentences)]) 

similarities = cosine_similarity(query_embedding.reshape(1, -1), sentence_embeddings)

# Find the indices of the top 5 most similar embeddings
top_5_indices = np.argsort(similarities[0])[-5:][::-1]  # Sort and get top 5, reversed for descending order

# Retrieve the corresponding sentences and similarities
top_5_sentences = [sentences[i] for i in top_5_indices]
top_5_similarities = [similarities[0][i] for i in top_5_indices]

# Print the top 5 matches
for idx, (sentence, similarity) in enumerate(zip(top_5_sentences, top_5_similarities), 1):
    print(f"{idx}. '{sentence}' with similarity: {similarity}")