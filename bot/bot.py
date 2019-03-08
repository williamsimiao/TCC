import telegram
import os
import sys
import logging
import random
import nltk
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import io
import json
import gzip
import csv
import pprint
# from ner.ner_allen import Ner_Allen
# from ner.ner_simple import Ner_Simple
from ner.ner_babelfy import Ner_Babel
from prediction import Prediction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from nltk import word_tokenize, pos_tag, ne_chunk
# from nltk.tree import Tree
from time import sleep
from telegram import Bot
from emoji import emojize
from configparser import ConfigParser
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, Dispatcher, MessageHandler, \
    Filters
from KB_interface import KB_interface
from text_processing import text_processing

def retrieve_default():
    try:
        config = ConfigParser()
        config.read_file(open(str(os.getcwd())+'/bot/config.ini'))
        return(config['DEFAULT'])
    except Exception as e:
        return(e)


class Chatbot:
    """
    The chatbot per se! Yay <3
    """
    def __init__(self, token):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)
        self.logger = logging.getLogger("log")
        self.bot = Bot(token)
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        info_handler = CommandHandler('info', self.info)
        self.dispatcher.add_handler(info_handler)
        feedbac_handler = CommandHandler('feedback', self.feedback)
        self.dispatcher.add_handler(feedbac_handler)
        insertion_handler = CommandHandler('insert', self.insert)
        self.dispatcher.add_handler(insertion_handler)
        self.dispatcher.add_handler(CallbackQueryHandler(self.button_clicked))
        text_message_handler = MessageHandler(Filters.text, self.text_message)
        self.dispatcher.add_handler(text_message_handler)
        document_message_handler = MessageHandler(Filters.document, self.document_message)
        self.dispatcher.add_handler(document_message_handler)
        self.dispatcher.add_handler(document_message_handler)
        self.dispatcher.add_error_handler(self.error)

        self.ner = Ner_Babel()
        self.prediction = Prediction()
        self.kb_interface = KB_interface()
        self.text_processing = text_processing()
        #O dicionario contem dicionarios que representam que tem o mesmo nome dos 
        # metodos que requisitam precionar de butão pelo usuario, esses dict possuem as 
        # variaveis uteis para lidar com essa ação. 
        # O callback_query do botao será então a identidicação desse estado e botão precionado
        self.global_variables = {"last_question"     : "",
                                 "last_answer"       : "",
                                 "main_entity"       : "",
                                 "related_entity"    : "",
                                 "ambiguos_entities" : [],
                                 "sugests_topics" : {
                                                    "buttons" : []
                                                    },
                                 "ask_for_answer_evaluation" : {
                                                                "buttons" : ["P", "N"]
                                                               },
                                 "sugests_question" : {
                                                        "buttons" : []
                                                      }
                                }
        # self.insetion_states = {
        #                         "active"          : 0,
        #                         "ask_entity_name" : {
        #                                               "active" : 0,
        #                                               "not_valid_message" : "Name not valid"
        #                                               },
        #                         "ask_for_synonyms" : {
        #                                               "active" : 0,
        #                                               "not_valid_message" : "Synonyms not valid"
        #                                              },
        #                         "ask_for_context" : {
        #                                               "active" : 0,
        #                                               "not_valid_message" : "Context not valid"
        #                                              },
        #                         "ask_for_relations" : {
        #                                               "active" : 0,
        #                                               "not_valid_message" : "relations not valid"
        #                                              }        
        #                         }

    

    def verify_bot(self):
        return(self.bot.get_me().username, self.bot.get_me().id)

    def start(self, bot, update):
        """
        Start command to start bot on Telegram.
        @bot = information about the bot
        @update = the user info.
        """
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        sleep(3.5)
        name = update.message['chat']['first_name']
        start_text = (
            f"Hi {name}, I'm a chatbot in development. Feel free to type '/feedback'" + 
                " after any question to let us know that do you think of answer given"
        )
        bot.send_message(chat_id=update.message.chat_id, text=start_text)

    def info(self, bot, update):
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Made for William's TCC",
        )
    
    def feedback(self, bot, update):
        bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        #Now we ask the user if the answer was helpfull
        no_question_bool = self.global_variables["last_question"] != ""
        nome = self.global_variables["last_question"]
        if(no_question_bool):
            self.ask_for_answer_evaluation(bot, update)


    def text_message(self, bot, update):
        #_____________________ colocar tudo a baixo em outro metodo
        entities = self.ner.get_entities(update.effective_message.text)
        bot.send_chat_action(chat_id=update.message.chat_id, 
                             action=telegram.ChatAction.TYPING)
        if(entities is None):
            bot.send_message(chat_id=update.message.chat_id, text="No entity reconized")
        
        #geting entities names(if they are called by nick names)ps: this helps finding the answer
        kb_entities = []
        for entity in entities:
            kb_entities.append(self.kb_interface.get_entity_id_and_name(entity))
            
        #trying on the FIRST[0] entity_id[0] of the list to select the context   
        print(f"AQUI: {kb_entities}")
        if kb_entities == [0] :
            bot.send_message(chat_id=update.message.chat_id, text="Make sure to ask about things in the knowledge base")
        
        else:
            entities_ids, entities_names = zip(*kb_entities)
            self.global_variables["last_question"] = update.effective_message.text
            print(f"{len(kb_entities)}")
            if len(kb_entities) == 1 :
            
                context = self.kb_interface.get_context_from_entityid(kb_entities[0][0])
                question = self.text_processing.rewrite_question(entities, entities_names, update.effective_message.text)
                response = self.prediction.predict(question, context)
                self.global_variables["last_answer"] = response
                #TODO _____________________ colocar tudo a acima em outro metodo

                bot.send_chat_action(chat_id=update.message.chat_id, 
                                    action=telegram.ChatAction.TYPING)
                # bot.send_message(chat_id=update.message.chat_id, text="<b>Question rewrite:</b> {}".format(question), parse_mode=telegram.ParseMode.HTML)
                # bot.send_message(chat_id=update.message.chat_id, text="<b>Answer:</b> {}".format(response), parse_mode=telegram.ParseMode.HTML)
                bot.send_message(chat_id=update.message.chat_id, text="{}".format(response), parse_mode=telegram.ParseMode.HTML)

                #List of entities related to the main entity of the question(the first one 0)
                entities_tuple_list = self.kb_interface.get_related_entities(entities_ids[0])
                self.global_variables["main_entity"] = entities_names[0]
                #Now let us sugest related topics to explore
                self.sugest_topics(update, entities_tuple_list)

            else:
                print("PIPI")
                print(kb_entities)
                bot.send_message(chat_id=update.message.chat_id, text="Select one of the following entities to focus on", parse_mode=telegram.ParseMode.HTML)
                self.show_ambiguos_entities(update, entities_names)

    def sugest_topics(self, update, entities_tuple_list):
        """
        Make the buttons for the entity sugestions
        """
        keyboard = []
        i = 0
        while(i < len(entities_tuple_list)):
            my_list = []
            left_entity_name = entities_tuple_list[i][1]
            query_data_left = "{}sugests_topics".format(str(i))
            self.global_variables["sugests_topics"]["buttons"].append(left_entity_name)
            left_button = InlineKeyboardButton(left_entity_name, callback_data=query_data_left)
            my_list.append(left_button)
            i +=1
            if(i < len(entities_tuple_list)):
                right_entity_name = entities_tuple_list[i][1]
                query_data_right = "{}sugests_topics".format(str(i))
                self.global_variables["sugests_topics"]["buttons"].append(right_entity_name)
                right_button = InlineKeyboardButton(right_entity_name, callback_data=query_data_right)
                my_list.append(right_button)
                i +=1
            keyboard.append(my_list)
        my_reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Explore more topics:', reply_markup=my_reply_markup, parse_mode=telegram.ParseMode.HTML)

    def show_ambiguos_entities(self, update, entities_tuple_list):
        """
        Make the buttons for the entity sugestions
        """
        keyboard = []
        i = 0
        while(i < len(entities_tuple_list)):
            my_list = []
            left_entity_name = entities_tuple_list[i]
            query_data_left = "{}ambiguos_entities".format(str(i))
            left_button = InlineKeyboardButton(left_entity_name, callback_data=query_data_left)
            my_list.append(left_button)
            i +=1
            if(i < len(entities_tuple_list)):
                right_entity_name = entities_tuple_list[i]
                query_data_right = "{}ambiguos_entities".format(str(i))
                right_button = InlineKeyboardButton(right_entity_name, callback_data=query_data_right)
                my_list.append(right_button)
                i +=1
            self.global_variables["ambiguos_entities"].append(left_entity_name)
            self.global_variables["ambiguos_entities"].append(right_entity_name)
            keyboard.append(my_list)
        my_reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Selecte one:', reply_markup=my_reply_markup, parse_mode=telegram.ParseMode.HTML)

    def ask_for_answer_evaluation(self, bot, update):
        query_data = "0ask_for_answer_evaluation"
        positive_button = InlineKeyboardButton(emojize(":thumbs_up:"), callback_data=query_data)

        query_data = "1ask_for_answer_evaluation"
        negative_button = InlineKeyboardButton(emojize(":thumbs_down:"), callback_data=query_data)

        query_data = "2ask_for_answer_evaluation"
        not_now_button = InlineKeyboardButton("Not now", callback_data=query_data)

        binary_markup = InlineKeyboardMarkup([[positive_button, negative_button, not_now_button]])
        update.message.reply_text('This answer was useful?',
            reply_markup=binary_markup, parse_mode=telegram.ParseMode.HTML)

    def sugest_questions(self, bot, query):
        question_entity = self.global_variables["main_entity"]
        related_entity = self.global_variables["related_entity"]
        q1 = "What is {}?".format(related_entity)
        q2 = "Is {} a kind of {}?".format(related_entity, question_entity)
        questios_union_string = "<b>1</b>: {}\n<b>2</b>: {}".format(q1, q2)
        possible_question_list = [q1, q2]
        keyboard = []
        i = 0
        while(i < len(possible_question_list)): 
            my_list = []

            #Mounting the first button
            query_data = "{}sugests_question".format(str(i))
            self.global_variables["sugests_question"]["buttons"].append(possible_question_list[i])
            left_button = InlineKeyboardButton(str(i+1), callback_data=query_data, parse_mode=telegram.ParseMode.HTML)
            my_list.append(left_button)
            i = i+1
            #Mounting the second button
            if(i < len(possible_question_list)):
                query_data = "{i}{sugests_question}"
                self.global_variables["sugests_question"]["buttons"].append(possible_question_list[i])
                rigth_button = InlineKeyboardButton(str(i+1), callback_data=query_data) 
                
                #Puting the row of buttons together
                my_list.append(rigth_button)
                i = i+1
            keyboard.append(my_list)
        my_reply_markup = InlineKeyboardMarkup(keyboard)

        text = "<b>{}</b>\nChoose a question:\n{}".format(related_entity, questios_union_string)
        bot.edit_message_text(text=text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id, reply_markup=my_reply_markup, parse_mode=telegram.ParseMode.HTML)

    def button_clicked(self, bot, update):
        query = update.callback_query
        query_str = query.data
        button_index = int(query_str[0])
        state = query_str[1:]        
        message = ""
        if(state == "ask_for_answer_evaluation"):
            if(button_index == 0 or button_index == 1):
                #button Index: 0 is positive 1 is negative
                self.kb_interface.insert_feedback(self.global_variables["last_question"],
                                                  self.global_variables["last_answer"],
                                                  self.global_variables["main_entity"],
                                                  button_index )
                message = "Thank you for the feedback"
            else:
                message = "OK"

            bot.edit_message_text(text=message,
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)

        elif(state == "sugests_topics"):
            #name of the related entity as shown in the button clicked
            related_entity_name = self.global_variables["sugests_topics"]["buttons"][button_index]
            self.global_variables["related_entity"] = related_entity_name
            self.sugest_questions(bot, query)

        elif(state == "sugests_question"):
            related_entity_name = self.global_variables["related_entity"]
            related_id = self.kb_interface.get_entity_id(related_entity_name)
            context = self.kb_interface.get_context_from_entityid(related_id)
            question = self.global_variables["sugests_question"]["buttons"][button_index]
            response = self.prediction.predict(question, context)
            text = "Question: {}\nAnswer:{}".format(question, response)
            bot.edit_message_text(text=text,
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)

        elif(state == "ambiguos_entities"):
            selectedEntity = self.global_variables["ambiguos_entities"][button_index]
            self.global_variables["main_entity"] = selectedEntity
            selected_id = self.kb_interface.get_entity_id(selectedEntity)
            context = self.kb_interface.get_context_from_entityid(selected_id)
            question = self.global_variables["last_question"]
            response = self.prediction.predict(question, context)
            text = "<b>Focus</b> Entity: {}\n<b>Answer</b>:{}".format(self.global_variables["main_entity"], response)
            bot.edit_message_text(text=text,
                                    chat_id=query.message.chat_id,
                                    message_id=query.message.message_id)




    def document_message(self, bot, update):
        file_id = update.message.document.file_id
        newFile = bot.get_file(file_id)
        FILE_PATH = "bot/new_entity.csv"
        newFile.download(FILE_PATH)
        self.read_insertion_file(bot, update, FILE_PATH)

    def insert(self, bot, update):
        # print("Inserion mode activated")
        # print("Inserion mode activated")
        #SEND 2 FILES, template e lista de entidades contidas
        message = "Look at the file entidades.txt to see what entities already exist. Then Download the CSV file and put the information you want to insert and send it back"
        bot.send_message(chat_id=update.message.chat_id, text=message)
        self.build_entity_file()
        bot.send_document(chat_id=update.message.chat_id, document=open('bot/entidades.txt', 'rb'))
        bot.send_document(chat_id=update.message.chat_id, document=open('bot/insertion_file.csv', 'rb'))

    def build_entity_file(self):
        entity_list = self.kb_interface.get_all_entities()
        relations_list = self.kb_interface.get_all_relations_types()
        FILE_PATH = "bot/entidades.txt"
        with open(FILE_PATH, "w") as data_file:
            data_file.write("Entities:\n")
            for entity in entity_list:
                data_file.write(f"{entity}\n")
            data_file.write("\nRelations:\n")
            for relation in relations_list:
                data_file.write(f"{relation}\n")

    def read_insertion_file(self, bot, update, file_path):
        # bot.send_message(chat_id=update.message.chat_id, text="Error reading file, please check if it conforms to the template")
        bot.send_message(chat_id=update.message.chat_id, text="Success.Entity inserted into knowledge base")

        entity_dict = {'name' : '',
                        'nicknames': [],
                        'relations': [],
                        'context': ''}
        with open(file_path, 'r', newline='') as csvfile:
            line_count = 1
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if(line_count == 2):
                    entity_dict['name'] = row[0]
                    entity_dict['nicknames'].append(row[1])
                    entity_dict['relations'].append((row[2], row[3]))
                    entity_dict['context'] = row[4]
                elif(line_count > 2):
                    if(row[1] != ''):
                        entity_dict['nicknames'].append(row[1])
                    if(row[2] != '' and row[3] != ''):
                        entity_dict['relations'].append((row[2], row[3]))
                line_count += 1
        # pprint.pprint(entity_dict)
        self.kb_interface.insert_data_from_dict(entity_dict)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def run(self):
        # Start the Bot
        print('Bot configured. Receiving messages now.')
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()


if __name__ == '__main__':
    token = retrieve_default()['token']
    if(not token):
        print('Configuration file not found.')
        sys.exit(1)
    x = Chatbot(token)
    x.run()
