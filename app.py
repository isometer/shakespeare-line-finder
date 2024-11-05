from flask import Flask, render_template, request
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from query_result import QueryResult

# set up the guts of the app's processing 
# (done in this file rather than an auxiliary one to keep everything in working memory.)

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


app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
  # Get the text input from the form
  user_text = request.form['user_text']
  
  # get results
  query_embedding = getEmbedding(user_text)

  similarities = cosine_similarity(query_embedding, shakespeare_embeddings)

  # Find the indices of the top 5 most similar embeddings
  top_5_indices = np.argsort(similarities[0])[-5:][::-1]  # Sort and get top 5, reversed for descending order

  top_5_sentences = [embeddings_to_sentences[embedding.tobytes()] for embedding in [shakespeare_embeddings[i].reshape(1, 768) for i in top_5_indices]]
  top_5_similarities = [similarities[0][i] for i in top_5_indices]

  query_results = [QueryResult(sentence_info, similarity) for sentence_info, similarity in zip(top_5_sentences, top_5_similarities)]
  
  # Render the result template with the user input
  return render_template('index.html', results=query_results)

if __name__ == '__main__':
  app.run(debug=True)
