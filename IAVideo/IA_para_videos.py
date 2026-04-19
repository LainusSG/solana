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



@st.cache_resource
def load_yolo_model():
    return YOLO_Pred('./models/best.onnx', './models/data.yml')


yolo = load_yolo_model()


lock = threading.Lock()
img_container = {"img": None, "raw_img": None, "data": []}
stream_state = {"frame_index": 0, "last_detections": [], "inference_running": False}

DISPLAY_MAX_WIDTH = 1280
INFERENCE_MAX_WIDTH = 640
INFERENCE_INPUT_SIZE = 640
PROCESS_EVERY_N_FRAMES = 2
CAMERA_STARTUP_PASSTHROUGH_FRAMES = 8
LOCAL_RTC_CONFIGURATION = RTCConfiguration({"iceServers": []})
PREDICTED_FRAME_PATH = "imagenes/pred_img_obj.png"


def resize_frame(img, max_width):
    height, width = img.shape[:2]
    if width <= max_width:
        return img
    scale = max_width / width
    new_size = (int(width * scale), int(height * scale))
    return cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)


def scale_detections(detections, scale_x, scale_y):
    scaled = []
    for detection in detections:
        x, y, w, h = detection["box"]
        scaled.append(
            {
                **detection,
                "box": [
                    int(x * scale_x),
                    int(y * scale_y),
                    int(w * scale_x),
                    int(h * scale_y),
                ],
            }
        )
    return scaled


def serialize_detection_labels(detections):
    return [f'{item["class_name"]}: {int(item["confidence"] * 100)}%' for item in detections]


def run_inference_async(source_img, display_img, inference_img):
    try:
        detections = yolo.detect(inference_img, input_size=INFERENCE_INPUT_SIZE)
        if inference_img.shape[:2] != display_img.shape[:2]:
            detections = scale_detections(
                detections,
                display_img.shape[1] / inference_img.shape[1],
                display_img.shape[0] / inference_img.shape[0],
            )
        if detections:
            save_detections = detections
            if source_img.shape[:2] != display_img.shape[:2]:
                save_detections = scale_detections(
                    detections,
                    source_img.shape[1] / display_img.shape[1],
                    source_img.shape[0] / display_img.shape[0],
                )
            annotated_img = yolo.draw_detections(source_img, save_detections)
            cv2.imwrite(PREDICTED_FRAME_PATH, annotated_img)
        with lock:
            stream_state["last_detections"] = detections
    except cv2.error:
        with lock:
            stream_state["last_detections"] = []
    finally:
        with lock:
            stream_state["inference_running"] = False




def video_frame_callback(frame):
    source_img = frame.to_ndarray(format="bgr24")
    display_img = resize_frame(source_img, max_width=DISPLAY_MAX_WIDTH)
    inference_img = resize_frame(display_img, max_width=INFERENCE_MAX_WIDTH)

    with lock:
        stream_state["frame_index"] += 1
        if stream_state["frame_index"] <= CAMERA_STARTUP_PASSTHROUGH_FRAMES:
            img_container["img"] = display_img
            img_container["raw_img"] = source_img.copy()
            img_container["data"] = []
            return av.VideoFrame.from_ndarray(display_img, format="bgr24")

        should_run_inference = (
            stream_state["frame_index"] % PROCESS_EVERY_N_FRAMES == 1
            or (not stream_state["last_detections"] and not stream_state["inference_running"])
        )

        if should_run_inference and not stream_state["inference_running"]:
            stream_state["inference_running"] = True
            threading.Thread(
                target=run_inference_async,
                args=(source_img.copy(), display_img.copy(), inference_img.copy()),
                daemon=True,
            ).start()

        pred_img = yolo.draw_detections(display_img, stream_state["last_detections"])
        falla_detectada = serialize_detection_labels(stream_state["last_detections"])
        img_container["img"] = pred_img
        img_container["raw_img"] = source_img.copy()
        img_container["data"] = falla_detectada
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")



ctx = webrtc_streamer(
    key="example",
    video_frame_callback=video_frame_callback,
    rtc_configuration=LOCAL_RTC_CONFIGURATION,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1280},
            "height": {"ideal": 720},
            "frameRate": {"ideal": 24},
        },
        "audio": False,
    },
    async_processing=True,
    video_html_attrs={
        "autoPlay": True,
        "muted": True,
        "playsInline": True,
    },
)

