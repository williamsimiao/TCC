import os
import io
import json
import gzip
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error

class Ner_Babel:

    #Return list of tuplets (start, end) of the entities on the text
    def ne_tagging(self, message):
        service_url = 'https://babelfy.io/v1/disambiguate'

        text = message
        lang = 'EN'
        annType = 'NAMED_ENTITIES'
        key  = '909f1dc3-bc2f-4807-89ed-e557a773c051'

        params = {
            'text' : text,
            'lang' : lang,
            'key'  : key
        }

        url = service_url + '?' + urllib.parse.urlencode(params)
        request = urllib.request.Request(url)
        request.add_header('Accept-encoding', 'gzip')
        response = urllib.request.urlopen(request)

        if response.info().get('Content-Encoding') == 'gzip':
            buf = io.BytesIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = json.loads(f.read())

        # retrieving data
        lista_de_tuplas = []
        for result in data:
            # retrieving char fragment
            charFragment = result.get('charFragment')
            cfStart = charFragment.get('start')
            cfEnd = charFragment.get('end')
            trueEnd = cfEnd+1
            lista_de_tuplas.append((cfStart, trueEnd))
        return lista_de_tuplas

    def getStart(self, elem):
        return elem[0]

    def getEnd(self, elem):
        return elem[1]

    def takeStart(self, elem):
        return elem[0][0][0]

    def get_entities(self, message):
        entity_candidates = []
        tuplets = self.ne_tagging(message)
        #The first 'if' below checks for each tuplet(start, end) if there is another
        #tuplet in the list tuplets thats is the meadle of (start, and)
        for tuplet_i in tuplets:
            count = 0
            for tuplet_j in tuplets:
                if(
                    #comeca no inicio e vai até o meio
                    (self.getStart(tuplet_i) >= self.getStart(tuplet_j)
                    and self.getEnd(tuplet_i) < self.getEnd(tuplet_j)) or
                    #comeca no meio e vai ate o fim
                    (self.getStart(tuplet_i) > self.getStart(tuplet_j)
                    and self.getEnd(tuplet_i) <= self.getEnd(tuplet_j)) or
                    #comeca depois do inicio e termina antes do fim
                    (self.getStart(tuplet_i) > self.getStart(tuplet_j)
                    and self.getEnd(tuplet_i) < self.getEnd(tuplet_j))):
                    break
                else:
                    count += 1
            #For some reason 'related to' is identified as an concept by Babelfy
            ## IDEA: Checar mais termos alem de 'related to' 
            if(count == len(tuplets)):
                nome = message[tuplet_i[0]:tuplet_i[1]]
                if(nome != 'related to'):
                    entity_candidates.append(nome)

        print(entity_candidates)
        return entity_candidates

         # with open("entidades.txt") as f:
         #     word_list = f.read().splitlines()
         # for word in word_list:
         #     word = word.lower()
         #
         # reconized_entities = set(entity_candidates) & set(word_list)
         # return reconized_entities, entity_candidates
