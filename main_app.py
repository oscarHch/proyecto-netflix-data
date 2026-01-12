import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.exploration import clean_netflix_data
from src.visualizer import get_trend_plot, get_countries_plot, get_genres_plot # Importamos los gráficos
from src.reporter import generate_pdf_report
import src.visualizer as visualizer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NetflixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Netflix Data Analyzer Pro")
        self.geometry("1100x700")

        self.df = clean_netflix_data('data/netflix-data.csv')

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="NETFLIX DATA\nANALYZER", font=("Arial", 20, "bold"), text_color="#E50914", justify="center")
        self.logo.pack(pady=20, padx=10)

        # Botones que llaman a visualizer
        ctk.CTkButton(self.sidebar, text="Tendencias", font=("Arial", 13, "bold"), command=lambda: self.render_plot(get_trend_plot(self.df))).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Top Países", font=("Arial", 13, "bold"), command=lambda: self.render_plot(get_countries_plot(self.df))).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Top Géneros", font=("Arial", 13, "bold"), command=lambda: self.render_plot(get_genres_plot(self.df))).pack(pady=10, padx=20)

        self.btn_report = ctk.CTkButton(self.sidebar, text="Generar PDF", font=("Arial", 13, "bold"), fg_color="green", hover_color="darkgreen", command=self.exportar_pdf)
        self.btn_report.pack(pady=40, padx=20)

        # Contenedor para gráficos
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, padx=(30, 20), pady=20, sticky="nsew")

    def exportar_pdf(self):
        ruta = generate_pdf_report(self.df, visualizer)

        print(f"Reporte generado: {ruta}")
        self.btn_report.configure(text=f"PDF generado")
        self.after(3000, lambda: self.btn_report.configure(text="Generar PDF", fg_color="green"))

    def render_plot(self, fig):

        # Limpiar frame anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Crear canvas
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
    
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, anchor="center")

if __name__ == "__main__":
    app = NetflixApp()
    app.mainloop()