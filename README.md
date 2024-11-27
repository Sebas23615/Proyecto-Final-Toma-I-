# Análisis de Patrones de Carga de Vehículos Eléctricos

Este proyecto proporciona un análisis exhaustivo de los patrones de carga de vehículos eléctricos (VE) y el comportamiento de los usuarios a partir de un conjunto de datos que contiene 1320 muestras de datos de sesiones de carga. El análisis incluye métricas como el consumo de energía, la duración de la carga, los detalles del vehículo, y mucho más.

## Características principales

El conjunto de datos contiene las siguientes columnas:

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
- **Tipo de usuario**: Clasificación del usuario en función de sus hábitos de conducción (p. ej., viajero diario, viajero de larga distancia).

## Descripción del Proyecto

El objetivo de este proyecto es permitir a los usuarios explorar y analizar los patrones de carga de vehículos eléctricos mediante una aplicación interactiva construida con **Streamlit**. Los usuarios pueden cargar el conjunto de datos, realizar filtrados y visualizaciones, y obtener estadísticas descriptivas para ayudar en la toma de decisiones.

## Tecnologías Utilizadas

Este proyecto utiliza las siguientes tecnologías:

- **Python**: Lenguaje de programación principal.
- **Streamlit**: Framework de desarrollo web para aplicaciones interactivas.
- **Pandas**: Para la manipulación de datos.
- **Matplotlib** y **Seaborn**: Para la visualización de datos.
- **Plotly**: Para gráficos interactivos.

## Instrucciones de uso

### Requisitos

Para ejecutar este proyecto localmente, necesitas tener **Python 3.x** y las siguientes librerías:

- Streamlit
- Pandas
- Numpy
- Matplotlib
- Seaborn
- Plotly

### Instrucciones para ejecutar localmente

1. Clona este repositorio a tu máquina local:
    ```bash
    git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/Sebas23615/Proyecto-Final-Toma-I-.git)
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd tu_repositorio
    ```

3. Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux o macOS
    venv\Scripts\activate     # En Windows
    ```

4. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

5. Ejecuta la aplicación Streamlit:
    ```bash
    streamlit run app.py
    ```

### Despliegue en Streamlit Cloud

Para desplegar la aplicación en **Streamlit Cloud** y compartirla con otros sin necesidad de que instalen las librerías, sigue estos pasos:

1. **Crea un repositorio en GitHub** con este proyecto si aún no lo has hecho.
2. **Sube tu código a GitHub**.
3. Accede a [Streamlit Cloud](https://share.streamlit.io/) y haz login con tu cuenta de GitHub.
4. **Conecta tu repositorio** a Streamlit Cloud:
   - Haz clic en "New App" y selecciona el repositorio que contiene el proyecto.
   - Elige la rama (normalmente `main`) y selecciona el archivo Python principal (`app.py`).
5. Haz clic en **Deploy** y tu aplicación será desplegada automáticamente en la web.

Una vez desplegada, podrás compartir el enlace generado por Streamlit Cloud para que otros usuarios accedan a la aplicación.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, por favor sigue estos pasos:

1. Forkea este repositorio.
2. Crea una rama con tus cambios (`git checkout -b feature-nueva`).
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`).
4. Haz push a tu rama (`git push origin feature-nueva`).
5. Abre un pull request.
