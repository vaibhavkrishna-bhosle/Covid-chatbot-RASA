import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from tensorflow.keras.models import load_model
model = load_model('save/chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json',encoding="utf8").read())
words = pickle.load(open('save/words.pkl','rb'))
classes = pickle.load(open('save/classes.pkl','rb'))
import requests, datetime
responses = requests.get("https://api.covid19india.org/data.json").json()

def get_state_data(state):
    if state == "india":
        state = "Total"
    for data in responses["statewise"]:
        if data["state"] == state.title():
            message = "Now Showing Cases For --> " + state.title() + "  \n" + "Active: " + data[
               "active"] + "  \n" + "Confirmed: " + data["confirmed"] + "  \n" + "Recovered: " + data[
                   "recovered"] + "  \n" + "Deaths: " + data["deaths"] + "  \n" + "Delta-Confirmed: " + data[
                       "deltaconfirmed"] + "  \n" + "Delta-Recovered: " + data[
                           "deltarecovered"] + "  \n" + "Delta-Deaths: " + data["deltadeaths"]
    return message

def get_date_count(date):
    for data in responses["cases_time_series"]:
        if data["dateymd"] == date:
            message = "Covid Cases on the date: " + date + "\nDaily Confirmed: " + data[
                "dailyconfirmed"] + "\nTotal Deceased: " + data["dailydeceased"] + "\nTotal Recovered" + data[
                    "dailyrecovered"] + "\nTotal Confirmed: " + data["totalconfirmed"] + "\nTotal Deceased: " + data[
                        "totaldeceased"] + "\nTotal Recovered: " + data["totalrecovered"]
    return message

def get_month_count(date):
    dailyconfirmed = 0
    dailydeceased = 0
    dailyrecovered = 0
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    for data in responses["cases_time_series"]:
            if data["dateymd"][:7] == date:
                    dailyconfirmed += int(data['dailyconfirmed'])
                    dailydeceased += int(data['dailydeceased'])
                    dailyrecovered += int(data['dailyrecovered'])
                    message = "Total cases in the month " + months[int(data["dateymd"][5:7])-1] + " " + str(int(data["dateymd"][:4])) + " is\nTotal Confirmed: " + str(dailyconfirmed) +"\nTotal Deceased: " + str(dailydeceased) + "\nTotal Recovered: " + str(dailyrecovered)
    return message

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    state_list = ["Total","Andaman and Nicobar Islands","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","State Unassigned","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
    format = "%Y-%m-%d"
    date_flag = 0
    msg = msg.lower()
    try:
        datetime.datetime.strptime(msg, format)
        date_flag = 1
    except ValueError:
        date_flag = 0
    if date_flag == 1:
        print(msg)
        message = get_date_count(msg)
        return message
    elif msg == "corona tracker":
        return "Enter State Name:"
    elif msg.title() in state_list:
        message = get_state_data(msg)
        return message
    elif msg == "corona counter":
        return "Enter date in format yyyy-mm-dd"
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    if ints[0]['intent'] == 'month_cal':
        return get_month_count(msg)

    return res+"\n\nwith accuracy "+ints[0]["probability"]