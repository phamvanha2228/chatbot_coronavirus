# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 22:52:49 2020

@author: VanHa
"""
# import os
# os.chdir('C:/Users/VanHa')
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
from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pandas as pd
import re
import time
from telegram import ParseMode
import numpy as np




#create message

greeting_sentence = ["hello", "hi", "Hello", "Hi", "Hello Chatbot", "Hi Chatbot", "Back"]

cor_info = "Coronaviruses are a large family of viruses which may cause illness in animals or humans. In humans, several coronaviruses are known to cause respiratory infections ranging from the common cold to more severe diseases such as MERS and SARS. COVID-19 is the infectious disease caused by the most recently discovered coronavirus. This new virus and disease were unknown before the outbreak began in Wuhan, China, in December 2019"

symptom1 = "\n The most common symptoms of COVID-19 are fever, tiredness, and dry cough. Some patients may have aches and pains, nasal congestion, runny nose, sore throat or diarrhea. These symptoms are usually mild and begin gradually.\n" 
symptom2 = "\n Some people become infected but don’t develop any symptoms and don't feel unwell. Around 1 out of every 6 people who gets COVID-19 becomes seriously ill and develops difficulty breathing. Older people, and those with underlying medical problems like high blood pressure, heart problems or diabetes, are more likely to develop serious illness. People with fever, cough and difficulty breathing should seek medical attention."

markup = ReplyKeyboardMarkup(keyboard=[['Understanding about Coronavirus', KeyboardButton(text='The symtoms of Covid_19 and its spread')],["Health Advisory", "The update of Coronavirus disease situation"]])
markup2 =  ReplyKeyboardMarkup(keyboard=[['Keep hygenic', 'Wearing masks', 'Cleaning and diseffection advisory', 'Travel Advisory', 'Back']])  



#### Craw data of Coronavirus



url2 = "https://www.worldometers.info/coronavirus/"
# req = Request(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'})
html = urlopen(url2).read()
soup_1 = BeautifulSoup(html, features="lxml")
r= soup_1.find_all('tr')



list_rows = []
for row in r:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)


col_labels = soup_1.find_all('th')   

all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
df2 = pd.DataFrame(all_header)
df2 = df2[0].str.replace(', ', ';')
df3 = df2.str.split(';', expand=True)


df = pd.DataFrame(list_rows)
df1 = df[0].str.replace(' , ', ';')
df1 = df1.str.replace(', ', ';')
df1 = df1.str.replace(',', '')
df1 = df1.str.split(';', expand = True)


frames = [df3, df1]

df4 = pd.concat(frames)
df5 = df4.rename(columns=df4.iloc[0])
df6 = df5.dropna(axis=0, how='any')
df7 = df6.drop(df6.index[0])

df7.rename(columns={'[Country,Other': 'Country'},inplace=True)
df7.rename(columns={'Tot\xa0Cases/1M pop]': 'TotCasesper1Mpop'},inplace=True)
df7.rename(columns={'NewCases': 'New'},inplace=True)
df7.rename(columns={'TotalCases': 'Total'},inplace=True)
df7.rename(columns={'TotalRecovered': 'Recovered'},inplace=True)

df7['Country'] = df7['Country'].str.strip('[ ')
df7['TotCasesper1Mpop'] = df7['TotCasesper1Mpop'].str.strip(']')
df7['New'] = df7['New'].str.replace('+', '')
df7['New'] = df7['New'].str.strip()
df7[["Total", "New", "TotalDeaths", "NewDeaths", "Recovered" ]]= df7[["Total", "New", "TotalDeaths", "NewDeaths", "Recovered" ]].apply(pd.to_numeric) 

html_df = df7.head(5)[["Country", "Total", "New", "TotalDeaths", "NewDeaths", "Recovered" ]].to_string()

str_total =str(df7['Total'].sum())

########################### CREATE BOT ##################################


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
    response = requests.get(req+"getUpdates", verify = False)
    response = response.json()
    result = response["result"]
    total_updates = len(result)- 1
    return result[total_updates]

def send_message(chat_id, mes):
    params = {"chat_id": chat_id, "text": mes}
    response =  requests.post(url + "sendMessage", data = params)
    return response



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
        bot.sendMessage(from_, "Total new cases over the world til today:" + str(df7['New'].sum()) + ". The average of new cases: " + str(df7['New'].mean()) )       
        bot.sendMessage(from_, "Total cases over the world : " + str_total )
        bot.sendMessage(from_, "Top 5 countries or region having infected cases ")
        bot.sendMessage(from_, html_df, parse_mode =ParseMode.HTML)
        bot.sendMessage(from_, "The herein website is the coronavirus map given by the John Hopskin engeneering:" +"https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6", parse_mode ="HTML", disable_web_page_preview = True)
    elif message == "/start":
        bot.sendMessage(from_,"Hello "+ username +"!\n" + "I am happy to give you information about Coronavirus disease (COVID-19) \n"  
                        , reply_markup = markup)        
    else:
        bot.sendMessage(from_,"Sorry, I cannot think of a reply for that.")
    
    
   

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
            
            
       
time.sleep(15)            

main()




