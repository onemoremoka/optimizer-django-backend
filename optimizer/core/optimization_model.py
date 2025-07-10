import pandas as pd
import pyomo.environ as pyo

class OptimizationModel:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.model = pyo.ConcreteModel()
        self._results = None

    def build_model_optimizer(self):

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
        self.model.x_A = pyo.Var(domain=pyo.NonNegativeIntegers) # restriccion de no negatividad implicita en la definicion de la variable
        self.model.x_B = pyo.Var(domain=pyo.NonNegativeIntegers) # restriccion de no negatividad implicita en la definicion de la variable

        # funcion objetivo
        def objective(model):
            return model.P_A * model.x_A + model.P_B * model.x_B # Por lo datos seria100 * x_A + 80 * x_B

        self.model.objective = pyo.Objective(rule=objective, sense=pyo.maximize)

        # restricciones
        def machine_1_constraint(model):
            return model.T_A1 * model.x_A + model.T_B1 * model.x_B <= model.T_M1
        
        def machine_2_constraint(model):
            return model.T_A2 * model.x_A + model.T_B2 * model.x_B <= model.T_M2
        
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

        # Guardar todos los resultados simulando "raw_format"
        self._results = {
            'variables': {
                'Product_A': self.model.x_A.value,
                'Product_B': self.model.x_B.value
            },
            'objective_value': pyo.value(self.model.objective),
            'constraints': {
                'machine_1': {
                    'lhs': pyo.value(c1.body),
                    'rhs': pyo.value(c1.upper)
                },
                'machine_2': {
                    'lhs': pyo.value(c2.body),
                    'rhs': pyo.value(c2.upper)
                }
            },
            'solver_status': str(results.solver.status),
            'termination_condition': str(results.solver.termination_condition),
            'raw_solver_output': results
        }

    @property
    def results(self) -> dict:
        """Acceso controlado a los resultados de la optimización."""
        if self._results is None:
            raise ValueError("Aun no se han calculado los resultados.")
        return self._results
    
      