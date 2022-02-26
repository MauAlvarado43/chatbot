from thefuzz import fuzz
import re


class Bot:

    def __init__(self, db):
        self.db = db

    def format_word(self, w):
        replacements = [["á", "a"], ["é", "e"], ["í", "i"], ["ó", "o"], ["ú", "u"]]
        [w.replace(letter[0], letter[1]) for letter in replacements]
        re.sub(";:_,.-¿\?¡!¨´\*+!\"#$%&/\(\)=\|°¬", "", w)
        return w

    def get_words_simliarity(self, w1, w2):
        return fuzz.ratio(self.format_word(w1.lower()), self.format_word(w2.lower())) / 100

    def get_probability(self, answer_id, request):

        self_ponderation = 0
        max_ponderation = 0
        keywords = self.db.get_all_keywords(answer_id)

        for keyword in keywords:

            best_ponderation_word = 0

            for word in request.split(" "):
                best_ponderation_word = max(self.get_words_simliarity(word, keyword[2]), best_ponderation_word)

            self_ponderation += best_ponderation_word * keyword[1]
            max_ponderation += keyword[1]

        if max_ponderation == 0:
            return 0

        return self_ponderation / max_ponderation

    def get_response(self, request):

        best_answer = 0
        best_probability = 0
        answers = self.db.get_all_answers()
        no_answer = None

        for index, answer in enumerate(answers):

            if index == 0:
                no_answer = answer[1]

            probability = self.get_probability(answer[0], request)

            # print(f"{probability} -> {answer[1]}")

            if best_probability < probability:
                best_probability = probability
                best_answer = answer[1]

        if best_probability < 0.3:
            return no_answer

        return best_answer
