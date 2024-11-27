import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
import urllib.parse

# Configuración inicial de la app
st.set_page_config(
    page_title="Patrones de carga de vehículos eléctricoss",
    page_icon=":bar_chart:",
    layout="wide"
)

pages = st.sidebar.radio("Navegación", ["Introduccion y modificación del dataset", "Filtrado y Analisis de Datos"])

# Encabezado principal con diseño
st.title("📊Patrones de carga de vehículos eléctricos")
st.markdown("""
<style>
.big-font {
    font-size: 22px !important;
    color: #4CAF50;
    text-align: center;
}
.sidebar-title {
    font-size: 20px !important;
    font-weight: bold;
    color: #003566;
}
</style>
""", unsafe_allow_html=True)

# Importar el dataset
import kagglehub

ruta = kagglehub.dataset_download("valakhorasani/electric-vehicle-charging-patterns")
csv_file_path = None

for filename in os.listdir(ruta):
    if filename.endswith(".csv"):
        csv_file_path = os.path.join(ruta, filename)
        break

if not csv_file_path:
    st.error("No se encontró un archivo CSV en el dataset.")
    st.stop()

# 2. Creación de la base de datos con SQLite
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'ev_charging_data.db')
conn = sqlite3.connect(db_path)
table_name = "ev_charging"

# 3. Análisis de datos con pandas
query = f"SELECT * FROM {table_name}"
datos = pd.read_sql_query(query, conn)

if pages == "Introduccion y modificación del dataset":
    # Pagina Introductoria
    st.title("Introduccion y modificación del dataset")

    # Introducción al Dataset
    st.markdown("<h2 style='color: #ff8c00;'>Conjunto de Datos</h2>", unsafe_allow_html=True)

    st.markdown("""
    Este conjunto de datos proporciona un análisis exhaustivo de los patrones de carga de vehículos eléctricos (VE) y del comportamiento de los usuarios. 
    Contiene 1320 muestras de datos de sesiones de carga, incluidas métricas como el consumo de energía, la duración de la carga y los detalles del vehículo. 
    Cada entrada captura varios aspectos del uso de los VE, lo que permite un análisis profundo y un modelado predictivo.

    ### Características principales:

    - **ID de usuario**: Identificador único para cada usuario.
    - **Modelo del vehículo**: Modelo del vehículo eléctrico que se está cargando (por ejemplo, Tesla Model 3, Nissan Leaf).
    - **Capacidad de la batería (kWh)**: Capacidad total de la batería del vehículo en kilovatios-hora.
    - **ID de la estación de carga**: Identificador único de la estación de carga utilizada.
    - **Ubicación de la estación de carga**: Ubicación geográfica de la estación de carga (por ejemplo, Nueva York, Los Ángeles).
    - **Hora de inicio de la carga**: Marca de tiempo que indica cuándo comenzó la sesión de carga.
    - **Hora de finalización de la carga**: Marca de tiempo que indica cuándo finalizó la sesión de carga.
    - **Energía consumida (kWh)**: Energía total consumida durante la sesión de carga, medida en kilovatios-hora.
    - **Duración de la carga (horas)**: Tiempo total que tarda en cargarse el vehículo, medido en horas.
    - **Tasa de carga (kW)**: Tasa promedio de entrega de energía durante la sesión de carga, medida en kilovatios.
    - **Costo de carga (USD)**: Costo total incurrido en la sesión de carga, medido en dólares estadounidenses.
    - **Hora del día**: Segmento de tiempo en el que se realizó la carga (por ejemplo, mañana, tarde).
    - **Día de la semana**: Día de la semana en que se realizó la carga (por ejemplo, lunes, martes).
    - **Estado de carga (% de inicio)**: Porcentaje de carga de la batería al inicio de la sesión de carga.
    - **Estado de carga (% final)**: Porcentaje de carga de la batería al final de la sesión de carga.
    - **Distancia recorrida (desde la última carga) (km)**: Distancia recorrida desde la última sesión de carga, medida en kilómetros.
    - **Temperatura (°C)**: Temperatura ambiente durante la sesión de carga, medida en grados Celsius.
    - **Edad del vehículo (años)**: Edad del vehículo eléctrico, medida en años.
    - **Tipo de cargador**: Tipo de cargador utilizado (por ejemplo, Nivel 1, Nivel 2, Cargador rápido de CC).
    - **Tipo de usuario**: Clasificación del usuario en función de sus hábitos de conducción (por ejemplo, viajero diario, viajero de larga distancia).
    """)

    # Mostrar valores nulos en la tabla original
    st.header("📄 Manejo de Valores Vacíos")
    missing_values = datos.isnull().sum()
    st.write("Cantidad de valores vacíos por columna:")
    st.write(missing_values)

    # Botón para reemplazar valores nulos
    if st.button("Reparar valores nulos"):
        # Reemplazar valores nulos en columnas numéricas con la media
        for column in datos.select_dtypes(include=['int64', 'float64']).columns:
            mean_value = datos[column].mean()

            # Actualizar valores NULL y cadenas vacías en la base de datos
            query = f"""
            UPDATE "{table_name}"
            SET "{column}" = ?
            WHERE "{column}" IS NULL OR "{column}" = ''
            """
            cursor = conn.execute(query, (mean_value,))
            conn.commit()

            st.write(f"Filas afectadas en {column}: {cursor.rowcount}")

        # Reemplazar valores nulos en columnas categóricas con la moda
        for column in datos.select_dtypes(include=['object']).columns:
            mode_value = datos[column].mode()[0]

            query = f"""
            UPDATE "{table_name}"
            SET "{column}" = ?
            WHERE "{column}" IS NULL OR "{column}" = ''
            """
            cursor = conn.execute(query, (mode_value,))
            conn.commit()

            st.write(f"Filas afectadas en {column}: {cursor.rowcount}")

        # Recargar los datos para reflejar los cambios en la base de datos
        datos = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

        # Mostrar la tabla actualizada en la página
        st.write("Tabla actualizada:")
        st.dataframe(datos)

        st.success("✔️ Valores nulos reparados correctamente en la base de datos.")

