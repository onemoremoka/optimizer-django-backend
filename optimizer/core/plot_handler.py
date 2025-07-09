
import io
import base64
import matplotlib
import pandas as pd
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from optimizer.models import OptimizationResult

class PlotHandler:
    # por construccion esta clase toma el historial de consultas. No se pasa un dataframe de entrada.
    sns.set_theme(style="darkgrid", palette="deep", font_scale=0.9)
    def __init__(self):
        # cargar todos los resultados de la base de datos
        self.df = pd.DataFrame.from_records(
            OptimizationResult.objects.all().values()
        ).sort_values('timestamp')

    def plot_objective_over_time(self):
        # el eje x es un contador que refleja el numero del experimento
        plt.figure(figsize=(8, 4))
        sns.lineplot(data=self.df, x='id', y='objective_value', marker='o')
        plt.ylim(0 - (self.df['objective_value'].max() * 0.1), self.df['objective_value'].max() * 1.1)
        plt.title('Valor Objetivo Experimentos')
        plt.xlabel('Número de Experimento')
        plt.ylabel('Valor Objetivo')
        return self._get_image_base64()

    def plot_products(self):
        plt.figure(figsize=(8, 4))
        sns.lineplot(data=self.df, x='id', y='product_a', label='Product A', marker='o')
        sns.lineplot(data=self.df, x='id', y='product_b', label='Product B', marker='s')

        plt.title('Producción Optimizada')
        plt.xlabel('Número de Experimento')
        
        # x label: 5:10:15
        plt.xticks(self.df['id'][::5]-1)
        plt.ylabel('Cantidad')
        plt.legend()
        return self._get_image_base64()

    def plot_solver_time(self):
        plt.figure(figsize=(8, 4))
        sns.lineplot(data=self.df, x='id', y='solve_time', marker='o', color='orange')
        plt.ylim(0 - (self.df['solve_time'].max() * 0.1), self.df['solve_time'].max() * 1.1)
        plt.xticks(self.df['id'][::5]-1)
        plt.title('Tiempo de Resolución del Solver')
        plt.xlabel('Número de Experimento')
        plt.ylabel('Tiempo (s)')
        return self._get_image_base64()

    def _get_image_base64(self):
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
