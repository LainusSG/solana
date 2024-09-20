import streamlit as st
from yolo_prediccion import YOLO_Pred
from PIL import Image
import numpy as np
import datetime
from sqlalchemy import text



















#st.set_page_config(page_title="Detección calificación de soldadura de Imagen",
#                   layout="wide",
#                   page_icon="./imagenes/busquedaIA.jpg")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown(f'<p style="display: block; text-align:right; font-size: 24px;  margin-top:-2rem;  color: #000;font-weight: bold;"> Usuario: {st.session_state["name"]}</p>', unsafe_allow_html=True)
col1, col2,col3 = st.columns((3))
with col1:
    st.write("")
with col2:
    st.image('reportes/TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
with col3:
    st.write("")

# ##################################  OBTENER VALORES DE LA IA #######################################


st.title('Por favor sube una imagen para hacer detección/calificación')

with st.spinner('Por favor, espera que tu modelo esta cargando'):   
    yolo = YOLO_Pred(onnx_model='./models/best.onnx',
                    data_yaml='./models/data.yml')
    
num = 0
#Subir imagen
def subir_imagen():
    archivo_imagen = st.file_uploader(label=":orange[Subir Imagen]")
    if archivo_imagen is not None:
        size_mb = archivo_imagen.size/(1024**2)
        detalles_archivo = {
            "filename": archivo_imagen.name,
            "filetype": archivo_imagen.type,
            "filesize": "{:,.2f} MB".format(size_mb)}
        #st.json(detalles_archivo)

        # Validando Archivo

        if detalles_archivo['filetype'] in ('image/png', 'image/jpeg'):
            st.success('Tipos de Archivos de IMAGEN Válidos (png o jpeg)')
            return {"archivo": archivo_imagen, "detalles": detalles_archivo}

        else:
            st.error('Tipo de archivo de imagen inválido')
            st.error('Subir solamente png, jpg, jpeg')
            return None
valorfalla=[]

object = subir_imagen()
if object:
    prediccion = False
    imagen_obj = Image.open(object['archivo'])

    col1, col2 = st.columns(2)

    with col1:
        st.info('Vista previa de la imagen')
        st.image(imagen_obj)
    with col2:
        st.subheader('Checa abajo los detalles del archivo')
        st.json(object['detalles'])
        boton = st.button('Realizar revisión con la IA')
        if boton:
            with st.spinner("""
                    Detectando fallas de soldadura en la imagen. Por favor, paciencia
                            """):
                st.write('Presionaste el botón')
                arreglo_imagen = np.array(imagen_obj)
                [pred_img, valorfalla] = yolo.predicciones(arreglo_imagen)
                pred_img_obj = Image.fromarray(pred_img)
                prediccion = True

    if prediccion:
        st.subheader(" Imagen analizada")
        st.caption("Detección de objetos con la IA")
        st.image(pred_img_obj)
        

        ### comienzo del archivo de subida 
        import pyrebase

        ## configuraciones de la base de datos
        firebaseConfig = {
            "apiKey": "AIzaSyCfThEEfRDrrxu-HI-aHdYf2LIrL4wDc8I",
            "authDomain": "soldaduraia.firebaseapp.com",
            "databaseURL": "https://console.firebase.google.com/u/0/project/soldaduraia/database/soldaduraia-default-rtdb/data/~2F?hl=en-419",
            "projectId": "soldaduraia",
            "storageBucket": "soldaduraia.appspot.com",
            "messagingSenderId": "555516242506",
            "appId": "1:555516242506:web:83e25c3add2f37773914b3",
            "measurementId": "G-MVY7HV0Y5Y"
            }

        firebase = pyrebase.initialize_app(firebaseConfig )
        ## declaracion de que funicion queremos usar, en este caso "storage" para almacenar ahi nuestras fotos dentro del bucket
        storage = firebase.storage()


        ## aquí declare la imagen con un nombre arbitrario, lo remplazare con los datos del reporte
        ## esá imagen siempre se guardará con el mismo nombre del archivo para remplazar el archivo existente
        ## pero en la base de datos tomara el nombre que le asigne, en este caso el de la fecha
        pred_img_obj.save("imagenes/pred_img_obj.png")
        imgw= "imagenes/pred_img_obj.png"

        
        

        today = datetime.datetime.now()
        today3 = today.strftime("%H:%M:%S")
        today2 = today.strftime("%d-%m-%Y")

        ## el estorage child es el nombre con el que guardaremos el archivo en la base de datos
        ## no uncluiur "/" en el nombre, ya que el programa lo reconocé como rutas y crea sub carpetas


        ## la funcion put sube la variable o el archivo que este contenido entre parentesis en este caso la foto
        ## que siempre cambiara en cada analisís
        storage.child(str(today2)+' - '+str(today3)).put(imgw)




