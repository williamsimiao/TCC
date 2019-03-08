import os
import sys
import json

class text_processing:
    # def __init__(self):
        
    def rewrite_question(self, original_entities, kb_entities, question):
            new_question = question
            #using all identified entities for replacing on question
            for x in range(0, len(original_entities)):
                if(kb_entities[x] != 0):
                    #replacing next entitie on previus iteration version of new_question
                    new_question = new_question.replace(original_entities[x], kb_entities[x])
            print(new_question)
            return new_question
