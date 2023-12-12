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
        GenderCoeff = 1
    elif Gender == "Male":
        GenderCoeff = .0652719
    elif Gender == "Unknown":
        GenderCoeff = .277797
    else:
        GenderCoeff = .2617218
    if Relation == "Yes":
        RelationCoeff =  -.0689343
    else:
        RelationCoeff = 1

    analyzer = SentimentIntensityAnalyzer()
    Neg = analyzer.polarity_scores(Text).get('compound')

    Response = -.19 * Neg + GenderCoeff + RelationCoeff   
    
    return Response
    
    

Response = Resp(user_input, Gender, Relation)

st.write("The likelihood that this consumer avoids your brand in the future is:", Response)



