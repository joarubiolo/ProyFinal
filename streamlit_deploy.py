import streamlit as st
import pandas as pd
import plotly.express as px
import folium #Librería de mapas en Python
from streamlit_folium import st_folium #Widget de Streamlit para mostrar los mapas
from folium.plugins import MarkerCluster #Plugin para agrupar marcadores
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(
    page_title="Sentiment Analisys California",
    page_icon="🌐",  
    layout='wide',
    initial_sidebar_state="expanded"
)

st.header('Informacion general y sentimental de Restaurantes')
dfRestaurantes= pd.read_csv('df_ML.csv') # modificar ruta en github
scaler = MinMaxScaler(feature_range=(1, 5))  # Cambia el rango
cols_to_fix = ['food', 'service', 'place', 'menu']
dfRestaurantes[cols_to_fix] = scaler.fit_transform(dfRestaurantes[cols_to_fix])

#dfRestaurantes['food']=dfRestaurantes['food'].fillna(0)
#dfRestaurantes['service']=dfRestaurantes['service'].fillna(0)
#dfRestaurantes['place']=dfRestaurantes['place'].fillna(0)
#dfRestaurantes['menu']=dfRestaurantes['menu'].fillna(0)
location = [27.9521519,-82.4608919]
stateslist = dfRestaurantes['state'].unique()
citylist = dfRestaurantes['city'].unique()

tab1,tab3,tab4=st.tabs(['Mapa Plotly','Mapa Folium' ,'Datos']) # ventanas #tab2 = 'Mapa Choropleth'
with tab1:
    parMapa = st.selectbox('Tipo Mapa',options=["open-street-map", "carto-positron","carto-darkmatter"])
    parUbi = st.selectbox('Buscar por', options=['coordenadas','codigo postal','estado','ciudad'])
    if parUbi=='coordenadas':
        lat = st.text_input('ingrese la latitud', placeholder="Ej: 27.9521519")
        lon = st.text_input('ingrese la longitud', placeholder="Ej: -82.4608919")
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                fig = px.scatter_mapbox(dfRestaurantes, lat='latitude', lon='longitude', 
                                        color='stars', hover_name='name', hover_data=['food', 'place','menu','service'],                                
                                        zoom=10, height=600)
                fig.update_layout(
                mapbox_style=parMapa,
                mapbox_center={"lat": lat, "lon": lon},  # Usa las coordenadas ingresadas
                mapbox_zoom=10  # Nivel de zoom inicial
                )
            except ValueError:
                st.error("Por favor, ingrese valores numéricos para la latitud y longitud.")  
    
    elif parUbi=='codigo postal':
        Cod = st.text_input("Ingrese un codigo postal", max_chars=4, placeholder="Ej: 1234")
        df_filtrado = dfRestaurantes[dfRestaurantes['postal_code'] == Cod]

        if not df_filtrado.empty:
            # Obtener las coordenadas promedio del código postal
            lat_central = df_filtrado['latitude'].mean()
            lon_central = df_filtrado['longitude'].mean()
    
            # Crear el mapa centrado
            fig = px.scatter_mapbox(
                dfRestaurantes, 
                lat='latitude', 
                lon='longitude', 
                color='stars', 
                hover_name='name', 
                hover_data=['food', 'place', 'menu', 'service'],
                zoom=10, 
                height=600
            )
            fig.update_layout(
                mapbox_style="open-street-map",
                mapbox_center={"lat": lat_central, "lon": lon_central},  # Centrar en el código postal
                mapbox_zoom=12
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No se encontraron restaurantes con ese código postal.")

    elif parUbi=='state':
        estado = st.selectbox('seleccione un estado',options=stateslist)
        df_filtrado = dfRestaurantes[dfRestaurantes['state'] == estado]
        if not df_filtrado.empty:
            lat_central = df_filtrado['latitude'].mean()
            lon_central = df_filtrado['longitude'].mean()
    
            # Crear el mapa centrado
            fig = px.scatter_mapbox(
                dfRestaurantes, 
                lat='latitude', 
                lon='longitude', 
                color='stars', 
                hover_name='name', 
                hover_data=['food', 'place', 'menu', 'service'],
                zoom=10, 
                height=600
            )
            fig.update_layout(
                mapbox_style="open-street-map",
                mapbox_center={"lat": lat_central, "lon": lon_central},  # Centrar en el código postal
                mapbox_zoom=12
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No se encontraron restaurantes en ese estado.")
    
    elif parUbi=='city':
        ciudad = st.selectbox('seleccione una ciudad',options=citylist)
        df_filtrado = dfRestaurantes[dfRestaurantes['city'] == ciudad]
        if not df_filtrado.empty:
            lat_central = df_filtrado['latitude'].mean()
            lon_central = df_filtrado['longitude'].mean()
    
            # Crear el mapa centrado
            fig = px.scatter_mapbox(
                dfRestaurantes, 
                lat='latitude', 
                lon='longitude', 
                color='stars', 
                hover_name='name', 
                hover_data=['food', 'place', 'menu', 'service'],
                zoom=10, 
                height=600
            )
            fig.update_layout(
                mapbox_style="open-street-map",
                mapbox_center={"lat": lat_central, "lon": lon_central},  # Centrar en el código postal
                mapbox_zoom=12
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No se encontraron restaurantes en esa ciudad.")
        
            
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
    fig.update_layout(
    mapbox_style=parMapa,
    mapbox_center={"lat": location[0], "lon": location[1]},  # Coordenadas iniciales
    mapbox_zoom=10  # Nivel de zoom inicial
    )

    st.plotly_chart(fig, use_container_width=True)
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
