import os
import nltk
from tqdm import tqdm
import ast

class cornelldata:
    
    movie_lines_path = "/Users/rohan/Desktop/projects/python-chatbot/movie_lines.txt"
    movie_conversations_path = "/Users/rohan/Desktop/projects/python-chatbot/movie_conversations.txt"
    movie_conversation_fields = ['char1ID', 'char2ID', 'movieID', 'utterances']
    movie_lines_fields = ['lineId', 'charId', 'movieId', 'charname', 'text']
    
    def splitConversations(max_len=20, fast_preprocessing=True):
        conversations = getconv()
        data = []
        for i, conversation in enumerate(tqdm(conversations)):
            lines = conversation['lines']
            for i in range(len(lines) - 1):
                request = lines[i]
                reply = lines[i + 1]
                if 0 < len(request) <= max_len and 0 < len(reply) <= max_len:
                    data += [(request, reply)]
        return data
    
    def getlines():
        with open(movie_lines_path, 'r', encoding='iso-8859-1') as f:
            lines = {}
            for line in f:
                values = line.split(' +++$+++ ')
                lineobj = {}
                for i, field in enumerate(movie_lines_fields):
                    lineobj[field] = values[i]
                    #lineobj['id'] = int(re.sub('L','',lineobj['lineId']))
                lines[lineobj['lineId']] = lineobj
        return(lines)
    
    def getconv():
        lines = getlines()
        with open(movie_conversations_path, 'r', encoding='iso-8859-1') as f:
            conversations = []
            for line in f:
                values = line.split(' +++$+++ ')
                #print(len(values))
                lineobj = {}
                for i, field in enumerate(movie_conversation_fields):
                    lineobj[field] = values[i]
                lineIds = ast.literal_eval(lineobj["utter"])
                lineobj['lines'] = []
                for lineid in lineIds:
                    lineobj['lines'].append(lines[lineid]['text'])
                conversations.append(lineobj)
        return conversations