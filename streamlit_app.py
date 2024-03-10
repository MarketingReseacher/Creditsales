import numpy as np
import pandas as pd
import streamlit as st

def Cov(Assets, Ib, WC, AdStock, RDStock, Dlc, Dltt, MV, PPE, Retained, Roa, IRoa):
    
    Size = np.log(Assets + 1)
    if Assets == 0:
        Assets = .1
    if Dlc == 0:
        Dlc = .1
    if Dltt == 0:
        Dltt = .1 
    if MV == 0:
        MV = .1
    Profit = Ib/Assets
    Liquidity = WC/Assets
    Ad = AdStock/Assets
    RD = RDStock/Assets
    Leverage = (Dlc + Dltt)/(Dlc + Dltt + MV)
    CI = PPE/Assets
    RE = Retained/Assets
    RP = Roa - IRoa
    
    return Size, Profit, Liquidity, Ad, RD, Leverage, CI, RE, RP

Selected_tab = st.sidebar.selectbox("Select a tab", ["Credit sales predictor", "Bankruptcy risk predictor"], help = "Choose 'Credit sales predictor' if you want to predict the firm\'s credit sales based on the number of its product issues, buyer orientation, and other financial covariates. Choose 'Bankruptcy risk predictor' if you want to predict the firm\'s bankruptcy risk based on its credit sales, product issues, buyer orientation, and financial covariates")

if Selected_tab == "Credit sales predictor":
    st.write("#### Credit sales Predictor")
    st.write("##### User Input")

    PI = st.number_input("Number of product issues:", value = 1)
    BO = st.slider('Buyer orientation', min_value= -1.00, max_value = 1.00, value = 0.5)
    Assets = st.number_input("Assets, in dollars:", value = 7300)
    AdStock = st.number_input("Advertising stock, in million dollars:", value = 1000)
    RDStock = st.number_input("R&D stock, in million dollars:", value = 1000)
    Ib = st.number_input("Income before extraordinary items, in million dollars:", value = 100)
    WC = st.number_input("Working capital, in million dollars:", 2200)
    Dlc = st.number_input("Debt in current liabilities, in million dollars:", 350)
    Dltt = st.number_input("Long-term debt, in million dollars:", 1500)
    MV = st.number_input("Market value, in million dollars:", 8200)
    PPE = st.number_input("Propery, plant, and equipment, in million dollars:", 1400)
    Retained = st.number_input("Retained earnings, in million dollars:", 100)
    Roa = st.number_input("Roa, in million dollars:", 1)
    IRoa = st.number_input("Average industry ROA, in million dollars:", 0)
    Concentration = st.slider('Segment concentration', min_value= 0.00, max_value = 1.00, value = .14)
    SG = st.slider('Sales growth', min_value= -1.00, max_value = 1.00, value = .07)
    ST = st.slider('Sales turbulence', min_value= -1.00, max_value = 1.00, value = .04)
    IC = st.slider('Industry competition', min_value= 0.00, max_value = 1.00, value = .28)
    IG = st.slider('Industry growth', min_value= -1.00, max_value = 1.00, value = .03)
    IT = st.slider('Industry turbulence', min_value= -1.00, max_value = 1.00, value = .06)

    Size, Profit, Liquidity, Ad, RD, Leverage, CI, RE, RP = Cov(Assets, Ib, WC, AdStock, RDStock, Dlc, Dltt, MV, PPE, Retained, Roa, IRoa)

    Creditsales = (-0.022 * PI) + (0.108 * BO) + (0.098 * PI * BO) + (-0.042 * Ad) + (-0.001 * RD) + (-0.004 * Size) + (-0.041 * Profit) + (0.030 * Liquidity) + (0.006 * Leverage) + (-0.019 * CI) + (0.005 * RE) + (0.000 * RP) + (-0.009 * Concentration) + (0.008 * SG) + (0.006 * ST) + (-0.015 * IC) + (0.002 * IG) + (0.031 * IT)

    Response = round(Creditsales * 100, 2)
    st.write(" ##### Credit sales:", Response, "%")


elif Selected_tab == "Bankruptcy risk predictor":
    st.write("#### Bankruptcy risk Predictor")
    st.write("##### User Input")

    Creditsales = st.slider('Credit sales', min_value=0.00, max_value = 1.00, value = .04)
    PI = st.number_input("Number of product issues:", value = 1)
    BO = st.slider('Buyer orientation', min_value= -1.00, max_value = 1.00, value = 0.5)
    Assets = st.number_input("Assets, in dollars:", value = 7300)
    AdStock = st.number_input("Advertising stock, in million dollars:", value = 1000)
    RDStock = st.number_input("R&D stock, in million dollars:", value = 1000)
    Ib = st.number_input("Income before extraordinary items, in million dollars:", value = 100)
    WC = st.number_input("Working capital, in million dollars:", 2200)
    Dlc = st.number_input("Debt in current liabilities, in million dollars:", 350)
    Dltt = st.number_input("Long-term debt, in million dollars:", 1500)
    MV = st.number_input("Market value, in million dollars:", 8200)
    PPE = st.number_input("Propery, plant, and equipment, in million dollars:", 1400)
    Retained = st.number_input("Retained earnings, in million dollars:", 100)
    Roa = st.number_input("Roa, in million dollars:", 1)
    IRoa = st.number_input("Average industry ROA, in million dollars:", 0)
    Concentration = st.slider('Segment concentration', min_value= 0.00, max_value = 1.00, value = .14)
    SG = st.slider('Sales growth', min_value= -1.00, max_value = 1.00, value = .07)
    ST = st.slider('Sales turbulence', min_value= -1.00, max_value = 1.00, value = .04)
    IC = st.slider('Industry competition', min_value= 0.00, max_value = 1.00, value = .28)
    IG = st.slider('Industry growth', min_value= -1.00, max_value = 1.00, value = .03)
    IT = st.slider('Industry turbulence', min_value= -1.00, max_value = 1.00, value = .06)

    Size, Profit, Liquidity, Ad, RD, Leverage, CI, RE, RP = Cov(Assets, Ib, WC, AdStock, RDStock, Dlc, Dltt, MV, PPE, Retained, Roa, IRoa)

    Bankruptcyrisk = (23.597 * Creditsales)  + (-1.344 * PI) + (1.547 * BO) + (5.761 * PI * BO) + (17.652 * Ad) + (1.508 * RD) + (1.153 * Size) + (-2.950 * Profit) + (-1.285 * Liquidity) + (2.957 * Leverage) + (-1.685 * CI) + (-0.314 * RE) + (-0.003 * RP) + (-0.876 * Concentration) + (-2.756 * SG) + (3.485 * ST) + (-0.493 * IC) + (-0.507 * IG) + (-1.189 * IT)

    Response = round(Bankruptcyrisk, 2)
    st.write("##### Bankruptcy risk:", Response)


