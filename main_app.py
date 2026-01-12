import customtkinter as ctk
from src.exploration import clean_netflix_data, get_advanced_stats
from src.visualizer import get_trend_plot, get_countries_plot, get_genres_plot
from src.reporter import generate_pdf_report
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import src.visualizer as visualizer

# Configuración Global de Estilo
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
FONT_BOLD = ("Arial", 14, "bold")
FONT_NORMAL = ("Arial", 13)
COLOR_RED = "#E50914"

class NetflixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Netflix Data Analyzer Pro")
        self.geometry("1150x750")

        # Carga de Datos
        self.df = clean_netflix_data('data/netflix-data.csv')

        # Configuración de Rejilla Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        
        # Contenedor Principal
        self.main_container = ctk.CTkFrame(self, fg_color="#121212")
        self.main_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.mostrar_dashboard_principal()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo
        ctk.CTkLabel(self.sidebar, text="NETFLIX DATA\nANALYZER", font=("Arial", 18, "bold"), text_color=COLOR_RED).pack(pady=30)

        # Botones de Navegación
        buttons = [
            ("Inicio", self.mostrar_dashboard_principal, None),
            ("Tabla de Datos", self.mostrar_tabla, None),
            ("Estadísticas", self.mostrar_estadisticas, None),
            ("Tendencias", lambda: self.render_plot(get_trend_plot(self.df)), None),
            ("Top Países", lambda: self.render_plot(get_countries_plot(self.df)), None),
            ("Top Géneros", lambda: self.render_plot(get_genres_plot(self.df)), None),
        ]

        for text, cmd, color in buttons:
            btn = ctk.CTkButton(self.sidebar, text=text, font=FONT_NORMAL, command=cmd)
            if color: btn.configure(fg_color=color)
            btn.pack(pady=8, padx=20, fill="x")

        # Botón de Reporte al final
        self.btn_report = ctk.CTkButton(self.sidebar, text="Generar PDF", font=FONT_BOLD, fg_color="green", hover_color="darkgreen", command=self.exportar_pdf)
        self.btn_report.pack(side="bottom", pady=40, padx=20, fill="x")

    def limpiar_pantalla(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def mostrar_dashboard_principal(self):
        self.limpiar_pantalla()
        
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="RESUMEN GENERAL", font=("Arial", 22, "bold"), text_color=COLOR_RED).pack(pady=20)

        # KPIs Rapidos
        stats = get_advanced_stats(self.df)
        kpi_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=10)
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.crear_card(kpi_frame, "PELÍCULAS", f"{len(self.df[self.df['type']=='Movie'])}", 0, 0)
        self.crear_card(kpi_frame, "SERIES", f"{len(self.df[self.df['type']=='TV Show'])}", 0, 1)
        self.crear_card(kpi_frame, "PAÍSES", str(stats['paises_productores']), 0, 2)

        # Gráficos en el Home
        charts_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        charts_frame.pack(fill="both", pady=20)
        charts_frame.grid_columnconfigure((0, 1), weight=1)

        self.embed_plot(get_trend_plot(self.df), charts_frame, 0, 0)
        self.embed_plot(get_genres_plot(self.df), charts_frame, 0, 1)

    def crear_card(self, master, titulo, valor, row, col):
        card = ctk.CTkFrame(master, corner_radius=12, fg_color="#1a1a1a", border_width=1, border_color="#333333")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(card, text=titulo, font=("Arial", 11, "bold"), text_color="#888888").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=valor, font=("Arial", 24, "bold")).pack(pady=(5, 15))

    def embed_plot(self, fig, master, row, col):
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def mostrar_tabla(self):
        self.limpiar_pantalla()
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        cols_map = {'title': 'TÍTULO', 'type': 'TIPO', 'country': 'PAÍS', 'release_year': 'AÑO', 'rating': 'CALIF.'}
        df_view = self.df[list(cols_map.keys())].head(50)

        for c_idx, col in enumerate(cols_map.values()):
            ctk.CTkLabel(scroll, text=col, font=FONT_BOLD, text_color=COLOR_RED).grid(row=0, column=c_idx, padx=10, pady=10, sticky="w")

        for r_idx, (_, row) in enumerate(df_view.iterrows()):
            bg = "#1f1f1f" if r_idx % 2 == 0 else "transparent"
            for c_idx, col in enumerate(cols_map.keys()):
                txt = (str(row[col])[:25] + "...") if len(str(row[col])) > 25 else str(row[col])
                ctk.CTkLabel(scroll, text=txt, font=FONT_NORMAL, fg_color=bg, height=32, anchor="w").grid(row=r_idx+1, column=c_idx, sticky="nsew")

    def mostrar_estadisticas(self):
        self.limpiar_pantalla()
        stats = get_advanced_stats(self.df)
        
        # 1. Título
        ctk.CTkLabel(self.main_container, text="ESTADÍSTICAS DEL CATÁLOGO", font=("Arial", 24, "bold"), text_color=COLOR_RED).pack(pady=(30, 10))
        
        # 2. El Contenedor de las tarjetas
        # Al poner expand=True, este cuadro absorberá TODO el espacio sobrante de abajo
        container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=(0, 30)) 

        # 3. Configuramos para que las filas también crezcan
        container.grid_columnconfigure((0, 1, 2), weight=1)
        container.grid_rowconfigure((0, 1), weight=1) # Esto estira las tarjetas hacia abajo

        data = [
            ("DURACIÓN MEDIA", f"{stats['promedio_duracion']:.0f} min"),
            ("ESPERA (AÑOS)", f"{stats['gap_estreno']:.1f}"),
            ("DIVERSIDAD", f"{stats['paises_productores']} Países"),
            ("ANTIGÜEDAD", f"{stats['antigüedad_media']:.1f} años"),
            ("SERIES", f"{stats['porcentaje_series']:.1f}%"),
            ("ULT. AÑO", f"{stats['añadidos_ultimo_año']}")
        ]

        for i, (t, v) in enumerate(data):
            # creamos la tarjeta
            card = ctk.CTkFrame(container, corner_radius=15, fg_color="#1a1a1a", 
                                border_width=1, border_color="#333333")
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")
            
            # Esto centra el texto verticalmente dentro de la tarjeta estirada
            card.grid_rowconfigure((0,1), weight=1)
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=t, font=("Arial", 12, "bold"), text_color="#888888").grid(row=0, column=0, pady=(20,0))
            ctk.CTkLabel(card, text=v, font=("Arial", 32, "bold"), text_color="white").grid(row=1, column=0, pady=(0,20))

    def crear_card_expandida(self, master, titulo, valor, row, col):
        card = ctk.CTkFrame(master, corner_radius=15, fg_color="#1a1a1a", 
                            border_width=1, border_color="#333333")
        # sticky="nsew" hace que la card se pegue a los 4 bordes de su celda
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Usamos expand=True dentro de la card para que los textos se centren verticalmente
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(expand=True)
        
        ctk.CTkLabel(inner_frame, text=titulo, font=("Arial", 12, "bold"), text_color="#888888").pack(pady=5)
        ctk.CTkLabel(inner_frame, text=valor, font=("Arial", 32, "bold"), text_color="white").pack(pady=5)

    def crear_card_expandida(self, master, titulo, valor, row, col):
        # Quitamos anchos fijos para que el grid mande
        card = ctk.CTkFrame(master, corner_radius=15, fg_color="#1a1a1a", 
                            border_width=1, border_color="#333333")
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Centramos el contenido dentro de la tarjeta
        ctk.CTkLabel(card, text=titulo, font=("Arial", 12, "bold"), text_color="#888888").pack(pady=(30, 5), padx=10)
        ctk.CTkLabel(card, text=valor, font=("Arial", 30, "bold"), text_color="white").pack(pady=(0, 30), padx=10)

    def render_plot(self, fig):
        self.limpiar_pantalla()
        canvas = FigureCanvasTkAgg(fig, master=self.main_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def exportar_pdf(self):
        ruta = generate_pdf_report(self.df, visualizer)
        self.btn_report.configure(text="¡PDF Generado!")
        self.after(3000, lambda: self.btn_report.configure(text="Generar PDF"))

if __name__ == "__main__":
    app = NetflixApp()
    app.mainloop()