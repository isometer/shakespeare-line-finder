import matplotlib.pyplot as plt
from collections import defaultdict 

# Function to plot word counts of plays
def plot_word_counts(plays):
    titles = list(plays.keys())
    word_counts = [plays[title].word_cnt for title in titles]
    
    plt.figure(figsize=(10, 6))
    plt.bar(titles, word_counts, color='skyblue')
    plt.title('Word Count per Work')
    plt.xlabel('Works')
    plt.ylabel('Word Count')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig('plots/word_counts.png')
    plt.close()  # Close the figure after saving

# Function to plot the number of characters per play
def plot_character_counts(plays):
    titles = list(plays.keys())
    character_counts = [len(plays[title].characters) for title in titles]
    
    plt.figure(figsize=(10, 6))
    plt.bar(titles, character_counts, color='salmon')
    plt.title('Number of Characters per Work')
    plt.xlabel('Works')
    plt.ylabel('Number of Characters')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig('plots/character_counts.png')
    plt.close()  # Close the figure after saving

# Function to plot the structure of plays (acts and scenes)
def plot_play_structure(plays):
    plt.figure(figsize=(10, 6))
    for title, play in plays.items():
        acts = [x[0] for x in play.structure]
        scenes = [x[1] for x in play.structure]
        plt.plot(acts, scenes, label=title)
    
    plt.title('Acts and Scenes per Work')
    plt.xlabel('Acts')
    plt.ylabel('Number of Scenes')
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/play_structure.png')
    plt.close()  # Close the figure after saving

# Function to plot the vocabulary space (V) of each play
def plot_vocabulary_space(plays):
    titles = list(plays.keys())
    vocab_spaces = [len(plays[title].V) for title in titles]
    
    plt.figure(figsize=(10, 6))
    plt.bar(titles, vocab_spaces, color='lightgreen')
    plt.title('Vocabulary Space per Work')
    plt.xlabel('Works')
    plt.ylabel('Vocabulary Space (V)')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig('plots/vocab_space.png')
    plt.close()  # Close the figure after saving


def plot_vocabulary_distribution(plays, play_title, top_n=10):
    """
    Plots the frequency distribution of the top N words in the play's vocabulary.
    
    :param plays: Dictionary of Play objects
    :param play_title: The title of the play you want to visualize
    :param top_n: Number of top words to display (default is 10)
    """
    play = plays[play_title]
    vocab_space = play.V  # Get the vocabulary space (bag of words) for the play
    
    # Sort the vocabulary by frequency (value) in descending order
    sorted_vocab = sorted(vocab_space.items(), key=lambda x: x[1], reverse=True)
    
    # Get the top N words and their frequencies
    top_words = [word for word, freq in sorted_vocab[:top_n]]
    top_freqs = [freq for word, freq in sorted_vocab[:top_n]]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(top_words, top_freqs, color='lightcoral')
    plt.title(f'Top {top_n} Words in "{play_title}" by Term Frequency')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f'plots/vocab_distribution_{play_title}.png')
    plt.close()  # Close the figure after saving


def plot_overall_vocabulary_distribution(plays, top_n=10):
    """
    Plots the frequency distribution of the top N words in the overall vocabulary of all plays.
    
    :param plays: Dictionary of Play objects
    :param top_n: Number of top words to display (default is 10)
    """
    overall_vocab = defaultdict(int)

    # Aggregate term frequencies across all plays
    for play in plays.values():
        for word, freq in play.V.items():
            overall_vocab[word] += freq

    # Sort the overall vocabulary by frequency in descending order
    sorted_vocab = sorted(overall_vocab.items(), key=lambda x: x[1], reverse=True)

    # Get the top N words and their frequencies
    top_words = [word for word, freq in sorted_vocab[:top_n]]
    top_freqs = [freq for word, freq in sorted_vocab[:top_n]]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(top_words, top_freqs, color='lightblue')
    plt.title(f'Top {top_n} Words in Overall Vocabulary of All Plays')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save the plot
    plt.savefig('plots/overall_vocab_distribution.png')
    plt.close()  # Close the figure after saving




"""

# Example calls:
# Assuming you have a dictionary of Play objects called 'plays', where keys are play titles
plot_word_counts(plays)
plot_character_counts(plays)
plot_play_structure(plays)
plot_vocabulary_space(plays)
plot_vocabulary_distribution(plays, play_title="A Midsummer Night's Dream", top_n=10)
plot_overall_vocabulary_distribution(plays, top_n=40)


"""