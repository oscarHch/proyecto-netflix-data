from fpdf import FPDF
import os

def generate_pdf_report(df, visualizer_module):
    # Crear carpeta si no existe
    if not os.path.exists("outputs/pdf"):
        os.makedirs("outputs/pdf")

    # Lógica de numeración automática
    contador = 1
    while os.path.exists(f"outputs/pdf/reporte_netflix_{contador}.pdf"):
        contador += 1
    
    output_path = f"outputs/pdf/reporte_netflix_{contador}.pdf"

    pdf = FPDF()
    pdf.add_page()
    
    # titulo principal
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(229, 9, 20) # Rojo Netflix
    pdf.cell(0, 20, "NETFLIX DATA REPORT", ln=True, align="C")
    pdf.ln(10)

    # Resumen estadistico
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Resumen General del Contenido:", ln=True)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"- Total de titulos analizados: {len(df)}", ln=True)
    pdf.cell(0, 8, f"- Peliculas disponibles: {len(df[df['type'] == 'Movie'])}", ln=True)
    pdf.cell(0, 8, f"- Series de TV disponibles: {len(df[df['type'] == 'TV Show'])}", ln=True)
    pdf.ln(10)

    # 4. Incluir Imágenes de los Gráficos
    # Guardaremos versiones temporales de los gráficos para el PDF
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Visualizaciones de Datos:", ln=True)
    pdf.ln(5)

    # Gráfico de Tendencias
    fig_trend = visualizer_module.get_trend_plot(df)
    fig_trend.savefig("temp_trend.png")
    pdf.image("temp_trend.png", x=10, w=180)
    pdf.ln(5)

    # Gráfico de Países (Nueva página para que no se amontone)
    pdf.add_page()
    pdf.cell(0, 10, "Distribucion por Paises y Generos:", ln=True)
    pdf.ln(5)
    
    fig_countries = visualizer_module.get_countries_plot(df)
    fig_countries.savefig("temp_countries.png")
    pdf.image("temp_countries.png", x=10, w=180)

    # Limpieza de archivos temporales
    os.remove("temp_trend.png")
    os.remove("temp_countries.png")
    
    pdf.output(output_path)
    return output_path