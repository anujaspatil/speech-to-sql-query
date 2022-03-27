# -*- coding: utf-8 -*-
import nltk

from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
import random
lemmatizer = WordNetLemmatizer()

from keras.models import Sequential
from keras.layers import Dense , Activation , Dropout
from tensorflow.keras.optimizers import SGD

words = []
classes = []
documents = []
ignore_words = ['?' , '!']
data_file = open('trial dataset.json', encoding='utf-8').read()
intents = json.loads(data_file)

intents

# nltk.download('punkt')

for intent in intents['intents']:
  for pattern in intent['patterns']:
    w = nltk.word_tokenize(pattern)
    words.extend(w)
    documents.append((w,intent['tag']))
    if intent['tag'] not in classes:
      classes.append(intent['tag'])

documents

# nltk.download('wordnet')

wmanaberds = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
print(len(documents),"documents")
print(len(classes),"classes",classes)
print(len(words), "unique lemmatized words", words)

pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

training = []
output_empty = [0]*len(classes)
for doc in documents:
  bag = []
  pattern_words = doc[0]
  pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
  for w in words:
    bag.append(1) if w in pattern_words else bag.append(0)
  output_row = list(output_empty)
  output_row[classes.index(doc[1])] = 1
  training.append([bag,output_row])
random.shuffle(training)
training = np.array(training)
train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()
model.add(Dense(128 , input_shape = (len(train_x[0]),),activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64 , activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))
sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9 , nesterov = True)
model.compile(loss = 'categorical_crossentropy', optimizer = sgd,metrics = ['accuracy'])

hist = model.fit(np.array(train_x),np.array(train_y),epochs = 200,batch_size=5,verbose=1)

for doc in documents:
  print(doc[0])

model.save('chatbot_model.h5', hist)
# !pip install SpeachRecognition

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('trial dataset.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


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
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def where_statement(msg_where,columns):
   if len(msg_where) == 0:
     return("")
   else:
      stop_words = ["is","to"]
      for i in stop_words:
        while(i in msg_where):
          msg_where.remove(i)
      msg_where = [sub.replace('equals', 'equal') for sub in msg_where]
      operators = ["greater than or equal","less than or equal","greater than","less than","equal"]
      str1 = " "
      msgwhere = str1.join(msg_where)
      for i in operators:
        while(i in msgwhere):
          if (i == "greater than or equal"):
            msgwhere = msgwhere.replace(i,">=")
          elif (i == "less than or equal"):
              msgwhere = msgwhere.replace(i,"<=")
          elif (i == "greater than"):
              msgwhere = msgwhere.replace(i,">")
          elif (i == "less than"):
              msgwhere = msgwhere.replace(i,"<")
          elif (i == "equal"):
              msgwhere = msgwhere.replace(i,"=")
      msg_where = list(msgwhere.split(" "))

      operator_sign = [">=","<=",">","<","="]
      for q in range(len(msg_where)):
        if msg_where[q] in operator_sign:
          if (msg_where[q+1].isnumeric()):
            pass
          else:
            msg_where[q+1] = '"'+msg_where[q+1]+'"' 

      ans_where = " "
      ans_where = ans_where.join(msg_where)
      ans_where = " where "+ans_where
      return(ans_where)

# Table_name = ["final","result"]
# columns = ["department","ID","name","score","rollno","marks"]
# columns_present = []
# table_present = []
import webbrowser as wb
from time import ctime
import time
import os
import random

from nltk.tokenize import word_tokenize
from keyword import kwlist

time.sleep(1)

# msg = input()
# print("User:",msg)
# msg = msg.split()

# for i in range(len(msg)):
#   if msg[i] in Table_name:
#     msg[i] = "<table_name>"
# for j in range(len(msg)):
#   if msg[j] in columns:
#     columns_present.append(msg[j])
#     msg[j] = "<column_1>"
# query = " "
# query = query.join(msg)
# ans = chatbot_response(query)
# ans = ans.replace("<table_name>",Table_name[0])
# for i in columns_present:
#   ans = ans.replace("<column_1>",i,1)

# print("query predicted: ",ans)