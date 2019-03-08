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
        my_tuple = self.get_entity_id_and_name("ml")
        myName = self.get_related_entities(my_tuple[0])
        print("myName: {}".format(myName))

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


    def close_KB(self):
        self.mydb.close()

if __name__ == '__main__':
    kb = KB_interface()