import os
from allennlp.predictors import Predictor

class Ner_Simple:

    def get_entities(self, text):
        if(text == ""):
            print("empty")
            return []
        else:
            results = self.predictor.predict(sentence=text)
            zipped = zip(results["words"], results["tags"])
            tuple_list = list(zipped)
            print(tuple_list)
            i=0
            final_list = []
            for tuple in tuple_list:
                if(tuple[1] != 'O'):
                    final_list.append(tuple)

            print(final_list)
            return  final_list
