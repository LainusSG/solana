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

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown(f'<p style="display: block; text-align:right; font-size: 24px;  margin-top:-2rem;  color: #000;font-weight: bold;"> Usuario: {st.session_state["name"]}</p>', unsafe_allow_html=True)
col1, col2,col3 = st.columns((3))
with col1:
    st.write("")
with col2:
    st.image('reportes/TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
with col3:
    st.write("")

# fl = st.file_uploader(":file_folder: Subir Archivo!",type=(["csv","txt","xlsx","xls"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_csv(filename, encoding = "ISO-8859-1")
# else:
    #os.chdir(r"reportes")
df = pd.read_csv("reportes/Graficas3.csv", encoding = "ISO-8859-1")



########################################################################################   
    
col1, col2 = st.columns((2))
def convert(dt):
    try:
        return datetime.strptime(dt, '%m/%d/%Y').strftime('%d/%m/%Y')
    except ValueError:
        return dt
df["FECHA"] = pd.to_datetime(df["FECHA"])

# Getting the min and max date 
startDate = pd.to_datetime(df["FECHA"]).min()
endDate = pd.to_datetime(df["FECHA"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Fecha de Inicio", startDate))
    today3 = date1.strftime("%d/%m/%Y")

with col2:
    date2 = pd.to_datetime(st.date_input("Fecha Final", endDate))
    today4 = date2.strftime("%d/%m/%Y")

df = df[(df["FECHA"] >= date1) & (df["FECHA"] <= date2)].copy()

########################################################################################   

col1, col2, col3, col4, col5 = st.columns((5))


# Create for Obra

with col1:
    calificacion = st.multiselect("Elige una Obra", df["OBRA"].unique())
    if not calificacion:
        df2 = df.copy()
    else:
        df2 = df[df["OBRA"].isin(calificacion)]
        
    Obra =calificacion
# Create for Tipo de Fallas
with col2:
    Tipo_de_Fallas = st.multiselect("Elige un Cliente", df2["CLIENTE"].unique())
    if not Tipo_de_Fallas:
        df3 = df2.copy()
    else:
        df3 = df2[df2["CLIENTE"].isin(Tipo_de_Fallas)]

# Create for Tipo de Pieza
with col3:
    Tipo_de_Pieza = st.multiselect("Elige un Material",df3["TIPO DE PIEZA"].unique())
    if not Tipo_de_Pieza:
        df4 = df3.copy()
    else:
        df4 = df3[df3["TIPO DE PIEZA"].isin(Tipo_de_Pieza)]

with col4:
    Pieza = st.multiselect("Elige una Pieza",df4["PIEZA"].unique())
    if not Pieza:
        df5 = df4.copy()
    else:
        df5 = df4[df4["PIEZA"].isin(Pieza)]

with col5:
    Falla = st.multiselect("Elige una Falla",df5["TIPO DE FALLAS"].unique())
   





if not calificacion and not Tipo_de_Fallas and not Tipo_de_Pieza:
    filtered_df = df
elif not Tipo_de_Fallas and not Tipo_de_Pieza:
    filtered_df = df[df["OBRA"].isin(calificacion)]
elif not calificacion and not Tipo_de_Pieza:
    filtered_df = df[df["CLIENTE"].isin(Tipo_de_Fallas)]
elif Tipo_de_Fallas and Tipo_de_Pieza:
    filtered_df = df3[df["CLIENTE"].isin(Tipo_de_Fallas) & df3["TIPO DE PIEZA"].isin(Tipo_de_Pieza)]
elif calificacion and Tipo_de_Pieza:
    filtered_df = df3[df["OBRA"].isin(calificacion) & df3["TIPO DE PIEZA"].isin(Tipo_de_Pieza)]
elif calificacion and Tipo_de_Fallas:
    filtered_df = df3[df["OBRA"].isin(calificacion) & df3["CLIENTE"].isin(Tipo_de_Fallas)]
elif Tipo_de_Pieza:
    filtered_df = df3[df3["TIPO DE PIEZA"].isin(Tipo_de_Pieza)]
else:
    filtered_df = df3[df3["OBRA"].isin(calificacion) & df3["CLIENTE"].isin(Tipo_de_Fallas) & df3["TIPO DE PIEZA"].isin(Tipo_de_Pieza)]

category_df = filtered_df.groupby(by = ["TIPO DE PIEZA"], as_index = False)["FALLAS"].sum()

category2_df = filtered_df.groupby(by = ["OBRA"], as_index = False)["FALLAS"].sum()

with st.expander("Fallas en Obras"):
    fig12 = px.bar(category2_df, x = "OBRA", y = "FALLAS", text = [x for x in category2_df["FALLAS"]],
                    template ="ggplot2")
    fig12.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig12.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig12,use_container_width=True, height = 200)
    
col1, col2= st.columns((2))


with col1:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Pieza</p>', unsafe_allow_html=True)
    fig1 = px.bar(category_df, x = "TIPO DE PIEZA", y = "FALLAS", text = [x for x in category_df["FALLAS"]])
    fig1.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig1.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig1,use_container_width=True, height = 200)

with col2:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;">Fallas por Tipo de Soldadura</p>', unsafe_allow_html=True)
    fig2 = px.pie(filtered_df, values = "FALLAS", names = "TIPO DE SOLDADURA", hole = 0.5, template ="presentation")
    fig2.update_traces(text = filtered_df["CATEGORIA"], textposition = "outside")
    fig2.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    
    st.plotly_chart(fig2,use_container_width=True)

# Create a treem based on Region, category, sub-Category


chart1, chart2 = st.columns((2))
with chart1:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Pieza</p>', unsafe_allow_html=True)
    fig3 = px.pie(filtered_df, values = "FALLAS", names = "TIPO DE PIEZA", template ="presentation")
    fig3.update_traces(text = filtered_df["TIPO DE PIEZA"], textposition = "inside")
    fig3.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig3,use_container_width=True)

