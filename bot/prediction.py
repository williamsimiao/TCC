import os
from allennlp.predictors import Predictor


class Prediction:
    def __init__(self):
        cwd = os.getcwd()
        file_name = "/bidaf-model-2017.09.15-charpad.tar.gz"
        full_path = cwd + "/" + file_name
        self.predictor = Predictor.from_path(full_path)



    def predict(self, question, context):
        if(question == "" or context == ""):
            return "empty"
        else:
            results = self.predictor.predict(passage=context, question=question)
            return results["best_span_str"]
