import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from fpdf import FPDF
import base64
import datetime

import plotly.figure_factory as ff
import time 
warnings.filterwarnings('ignore')

today = datetime.datetime.now()
today2 = today.strftime("%d/%m/%Y")



st.set_page_config(page_title="Solana.IA", page_icon=":large_blue_diamond:",layout="wide")

st.markdown("""
<style>.element-container:has(#button-after) + 
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Koulen&family=Lato&family=Nunito&family=Playfair+Display:ital@1&family=Prata&family=Raleway:ital,wght@1,100&family=Roboto&family=Roboto+Condensed&family=Teko&display=swap')
button {
padding: 10px 30px;

 }
 
 button:hover {
     
    transition : 1000ms;
    padding: 10px 30px;
    transform : translateY(-0px);
    background-color: #fff;
    color: black;
    border: solid 2px #FF8000;
}</style>""", unsafe_allow_html=True)





def sidebar_bg(side_bg):

   side_bg_ext = 'jpeg'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

side_bg = 'photo-1507497806295-753c4108560c-5.jpeg'
sidebar_bg(side_bg)






col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image('TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


with col3:
    st.write(' ')


# fl = st.file_uploader(":file_folder: Subir Archivo!",type=(["csv","txt","xlsx","xls"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_csv(filename, encoding = "ISO-8859-1")
# else:
    os.chdir(r"/Users/casho/Documents/SMARTEST/Proyectos/CalidadSoldadura/soldadura/DashboardIA")
    df = pd.read_csv("Graficas.csv", encoding = "ISO-8859-1")


    
########################################################################################   

st.sidebar.header("Choose your filter: ")    

st.logo("LOGOS JUNTOS.png")


st.html("""
  <style>
    [alt=Logo] {
      height: 5rem;
    }
  </style>
        """)
########################################################################################   
    
col1, col2 = st.columns((2))
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Getting the min and max date 
startDate = pd.to_datetime(df["Fecha"]).min()
endDate = pd.to_datetime(df["Fecha"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Fecha de Inicio", startDate))
    today3 = date1.strftime("%d/%m/%Y")

with col2:
    date2 = pd.to_datetime(st.date_input("Fecha Final", endDate))
    today4 = date2.strftime("%d/%m/%Y")

df = df[(df["Fecha"] >= date1) & (df["Fecha"] <= date2)].copy()

########################################################################################   

col1, col2, col3 = st.columns((3))


# Create for Obra

with col1:
    calificacion = st.multiselect("Elige una Obra", df["Obra"].unique())
    if not calificacion:
        df2 = df.copy()
    else:
        df2 = df[df["Obra"].isin(calificacion)]
        
    Obra =calificacion
# Create for Tipo de Fallas
with col2:
    Tipo_de_Fallas = st.multiselect("Elige una Falla", df2["Tipo de Fallas"].unique())
    if not Tipo_de_Fallas:
        df3 = df2.copy()
    else:
        df3 = df2[df2["Tipo de Fallas"].isin(Tipo_de_Fallas)]

# Create for Tipo de Pieza
with col3:
    Tipo_de_Pieza = st.multiselect("Elige un Material",df3["Tipo de Pieza"].unique())


# Filter the data based on Calificacion, Tipo de Fallas and Tipo de Pieza

if not calificacion and not Tipo_de_Fallas and not Tipo_de_Pieza:
    filtered_df = df
elif not Tipo_de_Fallas and not Tipo_de_Pieza:
    filtered_df = df[df["Obra"].isin(calificacion)]
elif not calificacion and not Tipo_de_Pieza:
    filtered_df = df[df["Tipo de Fallas"].isin(Tipo_de_Fallas)]
elif Tipo_de_Fallas and Tipo_de_Pieza:
    filtered_df = df3[df["Tipo de Fallas"].isin(Tipo_de_Fallas) & df3["Tipo de Pieza"].isin(Tipo_de_Pieza)]
elif calificacion and Tipo_de_Pieza:
    filtered_df = df3[df["Obra"].isin(calificacion) & df3["Tipo de Pieza"].isin(Tipo_de_Pieza)]
elif calificacion and Tipo_de_Fallas:
    filtered_df = df3[df["Obra"].isin(calificacion) & df3["Tipo de Fallas"].isin(Tipo_de_Fallas)]
elif Tipo_de_Pieza:
    filtered_df = df3[df3["Tipo de Pieza"].isin(Tipo_de_Pieza)]
else:
    filtered_df = df3[df3["Obra"].isin(calificacion) & df3["Tipo de Fallas"].isin(Tipo_de_Fallas) & df3["Tipo de Pieza"].isin(Tipo_de_Pieza)]

category_df = filtered_df.groupby(by = ["Tipo de Pieza"], as_index = False)["Fallas"].sum()

category2_df = filtered_df.groupby(by = ["Obra"], as_index = False)["Fallas"].sum()

with st.expander("Fallas en Obras"):
    fig12 = px.bar(category2_df, x = "Obra", y = "Fallas", text = [x for x in category2_df["Fallas"]],
                    template ="ggplot2")
    st.plotly_chart(fig12,use_container_width=True, height = 200)
    
col1, col2= st.columns((2))


with col1:
    st.subheader("Fallas por Pieza")
    fig1 = px.bar(category_df, x = "Tipo de Pieza", y = "Fallas", text = [x for x in category_df["Fallas"]],
                 template ="ggplot2")
    st.plotly_chart(fig1,use_container_width=True, height = 200)

with col2:
    st.subheader("Fallas por Tipo de Soldadura")
    fig2 = px.pie(filtered_df, values = "Fallas", names = "Tipo de Soldadura", hole = 0.5, template ="presentation")
    fig2.update_traces(text = filtered_df["Categoria"], textposition = "outside")
    st.plotly_chart(fig2,use_container_width=True)

# Create a treem based on Region, category, sub-Category


chart1, chart2 = st.columns((2))
with chart1:
    st.subheader("Fallas por Pieza")
    fig3 = px.pie(filtered_df, values = "Fallas", names = "Tipo de Pieza", template = "plotly_white")
    fig3.update_traces(text = filtered_df["Tipo de Pieza"], textposition = "inside")
    st.plotly_chart(fig3,use_container_width=True)

with chart2:
    st.subheader("Fallas por Tipo de Soldadura")
    fig4 = px.pie(filtered_df, values = "Fallas", names = "Tipo de Soldadura", template = "gridon")
    fig4.update_traces(text = filtered_df["Tipo de Fallas"], textposition = "inside")
    st.plotly_chart(fig4,use_container_width=True)

########################################################################################   
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Fallas por PIeza"):
        st.write(category_df.style.background_gradient(cmap="Oranges"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Descargar", data = csv, file_name = "Tipo de Pieza.csv", mime = "text/csv",
                            help = 'Haz click para descargar la información')
        
        
        
    
with cl2:
    with st.expander("Fallas por Tipo de Soldadura"):
        calificacion = filtered_df.groupby(by = "Categoria", as_index = False)["Fallas"].sum()
        st.write(calificacion.style.background_gradient(cmap="Oranges"))
        csv = calificacion.to_csv(index = False).encode('utf-8')
        st.download_button("Descargar", data = csv, file_name = "Categoria.csv", mime = "text/csv",
                        help = 'Haz click para descargar la información')
        
        





col1, col2 = st.columns((2))

########################################################################################           
with col1:
    filtered_df["Año"] = filtered_df["Fecha"].dt.to_period("Y")
    st.subheader('Fallas por Año')

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Año"].dt.strftime("%Y : %b"))["Fallas"].sum()).reset_index()
    fig5 = px.line(linechart, x = "Año", y="Fallas", labels = {"Fallas": "Cantidad"},height=500, width = 1000,template="ggplot2")
    st.plotly_chart(fig5,use_container_width=True)

    with st.expander("Fallas Por Año"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Año.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')



########################################################################################           
with col2:
    filtered_df["Mes"] = filtered_df["Fecha"].dt.to_period("M")
    st.subheader('Fallas por Mes')

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Mes"].dt.strftime("%Y : %b"))["Fallas"].sum()).reset_index()
    fig6 = px.line(linechart, x = "Mes", y="Fallas", labels = {"Fallas": "Cantidad"},height=500, width = 1000,template="ggplot2")
    st.plotly_chart(fig6,use_container_width=True)

    with st.expander("Fallas Por Mes"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Mes.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')


########################################################################################   
st.subheader("Fallas")
fig7 = px.treemap(filtered_df, path = ["Categoria","Tipo de Fallas","Tipo de Pieza", "Calificacion"], values = "Fallas",hover_data = ["Fallas"],template="presentation")
fig7.update_layout(width = 800, height = 800)
st.plotly_chart(fig7, use_container_width=True)


########################################################################################   

st.subheader("Tabla de datos ")
with st.expander("Reporte de Obra"):
    df_sample = filtered_df[["Obra","Tipo de Pieza","Tipo de Soldadura","Tipo de Fallas","Categoria","Calificacion"]]
    fig8 = ff.create_table(df_sample, colorscale = "hot")
    st.plotly_chart(fig8, use_container_width=True)



######################################################################################## 

csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Descargar Archivo', data = csv, file_name = "Data.csv",mime = "text/csv")
export_as_pdf = st.button("Reporte Cliente")



fig1.write_image("images/fig1.png")
fig2.write_image("images/fig2.png")
fig3.write_image("images/fig3.png")
fig4.write_image("images/fig4.png")
fig5.write_image("images/fig5.png")
fig6.write_image("images/fig6.png")
fig8.write_image("images/fig7.png")



def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Descargar PDF</a>'





if export_as_pdf:
    class PDF(FPDF):
        # Page footer
        def header(self):
            # Position at 1.5 cm from bottom
            self.image('images/Encabezado.png',0, 10, 225, 0, 'PNG')
            self.ln(16)
            self.set_font('Arial', 'B', 10)
            self.cell(35, 10, 'Nombre de la Obra:',0,0,'L')
            self.set_font('Arial', 'I', 10)
            self.cell(90, 10, str(Obra[0]),0,0,'L')
             
            self.ln(8)
            self.set_font('Arial', 'B', 10)
            self.cell(12, 10, 'Fecha:',0,0,'L')
            self.set_font('Arial', 'I', 10)
            self.cell(90, 10, str(today2) ,0,0,'L')
            
            self.ln(8)
            self.set_font('Arial', 'B', 10)
            self.cell(112, 10, '' ,0,0,'L')
            self.cell(33, 10, 'Rango de Fechas:',0,0,'L')
            self.set_font('Arial', 'I', 10)
            self.cell(20, 10, str(today3) ,0,0,'L')
            self.cell(6, 10, ' - ' ,0,0,'L')
            self.cell(20, 10, str(today4) ,0,0,'L')
            pdf.ln(16)
            
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
   
    
    

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'Fallas por Pieza',0,0,'L')
    pdf.ln(8)
    pdf.image('images/fig1.png', 20, 67, 90, 0, 'PNG')
    pdf.image('images/fig3.png', 100, 67, 90, 0, 'PNG')
    
    
    pdf.ln(65)
    pdf.cell(190, 10, 'Fallas por Tipo de Soldadura',0,0,'L')
    pdf.image('images/fig2.png', 20, 140, 90, 0, 'PNG')
    pdf.image('images/fig4.png', 105, 140, 90, 0, 'PNG')
    
    
    pdf.ln(70)
    pdf.cell(190, 10, 'Fallas por Año y Mes',0,0,'L')
    pdf.image('images/fig5.png', 20, 208, 90, 0, 'PNG')
    pdf.image('images/fig6.png', 105, 208, 90, 0, 'PNG')
    
    
    
    pdf.add_page()
        

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(190, 10, 'Reporte de Obra',0,0,'L')
    pdf.ln(13)
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(255, 178, 102)
    pdf.cell(32,10, 'Obra', 1,0,'C', True)
    pdf.cell(32,10, 'Tipo de Pieza', 1,0,'C', True)
    pdf.cell(32,10, 'Tipo de Soldadura', 1,0,'C', True)
    pdf.cell(32,10, 'Tipo de Falla', 1,0,'C', True)
    pdf.cell(32,10, 'Categoría', 1,0,'C', True)
    pdf.cell(32,10, 'Calificación', 1,0,'C', True)
    pdf.ln()
    
    pdf.set_font('Arial', '', 6)

    columnNameList = list(df_sample)
    for row in range(0, len (df_sample)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList) - 1 :
                pdf.cell(32,10, str(df_sample['%s' % (col_name)].iloc[row]), 1,0,'C')
            else: 
                pdf.cell(32,10, str(df_sample['%s' % (col_name)].iloc[row]), 1,2,'C')
                pdf.cell(-160)
                
    pdf.cell(35,10,'',0,2)
    pdf.cell(20)
    
    
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), 'Obra '+str(Obra[0])+ '_'+str(today2) )


    st.markdown(html, unsafe_allow_html=True)