fig_place = st.empty()
fig, ax = plt.subplots(1, 1)




def realizar_limpieza(valorfalla):
    valor2 =[]
    valor2_f=[]     
    total_fallas = []
    if len(valorfalla) > 0:
        for k in valorfalla:

            valor1 = k.split(':')
            try:
                valor3 = float(valor1[0])
                valor2.append(valor3)
                
        
            except:
                igual=False
                for kk in valor2_f:
                    if kk == valor1[0]:
                        igual=True
                if not igual:
                    valor2_f.append(valor1[0])
                
        nnn=0
        x=0
        for nn in valor2:
            nnn+=nn
            x+=1
        if x > 0:    
            calificacion = nnn/x
        else:
            calificacion = 0
        if len(valor2_f) > 0:
            for kkk in valor2_f:
                total_fallas.append([calificacion, kkk, 1])
        else:
            total_fallas.append([calificacion, 'No hay fallas', 0])
    else:
        total_fallas.append([0, 'No hay fallas', 0])
 
    return(total_fallas)







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
            total_fallas=[]
            valorfalla = []
            tamano = 0
            while ctx.state.playing:
                with lock:
                    img = img_container["img"]
                    raw_img = img_container["raw_img"]
                    for kk in img_container["data"]:
                        valor = kk.split(":")
                        if not valor[0] in total_fallas:
                            valorfalla.append(valor[0])
                            total_fallas= realizar_limpieza(valorfalla)
                            if len(total_fallas)>tamano:
                                tamano = len(total_fallas)
                                with conn.session as s:
                                    if len(total_fallas)<= 0:
                                        total_fallas. append([0,'No hay fallas',0])
                                    for [calificacion1, tipo_fallas1, fallas1] in total_fallas:
                                        import pyrebase

                                        ## configuraciones de la base de datos
                                        
                                        firebaseConfig = {
                                            "apiKey": "AIzaSyB3XiVjsPQMnlr4atYjU2xnL-NX9fk_2Mg",
                                            "authDomain": "solanaia.firebaseapp.com",
                                            "databaseURL": "https://solanaia-default-rtdb.firebaseio.com",
                                            "projectId": "solanaia",
                                            "storageBucket": "solanaia.appspot.com",
                                            "messagingSenderId": "781444992537",
                                            "appId": "1:781444992537:web:5986510634d48fc259e488",
                                            "measurementId": "G-Z1Q8XZ19SR"
                                            }


                                        firebase = pyrebase.initialize_app(firebaseConfig )
                                        ## declaracion de que funicion queremos usar, en este caso "storage" para almacenar ahi nuestras fotos dentro del bucket
                                        storage = firebase.storage()

                                        imgw= "imagenes/pred_img_obj.png"
                                        if raw_img is not None:
                                            cv2.imwrite(imgw, raw_img)

                                        
                                        

                                        today = datetime.datetime.now()
                                        today3 = today.strftime("%H:%M:%S")
                                        today2 = today.strftime("%d-%m-%Y")

                                        ## el estorage child es el nombre con el que guardaremos el archivo en la base de datos
                                        ## no uncluiur "/" en el nombre, ya que el programa lo reconocé como rutas y crea sub carpetas


                                        ## la funcion put sube la variable o el archivo que este contenido entre parentesis en este caso la foto
                                        ## que siempre cambiara en cada analisís
                                        #storage.child('IMAGENES/'+str(today2)+' - '+str(today3)).put(imgw)
                                        auth = firebase.auth()
                                        user = auth.sign_in_with_email_and_password(email='calidad@solana.mx', password='Calidad.2024*')
                                        url = storage.child('IMAGENES/'+str(today2)+' - '+str(today3)).get_url(user)  
                                        url2 = url.split("':")
                                        url3= url2[0]
                                        s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas, link) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas, :link );'),
                                            params=dict(fecha=Fecha, calificacion=calificacion1, obra=Obra, cliente=Cliente,  tipo_pieza=Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas=tipo_fallas1, fallas=fallas1, link=url3 )
                                                                    )
                                        s.commit()
                            


                if img is None:
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ax.cla()
                ax.hist(gray.ravel(), 256, [0, 256])
                fig_place.pyplot(fig)
    


                   

    


                

create_new_form()
