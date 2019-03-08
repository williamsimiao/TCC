import mysql.connector
class KB_interface:

    def __init__(self):
        self.mydb = mysql.connector.connect(
                    host="127.0.0.1",
                    user="myuser",
                    passwd="sorvete123!",
                    database='pdf_chato'
                )

        self.mycursor = self.mydb.cursor()
        #Para executar scripts
        # path_to_file = '/Users/william/Desktop/knowledge_base.sql'
        # for line in open(path_to_file):
        #     mycursor.execute(line)
        # for x in self.mycursor:
        #     print(x)
        # print("HELLO")

    def get_entity_id(self, entity):
        Q1 = "SELECT entity_id FROM entities WHERE name = '{}'".format(entity)
        self.mycursor.execute(Q1)
        entity_id = self.mycursor.fetchall()
        if(entity_id != []):
            return entity_id[0][0]
        return 0


    def get_entity_id_and_name(self, entity):
        entity_id = self.get_entity_id(entity)
        if(entity_id is not 0):
            query = "SELECT name FROM entities WHERE identities = {} LIMIT 1".format(entity_id)
            self.mycursor.execute(query)
            entity_name = self.mycursor.fetchall()
            if(entity_name != []):
                return (entity_id, entity_name[0][0])

        return 0

    def get_entity_id_and_name_by_id(self, entity_id):
        if(entity_id is not 0):
            query = "SELECT name FROM entities WHERE identities = {} LIMIT 1".format(entity_id)
            self.mycursor.execute(query)
            entity_name = self.mycursor.fetchall()
            if(entity_name != []):
                return (entity_id, entity_name[0][0])

        return 0
        
    def get_context_id_from_entity_id(self, entity_id):
        context_id_list = []
        #se a entidade não foi encontrada
        if(entity_id == 0):
            print("Entidade nao encontrada")
            return []
        else:
            # self.mycursor.execute("SELECT text FROM contexts WHERE id_entity = {} LIMIT 1".format(entity_id))
            self.mycursor.execute(f"SELECT context_id FROM entities_contexts_rel WHERE entity_id = {entity_id}")
            #TODO ver isso aqui [0][0]
            tuple_list = self.mycursor.fetchall()
            for tup in tuple_list:
                context_id_list.append(tup[0])
            # print(f"context_id_list: {context_id_list}")
            return context_id_list

    def get_context_text(self, context_id):
        self.mycursor.execute(f"SELECT text FROM contexts WHERE context_id = {context_id}")
        #TODO ver isso aqui [0][0]
        context_list = self.mycursor.fetchall()
        return context_list[0][0]    

    def get_capitulo_id(self, capitulo):
        self.mycursor.execute("SELECT context_id FROM contexts WHERE capitulo = {}".format(capitulo))
        context_id = self.mycursor.fetchall()
        return context_id[0][0]

    def get_capitulo_titulo(self, context_id):
        self.mycursor.execute("SELECT capitulo FROM contexts WHERE context_id = {}".format(context_id))
        context_titulo = self.mycursor.fetchall()
        return context_titulo[0][0]

    def insert_entity(self, name):
        if(name is not None):
            self.mycursor.execute(f"INSERT INTO entities (name) SELECT * FROM (SELECT '{name}') AS tmp WHERE NOT EXISTS (SELECT * FROM entities WHERE entities.name = '{name}')")
            self.mydb.commit()

        return 0
    
    def insert_context(self, text, capitulo):
        valid_text = text is not None
        valid_enitity = capitulo is not None
        if(valid_text and valid_enitity):
            self.mycursor.execute("INSERT INTO CONTEXTS (text, capitulo) VALUES ('{}', {})".format(text, capitulo))
            self.mydb.commit()

        return 0

    def insert_entities_contexts_rel(self, entity_id, context_id):
        # self.mycursor.execute(f"INSERT INTO entities_contexts_rel (entity_id, context_id) SELECT * FROM (SELECT {entity_id}, {context_id}) AS tmp WHERE NOT EXISTS (SELECT * from entities_contexts_rel WHERE entity_id = {entity_id} AND context_id = {context_id})")
        self.mycursor.execute("REPLACE INTO entities_contexts_rel (entity_id, context_id) VALUES ('{}', {})".format(entity_id, context_id))
        self.mydb.commit()

    def my_commit(self):
        self.mydb.commit()

    def get_all_relations_types(self):
        self.mycursor.execute("SELECT name FROM relations")
        relations_list = self.mycursor.fetchall()
        return relations_list


    def close_KB(self):
        self.mydb.close()