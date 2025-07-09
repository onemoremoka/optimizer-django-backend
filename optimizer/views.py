from django.shortcuts import render
from .forms import UploadFileForm
from optimizer.core.data_loader import DataLoader
from optimizer.core.optimization_model import OptimizationModel
from optimizer.core.results_handler import HtmlResultsHandler
#modelo
from .models import OptimizationResult
from optimizer.core.plot_handler import PlotHandler

def optimize_view(request):
    context = {}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # leer archivo CSV directamente desde request.FILES
                data_loader = DataLoader(request.FILES['file'])
                df = data_loader.run()

                # construir y resolver el modelo
                model = OptimizationModel(df)
                model.build_model_optimizer()
                model.solve()

                results = model.results
                html_handler = HtmlResultsHandler(results)
                context['results_html'] = html_handler.display()

                OptimizationResult.objects.create(
                    product_a=results['variables']['Product_A'],
                    product_b=results['variables']['Product_B'],
                    objective_value=results['objective_value'],
                    machine_1_lhs=results['constraints']['machine_1']['lhs'],
                    machine_1_rhs=results['constraints']['machine_1']['rhs'],
                    machine_2_lhs=results['constraints']['machine_2']['lhs'],
                    machine_2_rhs=results['constraints']['machine_2']['rhs'],
                    status=results['solver_status'],
                    termination=results['termination_condition'],
                    solve_time=results['raw_solver_output']['Solver'][0]['Time'],
                    error_rc=results['raw_solver_output']['Solver'][0].get('Error_rc', None)
                )


            except Exception as e:
                context['error'] = str(e)
    else:
        form = UploadFileForm()


    context['form'] = form
    plots = PlotHandler()
    context['objective_plot'] = plots.plot_objective_over_time()
    context['product_plot'] = plots.plot_products()
    context['solver_time_plot'] = plots.plot_solver_time()
    return render(request, 'layouts/optimizer.html', context)
