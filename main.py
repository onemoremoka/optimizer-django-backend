from optimizer.core.data_loader import DataLoader
from optimizer.core.optimization_model import OptimizationModel
from optimizer.core.results_handler import TerminalResultsHandler, FileResultsHandler, HtmlResultsHandler

# este archivo se uso para validar la logica del backend antes de integrar Django y Docker
def main():
    file_path = "data/optimization_problem_data.csv"
    data_loader = DataLoader(file_path)

    try:
        data = data_loader.run()
        opt_model = OptimizationModel(data)
        opt_model.build_model_optimizer()
        opt_model.solve()
        results = opt_model.results

        # display en terminal
        TerminalResultsHandler(results).display()

        # display en un .csv
        FileResultsHandler(results, "results/optimization_results.csv").display()

        # display info en formato json para HTML
        HtmlResultsHandler(results).display()

        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()