elif pages == "Filtrado y Analisis de Datos":

    st.title("Filtrado y Analisis de Datos")
    # Sidebar personalizado
    st.sidebar.markdown('<div class="sidebar-title">Filtros Interactivos</div>', unsafe_allow_html=True)
    # Agregar un selectbox para seleccionar el modelo de vehículo
    st.sidebar.subheader("🚗 Seleccionar modelo de vehículo")
    vehicle_models = datos['Vehicle Model'].unique()
    selected_model = st.sidebar.selectbox("Elige un modelo:", options=["Todos"] + list(vehicle_models))

    if selected_model != "Todos":
        filtered_data = datos[datos['Vehicle Model'] == selected_model]
    else:
        filtered_data = datos

    # Agregar un slider para el costo de carga
    st.sidebar.subheader("💰 Filtrar por rango de costos de carga")
    min_cost, max_cost = datos['Charging Cost (USD)'].min(), datos['Charging Cost (USD)'].max()
    selected_cost_range = st.sidebar.slider("Selecciona el rango:", min_value=float(min_cost), max_value=float(max_cost), value=(float(min_cost), float(max_cost)))

    filtered_data = filtered_data[(filtered_data['Charging Cost (USD)'] >= selected_cost_range[0]) & 
                              (filtered_data['Charging Cost (USD)'] <= selected_cost_range[1])]

    # Filtrar por Número de usuario
    st.sidebar.subheader("🔢 Filtrar por Número de Usuario")
    user_numbers = datos['User ID'].unique()
    selected_user = st.sidebar.selectbox("Elige un número de usuario:", options=["Todos"] + list(user_numbers))

    if selected_user != "Todos":
        filtered_data = filtered_data[filtered_data['User ID'] == selected_user]

    # Filtrar por Rango de Capacidad de batería
    st.sidebar.subheader("🔋 Filtrar por Rango de Capacidad de Batería")
    min_battery_capacity, max_battery_capacity = datos['Battery Capacity (kWh)'].min(), datos['Battery Capacity (kWh)'].max()
    selected_battery_capacity = st.sidebar.slider("Selecciona el rango de capacidad de batería:", 
                                                min_value=float(min_battery_capacity), 
                                                max_value=float(max_battery_capacity), 
                                                value=(float(min_battery_capacity), float(max_battery_capacity)))

    filtered_data = filtered_data[(filtered_data['Battery Capacity (kWh)'] >= selected_battery_capacity[0]) & 
                                (filtered_data['Battery Capacity (kWh)'] <= selected_battery_capacity[1])]

    # Filtrar por ID de estación de carga
    st.sidebar.subheader("🏪 Filtrar por ID de Estación de Carga")
    charging_station_ids = datos['Charging Station ID'].unique()
    selected_station_id = st.sidebar.selectbox("Elige una estación de carga:", options=["Todos"] + list(charging_station_ids))

    if selected_station_id != "Todos":
        filtered_data = filtered_data[filtered_data['Charging Station ID'] == selected_station_id]

    # Filtrar por Localización de carga
    st.sidebar.subheader("📍 Filtrar por Localización de Carga")
    locations = datos['Charging Station Location'].unique()
    selected_location = st.sidebar.selectbox("Elige una localización:", options=["Todas"] + list(locations))

    if selected_location != "Todas":
        filtered_data = filtered_data[filtered_data['Charging Station Location'] == selected_location]

    # Filtrar por Rango de Energía Consumida
    st.sidebar.subheader("⚡ Filtrar por Rango de Energía Consumida")
    min_energy, max_energy = datos['Energy Consumed (kWh)'].min(), datos['Energy Consumed (kWh)'].max()
    selected_energy_range = st.sidebar.slider("Selecciona el rango de energía consumida:", 
                                            min_value=float(min_energy), 
                                            max_value=float(max_energy), 
                                            value=(float(min_energy), float(max_energy)))

    filtered_data = filtered_data[(filtered_data['Energy Consumed (kWh)'] >= selected_energy_range[0]) & 
                                (filtered_data['Energy Consumed (kWh)'] <= selected_energy_range[1])]

    # Filtrar por Rango de Duración de Carga
    st.sidebar.subheader("⏳ Filtrar por Rango de Duración de Carga")
    min_duration, max_duration = datos['Charging Duration (hours)'].min(), datos['Charging Duration (hours)'].max()
    selected_duration_range = st.sidebar.slider("Selecciona el rango de duración de carga:", 
                                                min_value=float(min_duration), 
                                                max_value=float(max_duration), 
                                                value=(float(min_duration), float(max_duration)))

    filtered_data = filtered_data[(filtered_data['Charging Duration (hours)'] >= selected_duration_range[0]) & 
                                (filtered_data['Charging Duration (hours)'] <= selected_duration_range[1])]

    # Filtrar por Rango de Rate de Carga
    st.sidebar.subheader("⚡ Filtrar por Rango de Rate de Carga")
    min_rate, max_rate = datos['Charging Rate (kW)'].min(), datos['Charging Rate (kW)'].max()
    selected_rate_range = st.sidebar.slider("Selecciona el rango de rate de carga:", 
                                            min_value=float(min_rate), 
                                            max_value=float(max_rate), 
                                            value=(float(min_rate), float(max_rate)))

    filtered_data = filtered_data[(filtered_data['Charging Rate (kW)'] >= selected_rate_range[0]) & 
                                (filtered_data['Charging Rate (kW)'] <= selected_rate_range[1])]

    # Filtrar por Tiempo del Día
    st.sidebar.subheader("🕒 Filtrar por Tiempo del Día")
    times_of_day = datos['Time of Day'].unique()
    selected_time_of_day = st.sidebar.selectbox("Elige el tiempo del día:", options=["Todos"] + list(times_of_day))

    if selected_time_of_day != "Todos":
        filtered_data = filtered_data[filtered_data['Time of Day'] == selected_time_of_day]

    # Filtrar por Día de la Semana
    st.sidebar.subheader("📅 Filtrar por Día de la Semana")
    days_of_week = datos['Day of Week'].unique()
    selected_day_of_week = st.sidebar.selectbox("Elige el día de la semana:", options=["Todos"] + list(days_of_week))

    if selected_day_of_week != "Todos":
        filtered_data = filtered_data[filtered_data['Day of Week'] == selected_day_of_week]

    # Filtrar por Rango de Distancia Conducida
    st.sidebar.subheader("🚗 Filtrar por Rango de Distancia Conducida")
    min_distance, max_distance = datos['Distance Driven (since last charge) (km)'].min(), datos['Distance Driven (since last charge) (km)'].max()
    selected_distance_range = st.sidebar.slider("Selecciona el rango de distancia conducida:", 
                                                min_value=float(min_distance), 
                                                max_value=float(max_distance), 
                                                value=(float(min_distance), float(max_distance)))

    filtered_data = filtered_data[(filtered_data['Distance Driven (since last charge) (km)'] >= selected_distance_range[0]) & 
                                (filtered_data['Distance Driven (since last charge) (km)'] <= selected_distance_range[1])]

    # Filtrar por Rango de Temperatura
    st.sidebar.subheader("🌡️ Filtrar por Rango de Temperatura")
    min_temperature, max_temperature = datos['Temperature (°C)'].min(), datos['Temperature (°C)'].max()
    selected_temperature_range = st.sidebar.slider("Selecciona el rango de temperatura:", 
                                                min_value=float(min_temperature), 
                                                max_value=float(max_temperature), 
                                                value=(float(min_temperature), float(max_temperature)))

    filtered_data = filtered_data[(filtered_data['Temperature (°C)'] >= selected_temperature_range[0]) & 
                                (filtered_data['Temperature (°C)'] <= selected_temperature_range[1])]

    # Filtrar por Rango de Años del Vehículo
    st.sidebar.subheader("📅 Filtrar por Rango de Años del Vehículo")
    min_year, max_year = datos['Vehicle Age (years)'].min(), datos['Vehicle Age (years)'].max()
    selected_year_range = st.sidebar.slider("Selecciona el rango de años del vehículo:", 
                                            min_value=int(min_year), 
                                            max_value=int(max_year), 
                                            value=(int(min_year), int(max_year)))

    filtered_data = filtered_data[(filtered_data['Vehicle Age (years)'] >= selected_year_range[0]) & 
                                (filtered_data['Vehicle Age (years)'] <= selected_year_range[1])]
    
    # 4. Mostrar los datos filtrados
    st.subheader("🔍 Datos Filtrados")
    st.write(f"🔍 **Cantidad de filas tras filtros aplicados: {filtered_data.shape[0]}**")
    st.write(filtered_data)

    # Agregar un botón para descargar los datos filtrados
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_data = convert_df(filtered_data)
    st.download_button(
        label="📥 Descargar datos filtrados",
        data=csv_data,
        file_name="datos_filtrados.csv",
        mime='text/csv',
    )

    numerical_columns = filtered_data.select_dtypes(include=['int64', 'float64']).columns

    if not numerical_columns.empty:
        st.markdown("<h2 style='color: #ff8c00;'>Estadísticas de columnas numéricas</h2>", unsafe_allow_html=True)
        for column in numerical_columns:
            mean = filtered_data[column].mean()
            median = filtered_data[column].median()
            mode = filtered_data[column].mode()[0]
            std_dev = filtered_data[column].std()

            st.markdown(f"### {column}")
            st.markdown(f"**📊 Media**: {mean:.2f}")
            st.markdown(f"**📊 Mediana**: {median:.2f}")
            st.markdown(f"**📊 Moda**: {mode:.2f}")
            st.markdown(f"**📊 Desviación estándar**: {std_dev:.2f}")
    else:
        st.markdown("<p style='color: #ff4d4d;'>No hay columnas numéricas en los datos filtrados.</p>", unsafe_allow_html=True)

    # Mostrar estadísticas para las columnas de texto
    categorical_columns = filtered_data.select_dtypes(include=['object']).columns

    if not categorical_columns.empty:
        st.markdown("<h2 style='color: #ff8c00;'>Estadísticas de columnas de texto</h2>", unsafe_allow_html=True)
        for column in categorical_columns:
            mode = filtered_data[column].mode()[0]
            st.markdown(f"### {column}")
            st.markdown(f"**📋 Moda**: {mode}")
    else:
        st.markdown("<p style='color: #ff4d4d;'>No hay columnas de texto en los datos filtrados.</p>", unsafe_allow_html=True)


    # Visualizaciones con un diseño mejorado
    st.markdown("<div class='big-font'>Visualizaciones Interactivas</div>", unsafe_allow_html=True)

    # Dividir en columnas para mostrar gráficos
    col1, col2 = st.columns(2)

    if filtered_data.empty:
        st.warning("No hay datos para mostrar con los filtros aplicados.")
    else:
        with col1:
            st.write("**📋 Frecuencia de cada modelo de vehículo**")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            filtered_data['Vehicle Model'].value_counts().plot(kind='bar', color='skyblue', ax=ax1)
            ax1.set_title('Número de vehículos por modelo')
            ax1.set_xlabel('Modelo de Vehículo')
            ax1.set_ylabel('Frecuencia')
            st.pyplot(fig1)

            st.write("**📊 Distribución de los costos de carga**")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            filtered_data['Charging Cost (USD)'].plot(kind='hist', bins=20, color='green', ax=ax2)
            ax2.set_title('Distribución de costos de carga')
            ax2.set_xlabel('Costo (USD)')
            ax2.set_ylabel('Frecuencia')
            st.pyplot(fig2)

        with col2:
            st.write("**⚡ Consumo de Energía vs Duración de Carga**")
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            ax4.scatter(filtered_data['Energy Consumed (kWh)'], filtered_data['Charging Duration (hours)'], alpha=0.5)
            ax4.set_title('Consumo de energía vs Duración de carga')
            ax4.set_xlabel('Energía Consumida (kWh)')
            ax4.set_ylabel('Duración de Carga (Horas)')
            st.pyplot(fig4)

        # Diagrama de torta al final
        st.write("**📅 Distribución de días de la semana**")
        fig5, ax5 = plt.subplots(figsize=(8, 8))
        filtered_data['Day of Week'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax5)
        ax5.set_title('Distribución de días de la semana')
        ax5.set_ylabel('')
        st.pyplot(fig5)

# Pie de página
st.markdown("""
<hr>
<center>
    TOMA DE DECISIONES I © 2024
</center>
""", unsafe_allow_html=True)
