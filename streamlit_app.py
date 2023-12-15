import numpy as np
import pandas as pd
import streamlit as st
import nltk
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from nltk import word_tokenize
import contractions
from nltk.sentiment.vader import SentimentIntensityAnalyzer


st.write("## Brand Avoidance Likelihood Estimator") 

Gender = st.selectbox('Consumer\'s gender:', ["Female", "Male","Unknown", "Unspecified"])
Relation = st.selectbox('Whether the consumer was the primary victim:', ["Yes", "No"])

user_input = st.text_input("The failure incident description:")

PastDic = ['past', 'previously', 'previous', 'earlier', 'historically', 'formerly',  'history', 'before', 'prior', 'back', 
           'retroactively', 'priorly', 'hitherto', 'anteriorly', 'erstwhile', 'yesterday', 'already', 
           'precedingly', 'afore', 'fore', 'erewhile', 'yesteryear', 'precedently', 'antecedently', 
           'was', 'were', 'wasnt', 'werent', 'been', 'hindsight', 'rearview', 'aforetime', 'heretofore', 'foretime', 
           'foregoing', 'yore', 'ago', 'beforehand', 'since', 'then', 'temporary']


FutureDic = ['future', 'eventually', 'prospectively', 'henceforth', 'everytime', "everyday", "anytime", 'tomorrow',  
             'imminently',  'hereafter', 'hereon', 'henceforward', 
             'longrun', 'longterm', 'forthcoming', 'upcoming', 'oncoming', 'incoming', 'impending', 'foreseeable', 
             'will', 'shall', 'wont', 'might',  'may', 
             'aftertime', 'thereafter', 'potential', 'potentially', 'intermittently', 'successively', 'supposedly']

analyzer = SentimentIntensityAnalyzer()

           
def MyTense(t):
               
    Textclean = t.lower() 
               
    def ExpandContractions(text):
        Expanded = contractions.fix(text)
        return Expanded
           
    Textclean = ExpandContractions(Textclean)
               
    def POS(text):
               
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
                   
        past = []
        future = []
        previous = ""
        beforeprevious = ""
                   
        for item in tagged:
            if (item[0] in PastDic) or (item[1] in ["VBD", "VBN"]) or (item[1] == "VBG" and previous == "been" and beforeprevious == "had") or (item[1] == "VBG" and previous in ["was", "were", "wasnt", "werent"]) or (item[1] == "VBG" and previous == "not" and beforeprevious in ["was", "were", "wasnt", "werent"]):
                past.append(item[0])
            elif (item[0] in FutureDic) or (item[1] in ["VB", "VBZ", "VBP"] and previous in ["will", 'shall', 'wont', 'may', 'might', "would"]) or (item[1] in ["VB", "VBZ", "VBP"] and previous == "not" and beforeprevious in ["will", 'shall', 'wont', 'may', 'might']) or (item[1] in ["VB", "VBZ", "VBP"] and previous == "to" and beforeprevious == "going") or (item[1] == "VBG" and previous == "be" and beforeprevious in ["will", 'shall', 'wont', 'may', 'might', "not"]): 
                future.append(item[0])  
            else:
                pass
                       
            beforeprevious = previous 
            previous = item[0]

        Future = len(future)
        Past = len(past)

        response = {"future" : Future, "past": Past}
                   
        return response
           
    Tenses = POS(Textclean)
           
    return Tenses

def Resp(Rel, Com, G, R):
       
    if G == "Female":
        GenderCoeff = 0
    elif G == "Male":
        GenderCoeff = .02
    elif G == "Unknown":
        GenderCoeff = .21
    else:
        GenderCoeff = .18
            
    if R == "Yes":
        RelationCoeff =  -.05
    else:
        RelationCoeff = 0

    Cop = .02

    Answer = (-.19 * Rel) + GenderCoeff + RelationCoeff + (.01 * Com) + (1.14 * Cop) - 2.02

    Odds = np.exp(Answer)
    
    Prob = Odds/(1+Odds) 

    if T == "":
        Response = 0
    else:
        st.write("The odds of this consumer avoiding your brand in the future are:", round(Odds, 2))
        Response = round(Prob, 2) * 100
    return Response



Tenses = MyTense(user_input)
st.write(Tenses['future'])
Length = len(user_input.split())

