




class Play:
    def __init__(self, title, word_cnt, characters, structure, V, acts, scenes):
        self.title = title
        self.word_cnt = word_cnt        # total count of words in txt file
        self.characters = characters    # character list
        self.structure = structure      # list where each tuple = (act_no, # scenes in act)
        self.V = V                      # vocabulary space for entire play (raw term frequency)
        self.acts = acts                # list of dictionaries of vocabulary spaces for each act
        self.scenes = scenes            # dictionary where each act is key and each value is a list of the vocabulary spaces for that scene
        