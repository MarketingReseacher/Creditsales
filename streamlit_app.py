import numpy as np
import pandas as pd
import streamlit as st


def Cov(Assets, WC, Dlc, Dltt, MV, Cogs):
    
    Size = (np.log(Assets + 1)) -  6.98
    Sum = Dlc + Dltt + MV
    if Assets == 0:
        Assets = 1
    if Sum == 0:
        Sum = 1
    Liquidity = (WC/Assets) - .29
    Leverage = ((Dlc + Dltt)/Sum) - .18
    Debt = ((Dlc + (1/2 * Dltt))/Assets) - .13
    Costs = (Cogs/Assets) - .76
    
    return Size, Liquidity, Leverage, Debt, Costs

st.write("### Operational Performance Estimator")

TC_1 = st.slider('Trade credit', min_value=0.00, max_value = 1.00, value = .16) 
TC = TC_1 - .16
PI_1 = st.number_input("Product risk incidents:", value = 1)
PI = PI_1 
BO_1 = st.slider('Buyer orientation', min_value= -1.00, max_value = 1.00, value = .16) 
BO = BO_1 - .16

Assets = st.number_input("Total assets, in million dollars:", value = 7000)
WC = st.number_input("Working capital, in million dollars:", 900)
Cogs = st.number_input("Costs of goods sold, in million dollars:", 5000)
Dlc = st.number_input("Debt in current liabilities, in million dollars:", 300)
Dltt = st.number_input("Long-term debt, in million dollars:", 1500)
MV = st.number_input("Market value, in million dollars:", 8600)
Concentration_1 = st.slider('Segment concentration', min_value= 0.00, max_value = 1.00, value = .16)
Concentration = Concentration_1 - .16
SG_1 = st.slider('Sales growth', min_value= -1.00, max_value = 1.00, value = .08)
SG = SG_1 - .08
ST_1 = st.slider('Sales turbulence', min_value= -1.00, max_value = 1.00, value = .04)
ST = ST_1 - .04
IG_1 = st.slider('Industry growth', min_value= -1.00, max_value = 1.00, value = .04)
IG = IG_1 - .04
IT_1 = st.slider('Industry turbulence', min_value= -1.00, max_value = 1.00, value = .06)
IT = IT_1 - .06

Size, Liquidity, Leverage, Debt, Costs = Cov(Assets, WC, Dlc, Dltt, MV, Cogs)

ROA = (-.11 * TC)  + (-.02 * PI) + (-1.67 * BO) + (.01 * Size) + (.02 * Liquidity) + (-.17 * Leverage) + (0.02 * Costs) + (.22 * Debt) + (-.03 * Concentration) + (.02 * SG) + (-.22 * ST) + (.002 * IG) + (.02 * IT)

Response = round(ROA, 2)
st.write("#### Operational Performance:", Response)

