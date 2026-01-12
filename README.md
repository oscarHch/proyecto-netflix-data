# Netflix Data Analyzer

Una aplicación de escritorio interactiva desarrollada en Python para el análisis estadístico y visualización de datos del catálogo de Netflix hasta 2025.

## Características

* **Dashboard Principal:** Vista unificada con indicadores clave y gráficos de tendencias.
* **Análisis estadístico:** Cálculo automático de duración media, diversidad de países, y brecha (gap) entre estreno y adición a la plataforma.
* **Visualización dinámica:** Gráficos de barras y líneas integrados mediante Matplotlib.
* **Gestión de datos:** Tabla interactiva de datos.
* **Exportación:** Generación de reportes detallados en formato PDF.

## Tecnologías

* **Python 3.x**
* **CustomTkinter:** Interfaz de usuario personalizada.
* **Pandas:** Manipulación y limpieza de grandes volúmenes de datos.
* **Matplotlib:** Generación de gráficos estadísticos.
* **ReportLab:** Creación de reportes PDF.

## Estructura del Proyecto

```text
.
├── data/               # Repositorio de datos crudos (CSV)
├── notebooks/          # Experimentos preliminares y análisis exploratorio
├── outputs/            
│   └── pdf/            # Reportes exportados y documentos generados
├── src/                # Código fuente
│   ├── exploration.py  # Algoritmos de limpieza y cálculos estadísticos
│   ├── visualizer.py   # Configuración de gráficas y capas de Matplotlib
│   └── reporter.py     # Lógica de renderizado y exportación de documentos
├── main_app.py         # Orquestador de la aplicación y lógica del GUI
└── README.md           # Documentación
