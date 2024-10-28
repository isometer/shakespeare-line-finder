import os
import pickle
from play import create_play
from sentence_transformers import SentenceTransformer

# create a deterministic list of plays

library_directory = "../corpus"

def getPlayPath(filename):
    return os.path.join(library_directory, filename)

plays = []

for filename in os.listdir(library_directory):
    if filename == "__MACOSX":
        continue
    plays.append(create_play(getPlayPath(filename)))

# each play contains a list of Acts
# each Act contains a list of Scenes
# each Scene is a list of Sentences (has 'text' property)

# we can index lines as tuples (play title, act index, scene index, sentence index)
# and in this way save embeddings as a dictionary {embedding: (exact location)} to allow retrieval.

def getSentenceFromCoordinates(play_title: str, act: int, scene: int, sentence: int):
    play = next((play for play in plays if play.title == play_title), None)

    if play:
        try:
            return play.acts[act - 1].scenes[scene - 1].sentences[sentence - 1].text
        except:
            print("ERROR: indexing")
            return ""
    else:
        print("ERROR: play found with the title {play_title}}")
        return ""


# # example: third sentence Hamlet Act III scene 2

# print(getSentenceFromCoordinates("Hamlet", 3, 2, 3))

# and in this way save embeddings as a dictionary {embedding: ((exact location), sentence text)} to allow retrieval.

embeddings_to_coordinates = {}

model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v2')

def getEmbedding(sentence: str):
    return model.encode(sentence).reshape(1, -1)

for play_index, play in enumerate(plays):
    play_title = play.title
    print(play_title, f"{int(play_index * 100.0 / len(plays))} %")
    for act_index, act in enumerate(play.acts):
        print('\t' + "Act", act_index+1)
        for scene_index, scene in enumerate(act.scenes):
            print('\t\t' + "Scene", scene_index+1)
            for sentence_index, sentence in enumerate(scene.sentences):
                embedding_hashable = getEmbedding(sentence.text).tobytes()
                location = (play_title, act_index + 1, scene_index + 1, sentence_index + 1)
                embeddings_to_coordinates[embedding_hashable] = (location, sentence.text)

with open("embeddings_saved.pkl", "wb") as file:
    pickle.dump(embeddings_to_coordinates, file)

print("SAVED EMBEDDINGS")





