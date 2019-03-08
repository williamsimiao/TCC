"Para importar o indice de entidades para o banco de dados"
import os
import sys
import logging
import io
from KB_interface import KB_interface
filepath = str(os.getcwd()) + '/bot/' + "indice.txt"
with open(filepath) as fp:
    capitulo = fp.readline()
    line = fp.readline()
    cnt = 1
    while line:
        if(line == "\n"):
            #Descartando o titulo do capitulo
            capitulo = fp.readline()
            line = fp.readline()
            cnt += 1
        else:
            #removendo o \n do fim da linha
            line = line.strip('\n')
            KB_interface().insert_entity(line)
            entity_id = KB_interface().get_entity_id(line)
            # print(f"entity_id {entity_id}")
            
            capitulo_id = KB_interface().get_capitulo_id(cnt)
            print(f"entity_id:{entity_id}, capitulo_id:{capitulo_id}")
            KB_interface().insert_entities_contexts_rel(entity_id, capitulo_id)
            
            line = fp.readline()


# Desktop⁩/question_answering⁩/sql⁩/pdf_sql_creation.sql