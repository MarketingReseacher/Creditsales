import numpy as np
import pandas as pd
import streamlit as st
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

st.title("Brand Avoidance Likelihood Estimator")

Gender = st.selectbox('Consumr's gender', ["Female", "Male","Unknown", "Unspecified"])
Relation = st.selectbox('Whether the consumer was the primary victim', ["Yes", "No"])

user_input = st.text_input("Please enter the failure incident description:")


def Resp(T, G, R): 
    if G == "Female":
        GenderCoeff = 0
    elif G == "Male":
        GenderCoeff = .01
    elif G == "Unknown":
        GenderCoeff = .20
    else:
        GenderCoeff = .16
            
    if R == "Yes":
        RelationCoeff =  -.06
    else:
        RelationCoeff = 0

    analyzer = SentimentIntensityAnalyzer()
    
    Neg = analyzer.polarity_scores(T).get('compound')

    Cop = .03

    Answer = (-5.6 * Neg) + GenderCoeff + RelationCoeff + (1.05 * Cop) - .08

    Odds = np.exp(Answer)

    st.write("The odds of this consumer avoiding your brand in the future are:", round(Odds, 2))
    
    Prob = Odds/(1+Odds) 

    if T == "":
        Response = 0
    else:
        Response = round(Prob, 2) * 100
        
    return Response

Response = Resp(user_input, Gender, Relation)

st.write("The likelihood that this consumer avoids your brand in the future is:", Response, "%")
