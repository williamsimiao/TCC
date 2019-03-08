import os
from allennlp.predictors import Predictor

class Ner_Allen:
    def __init__(self):
        cwd = os.getcwd()
        file_name = "/ner-model-2018.04.26.tar.gz"
        full_path = cwd + "/" + file_name
        self.predictor = Predictor.from_path(full_path)

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
            while i < len(tuple_list):                
                 
                if(tuple_list[i][1] == 'U-PER'):
                    final_list.append(tuple_list[i][0])
                elif(tuple_list[i][1] == 'B-MISC' or tuple_list[i][1] == 'B-ORG'):
                    composto = tuple_list[i][0]
                    i = i+1
                    #Append de midle part, if there is one
                    if(tuple_list[i][1] == 'I-ORG' or tuple_list[i][1] == 'I-MISC'):
                        composto.join([" ", tuple_list[i][0]])
                        # i = i+1
                    #Append de final part
                    composto.join([" ", tuple_list[i][0]])
                    final_list.append(composto)

                i = i+1

            print("/////////////////////")
            for item in final_list:
                print(item)
            if final_list == [] :
                return 
            return  final_list
