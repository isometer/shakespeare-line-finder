class QueryResult:
    def __init__(self, sentence_info, similarity_score):
        coordinates = sentence_info[0]
        self.sentence = sentence_info[1]
        self.play, self.act, self.scene, self.sentence_index = coordinates