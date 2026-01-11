import pandas as pd
import os

def clean_netflix_data(file_path):

    # Ruta absoluta
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, '..', file_path)

    df = pd.read_csv(full_path)

    # Llenamos valores faltantes con valores predeterminados
    df['director'] = df['director'].fillna('Unknown Director')
    df['cast'] = df['cast'].fillna('No Cast Listed')
    df['country'] = df['country'].fillna('Unknown Country')
    df['rating'] = df['rating'].fillna('Not Rated')
    df['duration'] = df['duration'].fillna('0 min')

    # Eliminamos filas con valores faltantes en columnas
    df.dropna(subset = ['rating', 'date_added', 'duration'], inplace=True)

    # Adaptamos las fechas
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df.dropna(subset=['date_added'], inplace=True)
    # Columna año
    df['year_added'] = df['date_added'].dt.year.astype(int)

    return df

if __name__ == "__main__":
    # Prueba funcional
    data = clean_netflix_data('data/netflix-data.csv')
    print("Datos limpiados exitosamente.\nNumero de filas:", len(data))
    print(data)