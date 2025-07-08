from abc import ABC, abstractmethod
import pandas as pd

class ResultsHandler(ABC):
    """Clase base abstracta para procesar y presentar resultados."""
    def __init__(self, results: pd.DataFrame):
        self.results = results

    @abstractmethod
    def display(self):
        pass

class TerminalResultsHandler(ResultsHandler):
    def display(self):
        print(f"Resultados de la optimización:\n\n{self.results.to_string(index=False)}")

class FileResultsHandler(ResultsHandler):
    def __init__(self, results: pd.DataFrame, file_path: str):
        super().__init__(results)
        self.file_path = file_path

    def display(self):
        try:
            self.results.to_csv(self.file_path, index=False)
            print(f"Resultados guardados en {self.file_path}")
        except Exception as e:
            print(f"Error al guardar los resultados en {self.file_path}: {e}")

class HtmlResultsHandler(ResultsHandler):
    def __init__(self, results: pd.DataFrame, style: str = "table"):
        super().__init__(results)
        self.style = style

    def display(self):
        return self.results.to_html(classes=self.style, index=False)