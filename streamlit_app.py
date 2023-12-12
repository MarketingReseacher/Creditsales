import numpy as np
import pandas as pd
import streamlit as st
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


st.title("Brand Avoidance Likelihood Estimator")

user_input = st.text_input("Please enter the consumer's failure description:")

analyzer = SentimentIntensityAnalyzer()

def Comp(user_input):
    Neg = analyzer.polarity_scores(user_input).get('compound')
    return Neg


Gender = st.selectbox('Gender', ["Male","Female","Unknown", "Unspecified"])
Relation = st.selectbox('Primary victim', ["Yes", "No"])


st.write("The likelihood that this consumer avoids your brand in the future is:", Comp(user_input))



