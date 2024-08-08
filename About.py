import streamlit as st
import pandas as pd
import numpy as np


import streamlit as st


with open('style2.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.write('Sistema de Soldadura Versión. 1.1')
st.write('Copyright © 2023-2024, SMARTEST - El equipo de desarrollo del Sistema de Soldadura.')
st.write('')


st.subheader('LICENCIA')
st.write('''El uso de productos de software o hardware de SMARTEST se basa en la licencia de software y ciertos términos y condiciones para el producto al momento de su compra. La aceptación de esos términos es obligatoria para instalar o usar el producto. Consulta la licencia con tu proveedor o comunícate con nuestra área comercial ventas@smartest.mx.''')
st.write('')


st.subheader('MARCAS')
st.write('''El logotipo del Sistema de Soldadura y de SMARTEST son marcas registradas o marcas comerciales de SMARTEST en México.''')
st.write('')



st.subheader('POLÍTICAS Y AVISOS')
st.write('''Los avisos, términos y condiciones pertenecientes a software, hardware o datos de terceros se encuentran en https://www.smartest.mx/.''')
st.write('')


st.subheader('DERECHOS Y PERMISOS')
st.write('''La instalación y las adecuaciones del Sistema de Soldadura están limitadas a acciones de los técnicos de SMARTEST.''')
st.write('')


st.subheader('INTELIGENCIA ARTIFICIAL')
st.write('''El producto Sistema de Soldadura tiene inteligencia artificial ("IA"). Este es desarrollado por SMARTEST. La funcionalidad de la IA esta especificada en las características del producto o servicio. Las funciones de IA utilizan la información que el sistema recopila para mejorar los servicios que te proporcionamos o para mejorar la asistencia que te ofrecemos en relación con las operaciones del sistema.''')

st.write('')
st.subheader('El Sistema de Soldadura es creado por los SMARTEST.')