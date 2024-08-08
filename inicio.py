import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import base64





st.set_page_config(page_title="SolanaIA", page_icon="reportes/lluvia.ico", layout="wide")


# Pass the list of passwords directly to the 
# Hasher constructor and generate the hashes
# passwords_to_hash = ['fashion@123', 'increff@fashion']
# hashed_passwords = Hasher(passwords_to_hash).generate()

# print(hashed_passwords)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


col1, col2,col3 = st.columns((3))
with col1:
    st.write("")
with col2:
    st.image('reportes/TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
with col3:
    st.write("")


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

    
Hasher.hash_passwords(config['credentials'])
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)
name, authentication_status, username = authenticator.login()

bienvenida = st.Page(
    "bienvenida.py", title="Inicio", icon=":material/home:", default=True
)
IAImagenes = st.Page(
    "IAImagenes/IA_para_Imagenes.py", title="IA para Imagenes", icon=":material/search:"
)
Dashboard = st.Page(
    "reportes/dashboard.py", title="Dashboard", icon=":material/dashboard:"
)

IAVideo = st.Page(
    "IAVideo/IA_para_videos.py", title="IA para procesar videos", icon=":material/bug_report:"
)
About = st.Page(
    "About.py", title="Acerca de Nosotros", icon=":material/home:"
)

if st.session_state["authentication_status"]:
    authenticator.logout('Salir', 'sidebar', key='unique_key')

    if username == 'casho':
        st.markdown(f'<p style="display: block; text-align:center; font-size: 32px;color: #000;font-weight: bold;">Bienvenido {st.session_state["name"]} !!</p>', unsafe_allow_html=True)
        
        #st.title('Admin Casho')
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "Reportes": [Dashboard],
            "IAVideo": [IAVideo],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'solana':
        st.markdown(f'<p class="big-font">Bienvenido {st.session_state["name"]} !!</p>', unsafe_allow_html=True)
        #st.title('Usuario')
        pg = st.navigation(
        {
            "IAImagenes": [IAImagenes],
            "Reportes": [Dashboard],
            "IAVideo": [IAVideo],
        }
        )
        pg.run()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password es incorrecto')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor introduce tu username/password')




##################################################################################################################################################################
####################################################### bloque de estilos ########################################################################################
##################################################################################################################################################################

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.logo("reportes/LOGOS JUNTOS.png")

st.html("""
  <style>
    [alt=Logo] {
      height: 5rem;
    }
  </style>
        """)


##################################################################################################################################################################
####################################################### bloque de estilos ########################################################################################
##################################################################################################################################################################
