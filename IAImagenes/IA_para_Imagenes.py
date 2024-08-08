import streamlit as st
from yolo_prediccion import YOLO_Pred
from PIL import Image
import numpy as np
import datetime

#st.set_page_config(page_title="Detección calificación de soldadura de Imagen",
#                   layout="wide",
#                   page_icon="./imagenes/busquedaIA.jpg")


fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")

obra = title = st.text_input("Obra", "")

Pieza = title = st.text_input("Tipo de Pieza", "")

Categoria = title = st.text_input("Categoría", "")

Soldadura = title = st.text_input("Tipo de Soldadura", "")






st.title('Por favor sube una imagen para hacer detección/calificación')

with st.spinner('Por favor, espera que tu modelo esta cargando'):   
    yolo = YOLO_Pred(onnx_model='./models/best.onnx',
                    data_yaml='./models/data.yml')
    st.balloons()

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
                st.write('Pushaste el botón')
                arreglo_imagen = np.array(imagen_obj)
                pred_img = yolo.predicciones(arreglo_imagen)
                pred_img_obj = Image.fromarray(pred_img)
                prediccion = True

    if prediccion:
        st.subheader(" Imagen analizada")
        st.caption("Detección de objetos con la IA")
        st.image(pred_img_obj)

