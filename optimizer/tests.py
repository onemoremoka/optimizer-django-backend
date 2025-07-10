import pytest
import pandas as pd
from optimizer.core.optimization_model import OptimizationModel
from optimizer.core.data_loader import DataLoader
import tempfile


DATA_SAMPLE = pd.DataFrame([{
        'Product_A_Production_Time_Machine_1': 2,
        'Product_A_Production_Time_Machine_2': 1,
        'Product_B_Production_Time_Machine_1': 1,
        'Product_B_Production_Time_Machine_2': 2,
        'Machine_1_Available_Hours': 100,
        'Machine_2_Available_Hours': 80,
        'Price_Product_A': 100,
        'Price_Product_B': 80
    }])

@pytest.fixture
def temp_csv_file():
    def _save_csv(df: pd.DataFrame) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w") as tmp:
            df.to_csv(tmp.name, index=False)
            return tmp.name
    return _save_csv

@pytest.fixture
def valid_input_df():
    data = {
        "Price_Product_A": [100],
        "Price_Product_B": [80],
        "Product_A_Production_Time_Machine_1": [2],
        "Product_A_Production_Time_Machine_2": [1],
        "Product_B_Production_Time_Machine_1": [1],
        "Product_B_Production_Time_Machine_2": [2],
        "Machine_1_Available_Hours": [100],
        "Machine_2_Available_Hours": [80],
    }
    return pd.DataFrame(data)

# ModelOptimizer
def test_model_builds(valid_input_df):
    model = OptimizationModel(valid_input_df)
    model.build_model_optimizer()
    assert model.model is not None
    assert hasattr(model.model, "objective")


def test_model_solves(valid_input_df):
    print(valid_input_df)
    model = OptimizationModel(valid_input_df)
    model.build_model_optimizer()
    model.solve()

    results = model.results
    assert results["solver_status"] == "ok"
    assert results["termination_condition"] == "optimal"
    assert results["objective_value"] > 0
    assert results["variables"]["Product_A"] >= 0
    assert results["variables"]["Product_B"] >= 0

# Dataloader
def test_dataloader_missing_column(temp_csv_file):
    df = DATA_SAMPLE.drop(columns=['Product_A_Production_Time_Machine_2'])
    file_path = temp_csv_file(df)
    loader = DataLoader(file_path)
    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        loader.run()

def test_dataloader(temp_csv_file):
    # test buen funcionamiento del DataLoader
    file_path = temp_csv_file(DATA_SAMPLE)
    loader = DataLoader(file_path)
    result = loader.run()
    assert not result.empty

def test_dataloader_error_input(temp_csv_file):
    # modifico el tipo de dato de una columna numérica a string
    DATA_SAMPLE['Price_Product_A'] = [-1]
    file_path = temp_csv_file(DATA_SAMPLE)
    loader = DataLoader(file_path)
    with pytest.raises(ValueError, match="Los precios no pueden ser negativos."):
        loader.run()

def test_dataloader_typedata_input(temp_csv_file):
    # modifico el tipo de dato de una columna numérica a string
    DATA_SAMPLE['Product_A_Production_Time_Machine_1'] = ["x"]
    file_path = temp_csv_file(DATA_SAMPLE)
    loader = DataLoader(file_path)
    with pytest.raises(ValueError, match="Error al convertir columnas numéricas"):
        loader.run()
