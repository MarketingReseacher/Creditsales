import numpy as np
import pandas as pd
import streamlit as st


def Cov(Assets, WC, Dlc, Dltt, MV, RDStock, SGA):
    
    Size = (np.log(Assets + 1)) -  7.07
    Sum = Dlc + Dltt + MV
    if Assets == 0:
        Assets = .05
    if Sum == 0:
        Sum = .05 
    Liquidity = (WC/Assets) - .30
    Leverage = ((Dlc + Dltt)/Sum) - .18
    Debt = (Dlc + (1/2 * Dltt)) - 805
    RD = (RDStock/Assets) - .17
    SI = (SGA/Assets) - .24
    
    return Size, Liquidity, Leverage, Debt, RD, SI

st.write("### ROA Estimator")
st.write("#### User Input")

TC_1 = st.slider('Credit sales', min_value=0.00, max_value = 1.00, value = .16) 
TC = TC_1 
PI_1 = st.number_input("Number of product issues:", value = 1)
PI = PI_1 - 1
Assets_1 = st.number_input("Total assets, in million dollars:", value = 7000)
Assets = Assets_1 - 7000
WC_1 = st.number_input("Working capital, in million dollars:", 900)
WC = WC_1 - 900
Dlc_1 = st.number_input("Debt in current liabilities, in million dollars:", 300)
Dlc = Dlc_1 - 300
Dltt_1 = st.number_input("Long-term debt, in million dollars:", 1500)
Dltt = Dltt_1 - 1500
MV_1 = st.number_input("Market value, in million dollars:", 8600)
MV = MV_1 - 8600
RDStock_1 = st.number_input("R&D stock, in million dollars:", value = 600)
RDStock = RDStock_1 - 600
SGA_1 = st.number_input("Selling, general, and administrative costs, in million dollars:", value = 800)
SGA = SGA_1 - 800
Concentration_1 = st.slider('Segment concentration', min_value= 0.00, max_value = 1.00, value = .15)
Concentration = Concentration_1 - .15
SG_1 = st.slider('Sales growth', min_value= -1.00, max_value = 1.00, value = .07)
SG = SG_1 - .07
ST_1 = st.slider('Sales turbulence', min_value= -1.00, max_value = 1.00, value = .04)
ST = ST_1 - .04
IG_1 = st.slider('Industry growth', min_value= -1.00, max_value = 1.00, value = .03)
IG = IG_1 - .03
IT_1 = st.slider('Industry turbulence', min_value= -1.00, max_value = 1.00, value = .06)
IT = IT_1 - .06

Size, Liquidity, Leverage, Debt, RD, SI = Cov(Assets_1, WC_1, Dlc_1, Dltt_1, MV_1, RDStock_1, SGA_1)

ROA = (-.92 * TC)  + (-.03 * PI) + (-.13 * PI * TC) + (-.03 * Size) + (-.01 * Liquidity) + (.03 * Leverage) + (.00 * Debt) + (-.05 * RD) + (-.05 * SI) + (-.04 * Concentration) + (.09 * SG) + (-.14 * ST) + (.002 * IG) + (.07 * IT)


Response = round(ROA, 2)
st.write("#### ROA:", Response)

