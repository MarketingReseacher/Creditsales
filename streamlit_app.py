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


st.write("## Temporal Features and Brand Avoidance Likelihood Estimator") 

Selected_tab = st.sidebar.selectbox("Select a tab", ["Temporal feature estimator", "Brand Avoidance Likelihood based on Relative Future Focus", 
                                                     "Brand Avoidance Likelihood based on Relative Future Focus and Covariates"])

st.write("##### User Input")

Gender = st.selectbox('Consumer\'s gender:', ["Female", "Male","Unknown", "Unspecified"])
Relation = st.selectbox('Whether the consumer was the primary victim:', ["Yes", "No"])

user_input = st.text_input("Brand failure incident description:")

PastDic = ['past', 'previously', 'previous', 'earlier', 'historically', 'formerly',  'history', 'before', 'prior', 'back', 
           'retroactively', 'priorly', 'hitherto', 'anteriorly', 'yesterday', 'already',  'precedingly', 'afore', 'fore', 'yesteryear', 'antecedently', 
           'was', 'were', 'wasnt', 'werent', 'been', 'hindsight', 'rearview', 'aforetime', 'heretofore', 'yore', 'ago', 'beforehand', 'since', 'then']


FutureDic = ['future', 'eventually', 'prospectively', 'henceforth', 'everytime', "everyday", "anytime", 'tomorrow', 'imminently',  'hereafter', 'hereon', 
             'henceforward', 'longrun', 'longterm', 'forthcoming', 'upcoming', 'oncoming', 'incoming', 'impending', foreseeable', 'will', 'shall', 'wont', 'might',  'may', 
             'aftertime', 'thereafter', 'potential', 'potentially', 'intermittently', 'successively', 'supposedly']

analyzer = SentimentIntensityAnalyzer()

           
def MyTense(t):
               
    Textclean = t.lower() 
               
    def ExpandContractions(text):
        Expanded = contractions.fix(text)
        return Expanded
           
    Textclean = ExpandContractions(Textclean)

    def RemoveNonAscii(text):
        return "".join(w for w in text if ord(w) < 128) 
    
    Textclean = RemoveNonAscii(Textclean)
               
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

    Response = round(Prob * 100, 2)
           
    return Response



Tenses = MyTense(user_input)
Future = Tenses['future']
Past = Tenses['past'] 

st.write("##### Results")

Length = len(user_input.split())

if Length == 0:
    st.write("You have not entered a failure incident description yet.")
else:
    FuturePR = round(Future/Length * 100, 2)
    PastPR = round(Past/Length * 100, 2) 
    st.write("Percentage of future-focused words in the description:", FuturePR, "%")
    st.write("Percentage of past-focused words in the description:", PastPR, "%")
    Relative = FuturePR - PastPR      
    st.write("Relative future focus of the description:", Relative, "%")
    Comp = round(analyzer.polarity_scores(user_input).get('compound'), 2)
    st.write("Compound sentiment score of the description:", Comp)
    Response = Resp(Relative, Comp, Gender, Relation)
    st.write("The likelihood that this consumer avoids the brand in the future:", Response, "%")














