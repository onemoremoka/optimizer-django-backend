import pandas as pd
import pyomo.environ as pyo

class OptimizationModel:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.model = pyo.ConcreteModel()
        self._results = None

    def build_model_optimazer(self):

        # parametros
        row = self.data.iloc[0]
        self.model.P_A = pyo.Param(initialize=row['Price_Product_A'])
        self.model.P_B = pyo.Param(initialize=row['Price_Product_B'])
        self.model.T_A1 = pyo.Param(initialize=row['Product_A_Production_Time_Machine_1'])
        self.model.T_A2 = pyo.Param(initialize=row['Product_A_Production_Time_Machine_2'])
        self.model.T_B1 = pyo.Param(initialize=row['Product_B_Production_Time_Machine_1'])
        self.model.T_B2 = pyo.Param(initialize=row['Product_B_Production_Time_Machine_2'])
        self.model.T_M1 = pyo.Param(initialize=row['Machine_1_Available_Hours'])
        self.model.T_M2 = pyo.Param(initialize=row['Machine_2_Available_Hours'])

        # variables de decision
        self.model.x_A = pyo.Var(domain=pyo.NonNegativeIntegers) # esto indica la restriccion de no negatividad
        self.model.x_B = pyo.Var(domain=pyo.NonNegativeIntegers) # esto indica la restriccion de no negatividad

        # funcion objetivo
        def objective(model):
            return model.P_A * model.x_A + model.P_B * model.x_B # Por lo datos: 100 * x_A + 80 * x_B

        self.model.objective = pyo.Objective(rule=objective, sense=pyo.maximize)

        # restricciones
        def machine_1_constraint(model):
            return model.T_A1 * model.x_A + model.T_B1 * model.x_B <= model.T_M1
        
        def machine_2_constraint(model):
            return model.T_A2 * model.x_A + model.T_B2 * model.x_B <= model.T_M2
        
        def no_negative_constraint(model):
            return model.x_A >= 0 and model.x_B >= 0
        
        self.model.machine_1_constraint = pyo.Constraint(rule=machine_1_constraint)
        self.model.machine_2_constraint = pyo.Constraint(rule=machine_2_constraint)

    def solve(self):
        """Resuelve el modelo de optimización y valida las restriccionse"""

        solver = pyo.SolverFactory('glpk', executable='/usr/bin/glpsol')
        results = solver.solve(self.model)

        if results.solver.termination_condition != pyo.TerminationCondition.optimal:
            raise ValueError("No se pudo encontrar una solución óptima.")

        # Validación de restricciones ya definidas
        epsilon = 1e-6
        c1 = self.model.machine_1_constraint
        c2 = self.model.machine_2_constraint

        if pyo.value(c1.body) > pyo.value(c1.upper) + epsilon:
            raise ValueError("No se cumple la restricción de máquina 1")

        if pyo.value(c2.body) > pyo.value(c2.upper) + epsilon:
            raise ValueError("No se cumple la restricción de máquina 2")

        # Guardar resultados
        self._results = pd.DataFrame({
            'Product_A': [round(self.model.x_A.value, 6)],
            'Product_B': [round(self.model.x_B.value, 6)],
            'Objective_Value': [round(pyo.value(self.model.objective), 6)],
        })

    @property
    def results(self) -> pd.DataFrame:
        """Acceso controlado a los resultados de la optimización."""
        if self._results is None:
            raise ValueError("Aun no se han calculado los resultados.")
        return self._results
    
      