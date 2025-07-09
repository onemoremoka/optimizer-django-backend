import pandas as pd

class DataLoader:

    REQUIRED_COLUMNS = [
        'Product_A_Production_Time_Machine_1',
        'Product_A_Production_Time_Machine_2',
        'Product_B_Production_Time_Machine_1',
        'Product_B_Production_Time_Machine_2',
        'Machine_1_Available_Hours',
        'Machine_2_Available_Hours',
        'Price_Product_A',
        'Price_Product_B'
    ]
    
    # en este caso coinciden
    NUMERICAL_COLUMNS = REQUIRED_COLUMNS

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._data = None

    def run(self) -> pd.DataFrame:
        """ Inicia el Pipeline de carga de datos y devuelve un DataFrame en caso de no haber una excepcion"""
        self._load_data()
        self._validate_columns()
        self._validate_datatypes()

           # Validaciones
        if self._data.empty:
            raise ValueError("El archivo CSV está vacío.")

        if (self._data[['Price_Product_A', 'Price_Product_B']] < 0).any().any():
            raise ValueError("Los precios no pueden ser negativos.")

        if (self._data[['Machine_1_Available_Hours', 'Machine_2_Available_Hours']] <= 0).any().any():
            raise ValueError("Las horas disponibles deben ser mayores que cero.")
        return self.data

    def _load_data(self):
        """Carga los datos desde el archivo especificado."""
        try:
            self._data = pd.read_csv(self.file_path)
        except Exception as e:
            raise ValueError(f"Error loading data from {self.file_path}: {e}")
        

    def _validate_columns(self):
        """Verifica que existan todas las columnas requeridas."""
        missing = [col for col in self.REQUIRED_COLUMNS if col not in self._data.columns]
        if missing:
            raise ValueError(f"Faltan columnas requeridas: {', '.join(missing)}")

        # se trabaja unicamente con las cols necesarias
        self._data = self._data[self.REQUIRED_COLUMNS]

    def _validate_datatypes(self):
        """Convierte y valida tipos numéricos para las columnas correspondientes (sin for)."""
        try:
            self.data[self.NUMERICAL_COLUMNS] = self.data[self.NUMERICAL_COLUMNS].apply(
                pd.to_numeric, errors='raise'
            )
        except Exception as e:
            raise ValueError(f"Error al convertir columnas numéricas: {e}")

    @property
    def data(self) -> pd.DataFrame:
        """Acceso controlado al DataFrame"""
        if self._data is None:
            raise ValueError("Los datos aún no han sido cargados. Usa run() primero.")
        return self._data