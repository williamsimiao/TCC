"Cria indice de entidade "
import os
import re
import sys
import pprint
from ner.ner_babelfy import Ner_Babel
from tika import parser
import nltk
import json

BABELFY_LIMIT = 5000
indice_path = str(os.getcwd()) + '/bot/' + "indiceNOVO.txt"
indice_file = open(indice_path, "w+")

FILE_PATH = str(os.getcwd()) + '/bot/' + "full_file.txt"
with open(FILE_PATH) as data_file:
    data=data_file.read().replace('\n', '')
    section_pattern = r'\~(.*?)\~(.*?)\~'
    iterator = re.findall(section_pattern, data)
    lista_tuplas = list(iterator)

#Lembrando: tupla[0] é o titulo do capitulo
#           tupla[1] é o contexto
for tupla in lista_tuplas:
    contexto = tupla[1]
    if len(contexto) >= BABELFY_LIMIT:
        contexto = contexto[:BABELFY_LIMIT-1]
    print(f"CONTEXTO: {contexto}")
    nltk_result = nltk.pos_tag(nltk.word_tokenize(contexto))
    #setando pra ser igual a pergunta original
    # token_tupla  = (palavra, POS)
    for token_tupla in nltk_result:
        #VBG VBN VBP
        if(token_tupla[1] == "VB" or token_tupla[1] == "VBZ" 
            or token_tupla[1] == "VBN" or token_tupla[1] == "VBP"):
            # removendo o verbo da lista
            index = contexto.find(token_tupla[0])
            novo_index = index+len(token_tupla[0])
            contexto = contexto[:index]+contexto[novo_index:]
    entities = Ner_Babel().get_entities(contexto)

    entities_string = "\n".join(entities)
    indice_file.write(tupla[0] + entities_string.lower() + "\n\n")
