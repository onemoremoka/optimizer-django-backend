from abc import ABC, abstractmethod
import pandas as pd
import os

class ResultsHandler(ABC):
    """Clase base abstracta para procesar y presentar resultados."""
    def __init__(self, results: dict):
        self.results = results

    @abstractmethod
    def display(self):
        pass

    def flatted_results(self):
        """Convierte los resultados en un formato plano para facilitar su uso. Solo mapea la informacion base necesaria."""

        # cada Handler puede complementar este output o pasarlo directamente
        return {
                "Product_A": self.results["variables"]["Product_A"],
                "Product_B": self.results["variables"]["Product_B"],
                "Objective": self.results["objective_value"],
                "M1_LHS": self.results["constraints"]["machine_1"]["lhs"], # LHS (left-hand side) de la restriccion 1
                "M1_RHS": self.results["constraints"]["machine_1"]["rhs"], # RHS (right-hand side) de la restriccion 1
                "M2_LHS": self.results["constraints"]["machine_2"]["lhs"], # same
                "M2_RHS": self.results["constraints"]["machine_2"]["rhs"], # same
                "Status": self.results["solver_status"],
                "Termination": self.results["termination_condition"]
            }


class TerminalResultsHandler(ResultsHandler):

    def display(self):
        print("Variables:")
        for var, val in self.results.get("variables", {}).items():
            print(f"  {var}: {val}")

        print("\nObjetivo:")
        print(f"  {self.results.get('objective_value')}")

        print("\nRestricciones:")
        for name, c in self.results.get("constraints", {}).items():
            print(f"  {name}: {c['lhs']} <= {c['rhs']}")

        print("\nSolver:")
        print(f"  Status: {self.results.get('solver_status')}")
        print(f"  Termination: {self.results.get('termination_condition')}")

class FileResultsHandler(ResultsHandler):
    def __init__(self, results: dict, file_path: str):
        super().__init__(results)
        self.file_path = file_path

    def display(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        data = self.flatted_results()
        pd.DataFrame([data]).to_csv(self.file_path, index=False)
        return f"Guardado en {self.file_path}"


class HtmlResultsHandler(ResultsHandler):
    def __init__(self, results: dict, style: str = "table"):
        super().__init__(results)
        self.style = style

    def display(self):
        data = self.flatted_results()

        # se añade otra info disponible
        data['Time'] = self.results["raw_solver_output"]["Solver"][0]["Time"]
        data['Error_rc'] = self.results["raw_solver_output"]["Solver"][0].get("Error_rc")

        df = pd.DataFrame([data])
        return df.to_html(index=False, justify='center', classes=self.style)
