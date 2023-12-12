import numpy as np
import pandas as pd
import streamlit as st
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def change_label_style(label, font_size='12px', font_color='black', font_family='sans-serif'):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
    </script>
    """
    st.components.v1.html(html)

label = "My text here"
st.text_input(label)
change_label_style(label, '20px')

st.title("Brand Avoidance Likelihood")

user_input = st.text_input("Please enter the consumer's failure description:")

analyzer = SentimentIntensityAnalyzer()

def Comp(user_input):
    Neg = analyzer.polarity_scores(user_input).get('compound')
    return Neg

st.text("The likelihood that this consumer avoids your brand in the future is: Comp(user_input)")

