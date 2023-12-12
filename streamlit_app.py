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


def Resp(Text, Gender, Relation):
    if Text == "":
        Response = 0
    else:
        if Gender == "Female":
            GenderCoeff = 0
        elif Gender == "Male":
            GenderCoeff = .01
        elif Gender == "Unknown":
            GenderCoeff = .20
        else:
            GenderCoeff = .16
            
        if Relation == "Yes":
            RelationCoeff =  -.06
        else:
            RelationCoeff = 0

        analyzer = SentimentIntensityAnalyzer()
        Neg = analyzer.polarity_scores(Text).get('compound') * 100

        Cop = .0288489

        Odds = ((-.21 * Neg) + GenderCoeff + RelationCoeff + (1.053751 * Cop) - 1.48)
        Prob = (Odds/(1+Odds)) 
        Response = round(Prob, 2) * 100
    return Response
        
Response = Resp(user_input, Gender, Relation)

st.write("The likelihood that this consumer avoids your brand in the future is:", Response, "%")
