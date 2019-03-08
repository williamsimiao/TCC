import mysql.connector
class KB_interface:

    def __init__(self):
        self.mydb = mysql.connector.connect(
                    host="127.0.0.1",
                    user="myuser",
                    passwd="sorvete123!",
                    database='knowledge_base'
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
        Q1 = "SELECT identities FROM entities WHERE name = '{}'".format(entity)
        print(Q1)
        self.mycursor.execute(Q1)
        entity_id = self.mycursor.fetchall()
        if(entity_id != []):
            return entity_id[0][0]
        
        #tenatndo procurar nos sinonimos
        Q2 = "SELECT id_entity FROM synonyms WHERE synonym = '{}'".format(entity)
        self.mycursor.execute(Q2)
        entity_id = self.mycursor.fetchall()
        if(entity_id != []):
            return entity_id[0][0]

        return 0


    def get_entity_id_and_name(self, entity):
        entity_id = self.get_entity_id(entity)
        if(entity_id is not 0):
            query = "SELECT name FROM entities WHERE identities = {} LIMIT 1".format(entity_id)
            print("query: {}".format(query))
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
        
    def get_context_from_entityid(self, entity_id):
        #se a entidade não foi encontrada
        if(entity_id == 0):
            return 0
        else:
            self.mycursor.execute("SELECT text FROM contexts WHERE id_entity = {} LIMIT 1".format(entity_id))
            context = self.mycursor.fetchall()
            return context[0][0]

    def get_related_entities(self, entity_id):
        if(entity_id == 0):
            return 0
        else:
            print("KK {}".format(entity_id))
            self.mycursor.execute("SELECT id_entity_B from entities_rel WHERE id_entity_A = {}".format(entity_id))
            related_entities_tuples = self.mycursor.fetchall()
            related_ids = []
            for related_tuple in related_entities_tuples:
                related_ids.append(related_tuple[0])

            self.mycursor.execute("SELECT id_entity_A from entities_rel WHERE id_entity_B = {}".format(entity_id))
            related_entities_tuples = self.mycursor.fetchall()
            for related_tuple in related_entities_tuples:
                related_ids.append(related_tuple[0])

            
            related_id_name_tuple = []
            for one_id in related_ids:
                related_id_name_tuple.append(self.get_entity_id_and_name_by_id(one_id))
            return related_id_name_tuple

    def insert_entity(self, name):
        if(name is not None):
            self.mycursor.execute("INSERT INTO entities (name) VALUES ('{}')".format(name))
            mydb.commit()

        return 0
    
    def insert_context(self, text, entity_id):
        valid_text = text is not None
        valid_enitity = entity_id is not None
        if(valid_text and valid_enitity):
            self.mycursor.execute("INSERT INTO CONTEXTS (text, id_entity) VALUES ('{}', {})".format(text, entity_id))
            mydb.commit()

        return 0

    def insert_entities_relation(self, entity_id_A, entity_id_B, relation_id):
        valid_id_A = entity_id_A is not None
        valid_id_B = entity_id_B is not None
        valid_relation_id = relation_id is not None
        if(valid_id_A and valid_id_B and valid_relation_id):
            self.mycursor.execute("INSERT INTO entities_rel (id_entity_A, id_entity_B, id_relation) VALUES ({}, {}, {})".format(entity_id_A, entity_id_B, relation_id))

        return 0

    def insert_synonym(self, synonym, entity_id):
        valid_synonym = synonym is not None
        valid_entity_id = entity_id is not None
        if(valid_entity_id and valid_synonym):
            final_query = f"INSERT INTO synonyms (synonym, id_entity) VALUES ('{synonym}', {entity_id})"
            print(final_query)
            self.mycursor.execute(final_query)
            mydb.commit()

        return 0

    def get_all_entities(self):
        entities_list = []
        self.mycursor.execute("SELECT name FROM entities")
        result = self.mycursor.fetchall()
        for item in result:
            entities_list.append(item[0])
        return entities_list

    def insert_data_from_dict(self, dictionary):
        # entity_dict = {'name' : '',
        #                 'nicknames': [],
        #                 'relations': [],
        #                 'context': ''}
        print("XX")
        print(dictionary)
        print("XX")
        self.my_start_transaction()
        self.insert_entity(dictionary['name'].lower())
        entity_id = int(self.get_entity_id(dictionary['name'].lower()))
        #nickname insetion
        for nickname in dictionary['nicknames'] :
         self.insert_synonym(nickname.lower(), entity_id)
        
        #relation insertion
        for relation in dictionary['relations'] :
            rel_entity_id = self.get_entity_id(relation[0])
            relation_id = self.get_relation_id(relation[1])
            self.insert_entities_relation(entity_id, rel_entity_id, relation_id)

        #context insertion
        self.insert_context(dictionary['context'].lower(), entity_id)

    def get_all_relations_types(self):
        relations_list = []
        self.mycursor.execute("SELECT name FROM relations")
        result = self.mycursor.fetchall()
        for item in result:
            relations_list.append(item[0])
        return relations_list

    def get_relation_id(self, relation):
        self.mycursor.execute(f"SELECT name FROM relations WHERE name = '{relation}'")
        return self.mycursor.fetchall()

    def insert_feedback(self, question, answer, entityName, positive):
        self.mycursor.execute("INSERT INTO feedback (question, answer, entityName, positive) VALUES ('{}', '{}', '{}', {})".format(question, answer, entityName, positive))
        self.mydb.commit()

    def my_start_transaction(self):
        self.mydb.start_transaction()

    def my_commit(self):
        self.mydb.commit()

    def my_rollback(self):
        self.mydb.rollback()

    def close_KB(self):
        self.mydb.close()