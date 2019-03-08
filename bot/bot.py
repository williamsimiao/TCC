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
        cancel_handler = CommandHandler('cancel', self.cancel)
        self.dispatcher.add_handler(cancel_handler)
        self.dispatcher.add_handler(CallbackQueryHandler(self.button))
        message_handler = MessageHandler(Filters.text, self.text_message)
        self.dispatcher.add_handler(message_handler)
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
        self.insetion_states = {
                                "active"          : 0,
                                "ask_entity_name" : {
                                                      "active" : 0,
                                                      "not_valid_message" : "Name not valid"
                                                      },
                                "ask_for_synonyms" : {
                                                      "active" : 0,
                                                      "not_valid_message" : "Synonyms not valid"
                                                     },
                                "ask_for_context" : {
                                                      "active" : 0,
                                                      "not_valid_message" : "Context not valid"
                                                     },
                                "ask_for_relations" : {
                                                      "active" : 0,
                                                      "not_valid_message" : "relations not valid"
                                                     }        
                                }

    def deactivate_all_states(self):
        for key in self.insetion_states.keys():
            self.insetion_states[key]["active"] = 0
        return 0

    def activate_state(self, state):
        self.deactivate_all_states()
        if(state in self.insetion_states):
            self.insetion_states[state]["active"] = 1
        return 0

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
            f"Hi {name}, I'm a chatbot trying my best to answer questions about your Document."
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
        print(f"Z{nome}Z")
        if(no_question_bool):
            self.ask_for_answer_evaluation(bot, update)

    def update_table(self, curr_table, context_id_list):
        "Atuiliza tabela que conta o numero de contextos encontrados"
        for context_id in context_id_list:
            found = False
            for entry in curr_table:
                if context_id == entry["context_id"]:
                    found = True
                    entry["frequency"] +=1
            if not found:
                curr_table.append({"context_id":context_id,
                                   "frequency": 1
                                  })
        return curr_table

    def pick_context(self, entities):
        curr_table = []
        for entity in entities:
            entity_id = self.kb_interface.get_entity_id(entity)
            print(f"ENTITY: {entity}")
            context_id_list = self.kb_interface.get_context_id_from_entity_id(entity_id)
            self.update_table(curr_table, context_id_list)
        #ordenando curr_table
        curr_table = sorted(curr_table, key=lambda entry: entry["frequency"])
        #pegando o context_id de maior ocorrencia(ultimo)
        id_most_frequent = curr_table[-1]["context_id"]
        return id_most_frequent
            

    def text_message(self, bot, update):
        # entities = self.ner.get_entities(update.effective_message.text)
        message = update.effective_message.text
        bot.send_chat_action(chat_id=update.message.chat_id, 
                             action=telegram.ChatAction.TYPING)

        nltk_result = nltk.pos_tag(nltk.word_tokenize(message))
        #removendo verbos antes de reconhecer entidades
        for token_tupla in nltk_result:
            #VBG VBN VBP
            if(token_tupla[1] == "VB" or token_tupla[1] == "VBZ" 
                or token_tupla[1] == "VBN" or token_tupla[1] == "VBP"):
                # removendo o verbo da lista
                index = message.find(token_tupla[0])
                novo_index = index+len(token_tupla[0])
                message = message[:index]+message[novo_index:]
        entities = self.ner.get_entities(message)
        if(entities is None):
            bot.send_message(chat_id=update.message.chat_id, text="No entity reconized")
            return
                    
        id_context = self.pick_context(entities)
        tituloCap = self.kb_interface.get_capitulo_titulo(id_context)
        print(f"THE CONTEXT:{tituloCap}")
        bot.send_message(chat_id=update.message.chat_id, text=f"<b>Context selected:</b> {tituloCap}", parse_mode=telegram.ParseMode.HTML)
        
        context = self.kb_interface.get_context_text(id_context)


        if(context == 0):
            bot.send_message(chat_id=update.message.chat_id, text="Entity not in knowledge base")
            return

        response = self.prediction.predict(update.effective_message.text, context)
        response = response[:4095]
        bot.send_message(chat_id=update.message.chat_id, text=f"<b>Response:</b> {response}", parse_mode=telegram.ParseMode.HTML)
        
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

    def button(self, bot, update):
        query = update.callback_query
        query_str = query.data
        button_index = int(query_str[0])
        state = query_str[1:]        
        message = ""
        if(state == "ask_for_answer_evaluation"):
            if(button_index == 0 or button_index == 1):
                #TODO SAVE IN DATABASE
                #save self.global_variables["last_question"]
                #save self.global_variables["last_answer"]
                #save button_index
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

    def insert(self, bot, update):
        print("Inserion mode activated")
        self.insetion_states["active"] = 1
        ask_entity_name(bot, update)

    def cancel(self, bot, update):
        self.insetion_states["active"] = 0
        print("cancel insertion mode")

    def ask_entity_name(self, bot, update):
        message = "What the <b>NAME<\b> of th entity?"
        self.activate_state("ask_entity_name")
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

    def ask_for_synonyms(self, bot, update):
        message = "The has any the <b>SYNONYMS<\b> ?"
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

    def ask_for_context(self, bot, update):
        message = "What is the <b>CONTEXT<\b> for the entity?"
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

    def ask_for_relations(self, bot, update):
        message = "What is the <b>CONTEXT<\b> for the entity?"
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.HTML)


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
