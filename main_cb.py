# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 22:52:49 2020

@author: VanHa
"""
# import os
# os.chdir('C:/Users/VanHa')

import requests
import json
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

TOKEN= "1097801707:AAGTDaSyGoZRrkfKmMz7gn-x0Bh-uWaRGJc"
url = "https://api.telegram.org/bot"+ TOKEN+"/"

bot = telepot.Bot(TOKEN)

def get_chat_id(update):
    chat_id = update["message"]["chat"]["id"]
    return chat_id

def get_user_name(update):
    user_name = update["message"]["from"]["first_name"] + " " + update["message"]["from"]["last_name"]
    return user_name

def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text

def last_update(req):
    response = requests.get(req+"getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result)-1
    return result[total_updates]

def send_message(chat_id, mes):
    params = {"chat_id": chat_id, "text": mes}
    response =  requests.post(url + "sendMessage", data = params)
    return response


#create message

greeting_sentence = ["hello", "hi", "Hello", "Hi", "Hello Chatbot", "Hi Chatbot", "Back"]

cor_info = "Coronaviruses are a large family of viruses which may cause illness in animals or humans. In humans, several coronaviruses are known to cause respiratory infections ranging from the common cold to more severe diseases such as MERS and SARS. COVID-19 is the infectious disease caused by the most recently discovered coronavirus. This new virus and disease were unknown before the outbreak began in Wuhan, China, in December 2019"

symptom1 = "\n The most common symptoms of COVID-19 are fever, tiredness, and dry cough. Some patients may have aches and pains, nasal congestion, runny nose, sore throat or diarrhea. These symptoms are usually mild and begin gradually.\n" 
symptom2 = "\n Some people become infected but don’t develop any symptoms and don't feel unwell. Around 1 out of every 6 people who gets COVID-19 becomes seriously ill and develops difficulty breathing. Older people, and those with underlying medical problems like high blood pressure, heart problems or diabetes, are more likely to develop serious illness. People with fever, cough and difficulty breathing should seek medical attention."

markup = ReplyKeyboardMarkup(keyboard=[['Understanding about Coronavirus', KeyboardButton(text='The symtoms of Covid_19 and its spread')],["Health Advisory", "The update of Coronavirus disease situation"]])
markup2 =  ReplyKeyboardMarkup(keyboard=[['Keep hygenic', 'Wearing masks', 'Cleaning and diseffection advisory', 'Travel Advisory', 'Back']])  



def make_message(message, from_, username):
    if message in greeting_sentence: 
        bot.sendMessage(from_, "Hello "+ username +"!\n" + "I am happy to give you information about Coronavirus disease (COVID-19) \n"  
                        , reply_markup = markup) 
        
    elif message == "Understanding about Coronavirus":
        bot.sendMessage(from_,cor_info)
    elif message == "The symtoms of Covid_19 and its spread":
        bot.sendPhoto(from_ , "https://www.winyateshc.co.uk/website/M81019/files/coronasymp1.jpg")
        bot.sendMessage(from_,symptom1 + symptom2, reply_markup= markup)
        
        ## create command about question: if I have mild symptom"
        # bot.sendPhoto(from_ , "https://i.imgur.com/HpVZS2G.jpg")
        
    elif message == "Health Advisory":
        bot.sendPhoto(from_, "https://i.imgur.com/inzvlTp.jpgg", reply_markup = markup2 )      
        
    elif message == "Keep hygenic":    
        bot.sendMessage(from_, "TO KEEP PERSONAL HYGENIE \n")
        bot.sendPhoto(from_, "https://i.imgur.com/hhhzJpA.jpg", reply_markup = markup2 )

    elif message == "Wearing masks":    
        bot.sendMessage(from_, "TO WEAR MASKS CORRECTLY")
        bot.sendPhoto(from_, "https://i.imgur.com/klhSTD5.jpg")
        bot.sendPhoto(from_, "https://www.moh.gov.sg/docs/librariesprovider5/default-document-library/to-mask-or-not-to-mask---moh-copy-01.jpg", reply_markup = markup2)
    
    elif message == "Cleaning and diseffection advisory":    
        bot.sendPhoto(from_ , "https://i.imgur.com/1Ji7gaM.jpg", reply_markup = markup2)   
        
    elif message =="Travel Advisory":
        bot.sendPhoto(from_, "https://i.imgur.com/QKqM5vE.jpg", reply_markup = markup2)

    elif message =="The update of Coronavirus disease situation":
        bot.sendMessage(from_, "The herein website is the coronavirus map given by the John Hopskin engeneering:" +"https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6", parse_mode ="HTML", disable_web_page_preview = True)
    
    else:
        bot.sendMessage(from_,"Sorry, I don't have information about that. I will tell you later.")
    
    
   

def main():
    update_id  = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id ==update["update_id"]:
            try: 
                message = get_message_text(update)
            except:
                message = None
            from_ = get_chat_id(update)
            username= get_user_name(update)
            make_message(message, from_, username)
            update_id += 1
main()








