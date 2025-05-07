# Shakespeare Line Finder
CSCE 470 Info Storage and Retrieval - Final Project

A shakespeare line-finder, finding your favorite lines — no matter how poorly you recall them. 
Built on the principle of semantic search, using SRoBERTa sentence embeddings.

This project has two main use cases: one legitimate, where you've forgotten the exact wording of a line, but you remember the "gist". Just summarize what you remember, and the system will find it!
The less legitimate use case is where you need to say something, but it's got to be Shakespeare for proper comedic effect. Tell the system what you need to say, and it will find the closest Shakespeare came to saying it.

To properly capture the large files, make sure you have `git-lfs` installed before cloning the repo. 

You can install dependencies with `pip install -r requirements.txt`.

A quick demo:

![Shakespeare-demo](https://github.com/user-attachments/assets/7ddbba25-5719-499f-97d0-af1102b97633)
