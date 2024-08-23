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



################################################## Conexion a la base de dato ################################################################################







Fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")

Obra = st.text_input("Obra", "")

Cliente = st.text_input("Cliente", "")

Tipo_Pieza = st.text_input("Tipo de Pieza", "")

Pieza = st.text_input("Pieza", "")

Categoria = st.text_input("Categoría", "")

Tipo_soldadura = st.text_input("Tipo de Soldadura", "")

conn = st.connection("postgresql", type="sql")

if st.button("summit"):
    with conn.session as s:
    # soldadura = {Fecha, Obra, Cliente, Tipo_Pieza, Pieza, Categoria, Tipo_soldadura}


        s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas );'),
            params=dict(fecha=Fecha, calificacion ='10', obra=Obra, cliente=Cliente,  tipo_pieza = Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas='tope', fallas= 1 )
            )
        s.commit()






################################################## Conexion a la base de dato ################################################################################







st.title('Por favor sube una imagen para hacer detección/calificación')

with st.spinner('Por favor, espera que tu modelo esta cargando'):   
    yolo = YOLO_Pred(onnx_model='./models/best.onnx',
                    data_yaml='./models/data.yml')
    

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
                st.write('Pushaste el botón')
                arreglo_imagen = np.array(imagen_obj)
                [pred_img, valorfalla] = yolo.predicciones(arreglo_imagen)
                pred_img_obj = Image.fromarray(pred_img)
                prediccion = True

    if prediccion:
        st.subheader(" Imagen analizada")
        st.caption("Detección de objetos con la IA")
        st.image(pred_img_obj)



st.write(valorfalla)