with chart2:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Tipo de Soldadura</p>', unsafe_allow_html=True)
    fig4 = px.pie(filtered_df, values = "FALLAS", names = "TIPO DE SOLDADURA", template ="presentation")
    fig4.update_traces(text = filtered_df["TIPO DE FALLAS"], textposition = "inside")
    fig4.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
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
        calificacion = filtered_df.groupby(by = "CATEGORIA", as_index = False)["FALLAS"].sum()
        st.write(calificacion.style.background_gradient(cmap="Oranges"))
        csv = calificacion.to_csv(index = False).encode('utf-8')
        st.download_button("Descargar", data = csv, file_name = "Categoria.csv", mime = "text/csv",
                        help = 'Haz click para descargar la información')
        
        





col1, col2 = st.columns((2))

########################################################################################           
with col1:
    filtered_df["Año"] = filtered_df["FECHA"].dt.to_period("Y")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Año</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Año"].dt.strftime("%Y"))["FALLAS"].sum()).reset_index()
    fig5 = px.line(linechart, x = "Año", y="FALLAS", labels = {"FALLAS": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig5.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig5.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig5,use_container_width=True)

    with st.expander("Fallas Por Año"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Año.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')



########################################################################################           
with col2:
    filtered_df["Mes"] = filtered_df["FECHA"].dt.to_period("M")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Mes</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Mes"].dt.strftime("%B"))["FALLAS"].sum()).reset_index()
    fig6 = px.line(linechart, x = "Mes", y="FALLAS", labels = {"FALLAS": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig6.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig6.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig6,use_container_width=True)

    with st.expander("Fallas Por Mes"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Mes.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')


########################################################################################   


col1, col2 = st.columns((2))

########################################################################################           
with col1:
    filtered_df["Semana"] = filtered_df["FECHA"].dt.to_period("W")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Semana</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Semana"].dt.strftime("%W"))["FALLAS"].sum()).reset_index()
    fig9 = px.line(linechart, x = "Semana", y="FALLAS", labels = {"FALLAS": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig9.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig9.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig9,use_container_width=True)

    with st.expander("Fallas Por Semana"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Semana.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')


with col2:
    filtered_df["Dia"] = filtered_df["FECHA"].dt.to_period("D")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Dia</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Dia"].dt.strftime("%D"))["FALLAS"].sum()).reset_index()
    fig10 = px.line(linechart, x = "Dia", y="FALLAS", labels = {"FALLAS": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig10.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig10.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig10,use_container_width=True)

    with st.expander("Fallas Por Dia"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Dia.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')




st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas</p>', unsafe_allow_html=True)
with st.expander("Organización de Fallas"):
    fig7 = px.treemap(filtered_df, path = ["CATEGORIA","TIPO DE FALLAS","TIPO DE PIEZA", "CALIFICACION"], values = "FALLAS",hover_data = ["FALLAS"],template="presentation")
    fig7.update_layout(width = 800, height = 800)
    fig7.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
    st.plotly_chart(fig7, use_container_width=True)


########################################################################################   

st.write('<p style="font-size:25px; font-weight:bold; text-align:center;">Tabla de Datos</p>', unsafe_allow_html=True)
with st.expander("Reporte de Obra"):
    df_sample = filtered_df[["FECHA","OBRA","CLIENTE","TIPO DE PIEZA","PIEZA","TIPO DE SOLDADURA","TIPO DE FALLAS","CATEGORIA","CALIFICACION","FALLAS"]]
    df_sample["FECHA"] = [
        datetime.datetime.strptime(
            str(target_date).split(" ")[0], '%Y-%m-%d').date()
        for target_date in df_sample["FECHA"]
    ]
    fig8 = ff.create_table(df_sample, colorscale = "hot")
    fig8.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig8, use_container_width=True)



######################################################################################## 
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1]) 
with col1:
    st.write("")
with col2:
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Descargar Archivo', data = csv, file_name = "Data.csv",mime = "text/csv")
with col3:
    st.write("")
with col4:
    export_as_pdf = st.button("Reporte Cliente")
with col5:
    st.write("")



fig1.write_image("reportes/images/fig1.png")
fig2.write_image("reportes/images/fig2.png")
fig3.write_image("reportes/images/fig3.png")
fig4.write_image("reportes/images/fig4.png")
fig9.write_image("reportes/images/fig5.png")
fig10.write_image("reportes/images/fig6.png")
fig8.write_image("reportes/images/fig7.png")



def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Descargar PDF</a>'





if export_as_pdf:
    class PDF(FPDF):
        # Page footer
        def header(self):
            # Position at 1.5 cm from bottom
            self.image('reportes/images/ENCABEZADOSOLANA.png',0, 0, 217, 0, 'PNG')
            self.ln(34)
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
            pdf.ln(10)
            
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # Instantiation of inherited class
    pdf = PDF('P','mm','Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    
   
    
    

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'Fallas por Pieza',0,0,'L')
    pdf.ln(8)
    pdf.image('reportes/images/fig1.png', 20, 77, 90, 0, 'PNG')
    pdf.image('reportes/images/fig3.png', 100, 77, 90, 0, 'PNG')
    
    
    pdf.ln(65)
    pdf.cell(190, 10, 'Fallas por Tipo de Soldadura',0,0,'L')
    pdf.image('reportes/images/fig2.png', 20, 150, 90, 0, 'PNG')
    pdf.image('reportes/images/fig4.png', 105, 150, 90, 0, 'PNG')
    
    
    pdf.ln(70)
    pdf.cell(190, 10, 'Fallas Semanales y Diarias',0,0,'L')
    pdf.image('reportes/images/fig5.png', 20, 220, 90, 0, 'PNG')
    pdf.image('reportes/images/fig6.png', 105, 220, 90, 0, 'PNG')
    
    
    
    pdf.add_page()
        

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(190, 10, 'Reporte de Obra',0,0,'L')
    pdf.ln(13)
    
    pdf.set_font('Arial', 'B', 6)
    pdf.set_fill_color(255, 178, 102)
    pdf.cell(19.6,10, 'Fecha', 1,0,'C', True)
    pdf.cell(19.6,10, 'Obra', 1,0,'C', True)
    pdf.cell(19.6,10, 'Cliente', 1,0,'C', True)
    pdf.cell(19.6,10, 'Tipo de Pieza', 1,0,'C', True)
    pdf.cell(19.6,10, 'pieza', 1,0,'C', True)
    pdf.cell(19.6,10, 'Tipo de Soldadura', 1,0,'C', True)
    pdf.cell(19.6,10, 'Tipo de Falla', 1,0,'C', True)
    pdf.cell(19.6,10, 'Categoría', 1,0,'C', True)
    pdf.cell(19.6,10, 'Calificación', 1,0,'C', True)
    pdf.cell(19.6,10, 'Fallas', 1,0,'C', True)
    pdf.ln()
    
    pdf.set_font('Arial', '', 4)

    columnNameList = list(df_sample)
    for row in range(0, len (df_sample)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList) - 1 :
                pdf.cell(19.6,10, str(df_sample['%s' % (col_name)].iloc[row]), 1,0,'C')
            else: 
                pdf.cell(19.6,10, str(df_sample['%s' % (col_name)].iloc[row]), 1,2,'C')
                pdf.cell(-176.4)
                
    pdf.cell(35,10,'',0,2)
    pdf.cell(20)
    
    
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), 'Obra '+str(Obra[0])+ '_'+str(today2) )


    st.markdown(html, unsafe_allow_html=True)









