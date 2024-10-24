import nltk
from nltk.tokenize import sent_tokenize


from transformers import RobertaTokenizer, RobertaModel
import torch
from torch.nn.functional import cosine_similarity
import os
import re
import numpy as np


tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaModel.from_pretrained('roberta-base')


query = input("Submit your query: ")

inputs = tokenizer(query, return_tensors='pt')
with torch.no_grad():
    outputs = model(**inputs)
query_embedding = outputs.last_hidden_state.mean(dim=1)




def extract_sentences_from_file(file_path):
    sentences = []

    with open(file_path, 'r') as f:
        text = f.read()  # Read the entire file content
        sentences = sent_tokenize(text)  # Tokenize the text into sentences

    return sentences

# Example usage:
file_path = "../corpus/a-midsummer-nights-dream_TXT_FolgerShakespeare.txt"  # Update the path as needed
sentences = extract_sentences_from_file(file_path)


results = []

for sentence in sentences:
    inputs = tokenizer(sentence, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    line_embedding = outputs.last_hidden_state.mean(dim=1)
    similarity = cosine_similarity(line_embedding, query_embedding)
    results.append([sentence, similarity])



results = sorted(results, key=lambda x: x[1])
for result in results:
    print(result)
