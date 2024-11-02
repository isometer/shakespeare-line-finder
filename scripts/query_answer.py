import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

embeddings_to_sentences = {}

with open('embeddings_saved.pkl', 'rb') as file:
  embeddings_to_sentences = pickle.load(file)

# dict keys are made with getEmbedding(sentence.text).tobytes()

def reconstruct_embedding(bytes):
  return np.frombuffer(bytes, dtype=np.float32).reshape(1, 768) # dims of embedding

shakespeare_embeddings = np.vstack([reconstruct_embedding(bytes) for bytes in embeddings_to_sentences.keys()])

model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')

def getEmbedding(sentence: str):
  return model.encode(sentence).reshape(1, -1)

def display_sentence_info(sentence_info, similarity_score):
  coordinates = sentence_info[0]
  sentence = sentence_info[1]
  play, act, scene, sentence_index = coordinates
  print(f"{play} -- Act {act}, Scene {scene}, sentence {sentence_index}")
  print(f'"{sentence}"')
  print(f"(Match {similarity_score * 100:.1f}%)")
  print("----------------------")
  
while(True):
  
  query = input("What sentence would you like to find? (or 'quit' to end)  ")

  if(query == "quit"):
    break

  query_embedding = getEmbedding(query)

  similarities = cosine_similarity(query_embedding, shakespeare_embeddings)

  # Find the indices of the top 5 most similar embeddings
  top_5_indices = np.argsort(similarities[0])[-5:][::-1]  # Sort and get top 5, reversed for descending order

  top_5_sentences = [embeddings_to_sentences[embedding.tobytes()] for embedding in [shakespeare_embeddings[i].reshape(1, 768) for i in top_5_indices]]
  top_5_similarities = [similarities[0][i] for i in top_5_indices]

  # Print the top 5 matches
  for idx, (sentence_info, similarity) in enumerate(zip(top_5_sentences, top_5_similarities), 1):
    display_sentence_info(sentence_info, similarity)

