import numpy as np
import pandas as pd
import streamlit as st
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


st.title("Brand Avoidance Likelihood Estimator")

user_input = st.text_input("Please enter the consumer's failure description:")

Gender = st.selectbox('Gender', ["Female", "Male","Unknown", "Unspecified"])
Relation = st.selectbox('Primary victim', ["Yes", "No"])

def Resp(Text, Gender, Relation):
    if Gender == "Female":
        GenderCoeff = 0
    elif Gender == "Male":
        GenderCoeff = .0067003
    elif Gender == "Unknown":
        GenderCoeff = .1997189
    else:
        GenderCoeff = .1570801
    if Relation == "Yes":
        RelationCoeff =  -.0597732
    else:
        RelationCoeff = 0

    analyzer = SentimentIntensityAnalyzer()
    Neg = analyzer.polarity_scores(Text).get('compound') * 100

    Cop = .0288489

    Response = ((-.2098055 * Neg) + GenderCoeff + RelationCoeff + (1.053751 * Cop) - 1.477298) * 100
    
    return Response
    
    

Response = Resp(user_input, Gender, Relation)

st.write("The likelihood that this consumer avoids your brand in the future is:", Response, "%")
