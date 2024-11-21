import streamlit as st
import pandas as pd
import plotly.express as px
import folium #Librería de mapas en Python
from streamlit_folium import st_folium #Widget de Streamlit para mostrar los mapas
from folium.plugins import MarkerCluster #Plugin para agrupar marcadores

st.set_page_config(
    page_title="Sentiment Analisys California",
    page_icon="🌐",  
    layout='wide',
    initial_sidebar_state="expanded"
)

st.header('Informacion general y sentimental de Restaurantes')
dfRestaurantes= pd.read_csv('df_ML.csv') # modificar ruta en github
#dfRestaurantes['food']=dfRestaurantes['food'].fillna(0)
#dfRestaurantes['service']=dfRestaurantes['service'].fillna(0)
#dfRestaurantes['place']=dfRestaurantes['place'].fillna(0)
#dfRestaurantes['menu']=dfRestaurantes['menu'].fillna(0)
location = [27.9521519,-82.4608919]

tab1,tab3,tab4=st.tabs(['Mapa Plotly','Mapa Folium' ,'Datos']) # ventanas #tab2 = 'Mapa Choropleth'
with tab1:
    parUbi = st.checkbox('Ingresar coordenadas:')
    if parUbi:
        lat = st.text_input('ingrese la latitud')
        lon = st.text_input('ingrese la longitud')
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                fig = px.scatter_mapbox(dfRestaurantes, lat=lat, lon=lon, 
                                        color='stars', hover_name='name', hover_data=['food', 'place','menu','service'],                                
                                        zoom=10, height=600)
            except ValueError:
                st.error("Por favor, ingrese valores numéricos para la latitud y longitud.")
    parMapa = st.selectbox('Tipo Mapa',options=["open-street-map", "carto-positron","carto-darkmatter"])    
    
    parCaract = st.checkbox('Tamaño por caracteristica de restaurante')

    dfRestaurantes[['food', 'service', 'place', 'menu']] = dfRestaurantes[['food', 'service', 'place', 'menu']].fillna(0)

    caract_map = {'servicio': 'service', 'lugar': 'place', 'menu': 'menu', 'comida': 'food'}

    if parCaract:
        caract = st.selectbox('Elija la característica', options=list(caract_map.keys()))
        col = caract_map[caract]
        fig = px.scatter_mapbox(dfRestaurantes, lat='latitude', lon='longitude', 
                                color='stars', hover_name='name', hover_data=['food', 'place', 'menu', 'service'],
                                zoom=10, size=col, height=600)
    else:
        fig = px.scatter_mapbox(dfRestaurantes,lat='latitude',lon='longitude', 
                                color='stars', hover_name='name',hover_data=['food', 'place','menu','service'],                                
                                zoom=10,height=600)
    fig.update_layout(mapbox_style=parMapa)
    st.plotly_chart(fig,use_container_width=True)
#with tab2:
#    df = px.data.gapminder().query("year==2007")    
#    fig = px.choropleth(df, locations="iso_alpha",
#                        color="lifeExp", # lifeExp is a column of gapminder
#                        hover_name="country", # column to add to hover information
#                        color_continuous_scale=px.colors.sequential.Plasma)
#    st.plotly_chart(fig,use_container_width=True)
#    st.dataframe(df)
with tab3:
    parTipoMapa = st.radio('Tipo de marcadores',options=['Cluster','Individuales'],horizontal=True)
    m = folium.Map(location= location, zoom_start=15) #location = [6.242827227796505, -75.6132478]
    if parTipoMapa=='Cluster':
        marker_cluster = MarkerCluster().add_to(m)

    for index, row in dfRestaurantes.iterrows():        
        marker = folium.Marker(        
                location=[row['latitude'], row['longitude']],
                popup=row['name'],
                icon=folium.Icon(color="red", icon="ok-sign"),
            )
        if parTipoMapa=='Cluster':
            marker.add_to(marker_cluster)
        else:
            marker.add_to(m)
    folium.plugins.Fullscreen(
        position="topright",
        title="Pantalla completa",
        title_cancel="Cancelar",
        force_separate_button=True,
    ).add_to(m)
    out = st_folium(m, height=600,use_container_width=True)
    st.write(out)
with tab4:
    st.dataframe(dfRestaurantes,use_container_width=True)