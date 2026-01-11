import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_content_distribution(df):
    # Configuramos el estilo
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 6))
    
    # Creamos el grafico
    ax = sns.countplot(data=df, x='type', palette='viridis')
    
    plt.title('Distribución de contenido en Netflix', fontsize=14)
    plt.xlabel('Tipo de contenido', fontsize=12)
    plt.ylabel('Cantidad', fontsize=12)

    # Creamos la carpeta outputs si no existe
    base_path = os.path.dirname(__file__)
    output_dir = os.path.join(base_path, '..', 'outputs')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Guardamos el gráfico
    output_path = os.path.join(output_dir, 'content_distribution.png')
    plt.savefig(output_path)
    plt.close()
    
    print(f"Gráfico guardado en: {output_path}")