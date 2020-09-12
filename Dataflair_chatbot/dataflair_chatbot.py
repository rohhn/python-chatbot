import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random

lemmatizer = WordNetLemmatizer()


model = load_model('dataflair-chatbot.h5')

intents = json.loads(open('data-flair/intents.json').read())
vocab = pickle.load(open('dataflair_vocab.pkl','rb'))
classes = pickle.load(open('dataflair_classes.pkl','rb'))

def cleanup_sentence(sentence):
    sw = nltk.word_tokenize(sentence)
    sw = [lemmatizer.lemmatize(word.lower()) for word in sw]
    
    return sw

def bagofwords(sentence, words, show_details = True):
    sentence_words = cleanup_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w==s:
                bag[i] = 1
                if show_details:
                    print('found in bag: %s' % w)
    return(np.array(bag))

def predict_class(sentence, model):
    bow = bagofwords(sentence,vocab,show_details=False)
    res = model.predict(np.array([bow]))[0]
    error_threshold = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse= True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]],'probability': str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_respone(text):
    ints = predict_class(text,model)
    res = getResponse(ints, intents)
    return res


while(True):
    input_text = input('enter text: ')
    print(chatbot_respone(input_text))