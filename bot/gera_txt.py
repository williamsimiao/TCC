# -*- coding: utf-8 -*-

import os
import re
import sys
import pprint
from ner.ner_babelfy import Ner_Babel
from tika import parser
import nltk
#besshi_e23

def find_qa_by_chapter(pdf_content, chapter_pattern):
    content_match = re.finditer(chapter_pattern, pdf_content)
    return content_match

parsedPDF = parser.from_file("bot/besshi_e23.pdf")
pdf = parsedPDF["content"]
full_file = open("full_file.txt", "w+")
full_file.write(pdf)
# # print(f"{pdf}\n\n\n")
# # for i in range(1, 11):
# # chapter_pattern = r'\n\d\.....'
# chapter_pattern = r'\n\d\..*\n'
# # chapter_pattern = "Monthly"
# iterator = find_qa_by_chapter(pdf, chapter_pattern)
# # for item in thing:
# #     pprint.pprint(item)
# lista_thing = list(iterator)
# m_file = open("output.txt","w+")
# indice_file = open("indiceERRADO.txt", "w+")
# lista_tuplas_qa = []
# for i in range(0, len(lista_thing)):
#     line_pattern = r'\n(Q\d.*\n)(A\d.*\n)'
#     section_name = pdf[lista_thing[i].start() :lista_thing[i].end()]
#     if(i+1 == len(lista_thing)):
#         full_section_string  = pdf[lista_thing[i].start() :]
#     else:
#         full_section_string  = pdf[lista_thing[i].start() : lista_thing[i+1].start()]
#     # lista de tupla, [0] é Q e [1] é A, devido aos groups '()()'
#     lista_tuplas_qa = re.findall(line_pattern, full_section_string)
#     m_file.write(f"'{section_name[1:-1]}'\n")
#     indice_list = []
#     for tupla in lista_tuplas_qa:
#         #printing Q
#         m_file.write(f"\t{tupla[0]}\n")
#         #printing A
#         # print(f"\t{tupla[1]}\n")
        
#         nltk_result = nltk.pos_tag(nltk.word_tokenize(tupla[0]))
#         # print(f"TAG: {nltk_result}")
#         #setando pra ser igual a pergunta original
#         pergunta = tupla[0]
#         # print(f"pergunta antes: {pergunta}")
#         for token_tupla in nltk_result:
#             #VBG VBN VBP
#             if(token_tupla[1] == "VB" or token_tupla[1] == "VBZ" 
#                 or token_tupla[1] == "VBN" or token_tupla[1] == "VBP"):
#                 # removendo o verbo da lista
#                 index = pergunta.find(token_tupla[0])
#                 # print(f"verbo: {token_tupla[0]}")
#                 # print(f"com verbo: {tupla[0]}")
#                 novo_index = index+len(token_tupla[0])
#                 pergunta = pergunta[:index]+pergunta[novo_index:]
#         # print(f"pergunta depois: {pergunta}")
#         # print("\n")
#         entities = Ner_Babel().get_entities(pergunta)
#         # indice_list.append()            

#         string = "\n".join(entities)
#         indice_list.append(string)
#     uma_lista = "\t\n".join(indice_list)
#     indice_file.write(f"{section_name} \n{uma_lista}")


