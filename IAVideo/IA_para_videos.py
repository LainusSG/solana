import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
from yolo_prediccion import YOLO_Pred
import datetime
import threading
from matplotlib import pyplot as plt

import cv2
from sqlalchemy import text


st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown(f'<p style="display: block; text-align:right; font-size: 24px;  margin-top:-2rem;  color: #000;font-weight: bold;"> Usuario: {st.session_state["name"]}</p>', unsafe_allow_html=True)
col1, col2,col3 = st.columns((3))
with col1:
    st.write("")
with col2:
    st.image('reportes/TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
with col3:
    st.write("")



yolo = YOLO_Pred('./models/best.onnx',
                  './models/data.yml')


lock = threading.Lock()
img_container = {"img": None}
total_fallas=[]




def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        #flipped = img[::-1,:,:]
        [pred_img, falla_detectada] = yolo.predicciones(img)

        total_fallas.append(falla_detectada)
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")

st.write(total_fallas)

ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback, rtc_configuration= {"iceServers": [{"urls":["stun:stun1.l.google.com:19302"]}]}, media_stream_constraints={"video":True, "audio": False})

fig_place = st.empty()
fig, ax = plt.subplots(1, 1)

while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ax.cla()
    ax.hist(gray.ravel(), 256, [0, 256])
    fig_place.pyplot(fig)

if len(total_fallas) > 0:
    st.write(total_fallas)
else:
    st.write('No se ha detectado falla')


conn = st.connection("postgresql", type="sql")

def create_new_form():
    with st.form("myform", clear_on_submit=True):
        Fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")

        Obra = st.text_input("Obra", "")

        Cliente = st.text_input("Cliente", "")

        Tipo_Pieza = st.text_input("Tipo de Pieza", "")

        Pieza = st.text_input("Pieza", "")

        Categoria = st.text_input("Categoría", "")

        Tipo_soldadura = st.text_input("Tipo de Soldadura", "")
        submit = st.form_submit_button(label="Submit")
        if submit:
            with conn.session as s:
                if len(total_fallas)<= 0:
                    total_fallas. append([0,'No hay fallas',0])
                for [calificacion1, tipo_fallas1, fallas1] in total_fallas:
                    s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas );'),
                           params=dict(fecha=Fecha, calificacion=calificacion1, obra=Obra, cliente=Cliente,  tipo_pieza=Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas=tipo_fallas1, fallas=fallas1 )
                                                )
                    s.commit()
                    

        st.write(total_fallas)
    


                

create_new_form()