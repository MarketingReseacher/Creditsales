import numpy as np
import pandas as pd
import streamlit as st
import nltk

st.title("Brand Avoidance Likelihood")

user_input = st.text_input("Enter failure description")

analyzer = SentimentIntensityAnalyzer()

def Comp(user_input):
    Neg = analyzer.polarity_scores(user_input).get('neg')
    return Neg


st.text(Comp(user_input))

