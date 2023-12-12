import numpy as np
import pandas as pd
import streamlit as st
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

st.title("Brand Avoidance Likelihood Estimator")

Gender = st.selectbox('Gender', ["Female", "Male","Unknown", "Unspecified"])
st.write("The consumer's gender is:", Gender)

Relation = st.selectbox('Primary victim', ["Yes", "No"])
st.write("The consumer is the primary victim:", Relation)

user_input = st.text_input("Please enter the consumer's failure description:")


def Resp(T, G, R):
    
    if T == "":
        Response = 0
    else:
        
        if G == Female:
            GenderCoeff = 0
        elif G == Male:
            GenderCoeff = .01
        elif G == Unknown:
            GenderCoeff = .20
        else:
            GenderCoeff = .16
            
        if R == Yes:
            RelationCoeff =  -.06
        else:
            RelationCoeff = 0

        analyzer = SentimentIntensityAnalyzer()
        Neg = analyzer.polarity_scores(T).get('compound') * 100

        Cop = .03

        Odds = ((-.21 * Neg) + GenderCoeff + RelationCoeff + (1.05 * Cop) - 1.48)
        Prob = (Odds/(1+Odds)) 
        Response = round(Prob, 2) * 100
        
    return Response
        
Response = Resp(user_input, Gender, Relation)

st.write("The likelihood that this consumer avoids your brand in the future is:", Response, "%")
