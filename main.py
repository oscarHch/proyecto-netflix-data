from src.exploration import clean_netflix_data
from src.visualizer import plot_content_distribution

def run():
    print("Netlix Data Analyzer")
    
    path_al_archivo = 'data/netflix-data.csv'
    df_limpio = clean_netflix_data(path_al_archivo) # Limpiamos los datos
    
    print(f"He encontrado {len(df_limpio)} títulos.")
    confirmacion = input("¿Deseas generar el gráfico de distribución? (s/n): ")
    
    if confirmacion.lower() == 's':
        plot_content_distribution(df_limpio)
        print("¡Listo! Revisa tu carpeta 'outputs'.")
    else:
        print("Análisis cancelado.")

if __name__ == "__main__":
    run()