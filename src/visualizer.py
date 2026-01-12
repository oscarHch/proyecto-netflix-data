import matplotlib.pyplot as plt
import seaborn as sns

def get_trend_plot(df):
    trend_data = df[df['year_added'] > 2008].groupby(['year_added', 'type']).size().unstack().fillna(0)
    
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    sns.lineplot(data=trend_data, markers=True, ax=ax)

    ax.set_title("Evolución de Contenido")
    ax.set_xlabel("Año de Adición")
    ax.set_ylabel("Cantidad de Títulos")

    fig.tight_layout()

    return fig

def get_countries_plot(df):
    countries = df.explode('countries_list')['countries_list'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    countries.plot(kind='barh', ax=ax, color='salmon')

    ax.invert_yaxis()
    ax.set_title("Top 10 Países")
    ax.set_xlabel("Cantidad de títulos")
    ax.set_ylabel("País")

    fig.tight_layout()

    return fig

def get_genres_plot(df):
    genres = df.explode('genres_list')['genres_list'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    genres.plot(kind='bar', ax=ax, color='mediumpurple')
    plt.xticks(rotation=45, ha='right')
    
    ax.set_title("Top 10 Géneros")
    ax.set_xlabel("Categoría / Género")
    ax.set_ylabel("Total de Títulos")

    fig.tight_layout()

    return fig