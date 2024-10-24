"""

This script runs through the text files of the works and for each work generates
a text file of formmat line_no, embedding


"""

from transformers import RobertaTokenizer, RobertaModel
import torch
from torch.nn.functional import cosine_similarity
import os
import re
import numpy as np


tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaModel.from_pretrained('roberta-base')

directory = "../corpus";


for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as infile:
            line =  infile.readline().strip().lower()
            line =  re.sub(r'[^a-zA-Z ]', '', line)
            title = line.replace(" ", "_") 

        output_filename = f"../data/{title}.txt"
        with open(output_filename, 'w') as outfile:
            with open(file_path, 'r') as infile:  
                act, line_no = 0, 0
                for line in infile:
                    line_no += 1
                    stripped_line = re.sub(r'[^a-zA-Z ]', '', line.strip())
                    line = re.sub(r'[^a-zA-Z \[\]=]', '', line.strip())
                    
                    if act > 0:
                        inputs = tokenizer(stripped_line, return_tensors='pt')
                        with torch.no_grad():
                            outputs = model(**inputs)
                        embedding = outputs.last_hidden_state.mean(dim=1)
                        array = embedding.numpy()
                        formatted_embedding = ' '.join(map(str, array.flatten()))
                        outfile.write(str(line_no) + ", " + formatted_embedding + "\n")

                    match line:
                        case "=====":
                            act += 1

                    
       
    
    break          
   
    











""""




# Theme embedding (for "love")
love_text = "love"
love_inputs = tokenizer(love_text, return_tensors='pt')
with torch.no_grad():
    love_outputs = model(**love_inputs)
love_embedding = love_outputs.last_hidden_state.mean(dim=1)



# Theme embedding (for "suicide")
theme_text = "suicide"
theme_inputs = tokenizer(theme_text, return_tensors='pt')
with torch.no_grad():
    theme_outputs = model(**theme_inputs)
theme_embedding = theme_outputs.last_hidden_state.mean(dim=1)

# Quote embedding ("to be or not to be")
quote_text = "to be or not to be"
quote_inputs = tokenizer(quote_text, return_tensors='pt')
with torch.no_grad():
    quote_outputs = model(**quote_inputs)
quote_embedding = quote_outputs.last_hidden_state.mean(dim=1)

# Calculate cosine similarity
similarity = cosine_similarity(theme_embedding, quote_embedding)

print(f"Similarity between 'suicide' and 'to be or not to be': {similarity.item()}")

similarity = cosine_similarity(love_embedding, quote_embedding)

print(f"Similarity between 'love' and 'to be or not to be': {similarity.item()}")

"""