import pandas as pd
import os

def clean_netflix_data(file_path):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, '..', file_path)

    df = pd.read_csv(full_path)

    # Limpieza de rating (adicional)
    df = df[~df['rating'].str.contains('min|Season', na=False)]

    # Valores predeterminados
    df['director'] = df['director'].fillna('Unknown Director')
    df['cast'] = df['cast'].fillna('No Cast Listed')
    df['country'] = df['country'].fillna('Unknown Country')
    df['rating'] = df['rating'].fillna('Not Rated')

    # Eliminamos filas con valores faltantes en columnas
    df.dropna(subset = ['rating', 'date_added', 'duration'], inplace=True)

    # Fechas
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df.dropna(subset=['date_added'], inplace=True)
    df['year_added'] = df['date_added'].dt.year.astype(int)

    # Análisis individuales
    df['countries_list'] = df['country'].str.split(', ')
    df['genres_list'] = df['listed_in'].str.split(', ')

    return df

if __name__ == "__main__":
    # Prueba funcional
    data = clean_netflix_data('data/netflix-data.csv')
    print("Datos limpiados exitosamente.\nNumero de filas:", len(data))
    print(data)