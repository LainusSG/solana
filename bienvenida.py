import streamlit as st
import pandas as pd
import numpy as np


import streamlit as st


with open('style2.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image( "reportes/ESTRUCTURAS SOLANA - 04 (1).png")

with col3:
    st.write(' ')


st.markdown('<p style="display: block; text-align:center; font-size: 82px;color: #000;font-weight: bold;">Bienvenido al</p>', unsafe_allow_html=True)
st.markdown('<p style="display: block; text-align:center; font-size: 82px;color: #000;font-weight: bold;">Sistema de Análisis de Soldadura</p>', unsafe_allow_html=True)


st.markdown('<p style="display: block; text-align:center; font-size: 35px;color: #000;">Para obtener información sobre avisos legales, de protección de datos</p>', unsafe_allow_html=True)
st.markdown('<p style="display: block; text-align:center; font-size: 35px;color: #000;">y desarrollo ir a "Acerca de"</p>', unsafe_allow_html=True)
st.markdown('<p style="display: block; text-align:center; font-size: 35px;color: #000;font-weight: bold;"> </p>', unsafe_allow_html=True)

st.markdown('<p style="display: block; text-align:center; font-size: 35px;color: #000;font-weight: bold;">Derechos Reservados © 2024 SMARTEST</p>', unsafe_allow_html=True)

