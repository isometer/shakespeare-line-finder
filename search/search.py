from flask import Blueprint, render_template, session, redirect, url_for, request
from query_result import QueryResult
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import numpy as np
import random


search_bp = Blueprint('search_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets')



embeddings_to_sentences = {}
titles = []
yellowtexts = [
  {'line':"What is 't you seek?", 'title':"King Lear", "act":3, "scene":4, "line_no":111},
  {'line':"Search, seek, find out.", 'title':"The Merry Wives of Windsor", "act":3, "scene":3, "line_no":157},
  {'line':"What you would work me to, I have some aim.", 'title':"Julius Caesar", "act":1, "scene":2, "line_no":106},
  {'line':"Go and search.", 'title':"Cymbeline", "act":2, "scene":3, "line_no":117},
  {'line':"Once more search with me", 'title':"The Merry Wives of Windsor", "act":4, "scene":2, "line_no":148},
  {'line':"Look, and thou shalt see.", 'title':"Romeo and Juliet", "act":5, "scene":3, "line_no":196},
  {'line':"What are you then determined to do?", 'title':"Julius Caesar", "act":5, "scene":1, "line_no":79}
]
colors = ["rgba(226, 226, 226, 0.5);", "rgba(255, 250, 241, 0.5);"]


with open('titles_saved.pkl', 'rb') as file:
  titles = (pickle.load(file))


with open('embeddings_saved.pkl', 'rb') as file:
  embeddings_to_sentences = pickle.load(file)

# dict keys are made with getEmbedding(sentence.text).tobytes()
def reconstruct_embedding(bytes):
  return np.frombuffer(bytes, dtype=np.float32).reshape(1, 768) # dims of embedding

shakespeare_embeddings = np.vstack([reconstruct_embedding(bytes) for bytes in embeddings_to_sentences.keys()])
model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')

def getEmbedding(sentence: str):
  return model.encode(sentence).reshape(1, -1)


@search_bp.route("/")
def start():
  return render_template("search.html", titles=titles, yellowtext = yellowtexts[random.randint(0, 100) % len(yellowtexts)])

@search_bp.route('/submit', methods=['POST'])
def submit():
  
  # Get the text input from the form
  user_text = request.form['user_text']
  play_filter = request.form['play_filter']
  act_filter = request.form['act_filter']
  scene_filter = request.form['scene_filter']

  
  # get results
  query_embedding = getEmbedding(user_text)

  filtered_embeddings = []
  # Filter embeddings by play, act, and/or scene
  for embedding_bytes, sentence_text in embeddings_to_sentences.items():
      play, act, scene, line = sentence_text[0]
      if act_filter and (str(act) != act_filter) or \
        scene_filter and (str(scene) != scene_filter) or \
        play_filter != "All" and (play != play_filter):
          continue
      filtered_embeddings.append(reconstruct_embedding(embedding_bytes))
  filtered_embeddings = np.vstack(filtered_embeddings)

  final_embeddings = shakespeare_embeddings
  if act_filter or scene_filter or (play_filter != "All"):
    final_embeddings = filtered_embeddings
  
  
  similarities = cosine_similarity(query_embedding, final_embeddings)


  # Find the indices of the top 5 most similar embeddings
  top_5_indices = np.argsort(similarities[0])[-20:][::-1]  # Sort and get top 20, reversed for descending order
  top_5_sentences = [embeddings_to_sentences[embedding.tobytes()] for embedding in [final_embeddings[i].reshape(1, 768) for i in top_5_indices]]
  top_5_similarities = [similarities[0][i] for i in top_5_indices]
      
  query_results = [QueryResult(sentence_info, similarity) for sentence_info, similarity in zip(top_5_sentences, top_5_similarities)]

  # Render the result template with the user input
  return render_template('search.html', results=query_results, query=user_text, titles=titles, yellowtext = yellowtexts[random.randint(0, 100) % len(yellowtexts)], colors=colors)


def handle_post_request():
  print("HEYYYYYYYYYYYYYYYYYYY")
