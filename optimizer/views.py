from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from optimizer.core.data_loader import DataLoader
from optimizer.core.optimization_model import OptimizationModel
from optimizer.core.results_handler import HtmlResultsHandler
from optimizer.core.plot_handler import PlotHandler
from .models import OptimizationResult


def optimize_view(request):
    context = {}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Leer archivo CSV
                data_loader = DataLoader(request.FILES['file'])
                df = data_loader.run()

                # Construir y resolver modelo
                model = OptimizationModel(df)
                model.build_model_optimizer()
                model.solve()

                results = model.results
                html_handler = HtmlResultsHandler(results)
                results_html = html_handler.display()

                # Guardar resultados en base de datos
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

                # Guardar resultado temporalmente en la sesión y redirigir
                request.session['results_html'] = results_html
                return redirect(reverse('optimize'))

            except Exception as e:
                context['error'] = str(e)
        else:
            context['error'] = 'Formulario inválido.'
        context['form'] = form

    else:
        form = UploadFileForm()
        context['form'] = form

        # Si hay resultados guardados en sesión desde un POST previo
        if 'results_html' in request.session:
            context['results_html'] = request.session.pop('results_html')

    # Graficar (siempre se muestran)
    plots = PlotHandler()
    context['objective_plot'] = plots.plot_objective_over_time()
    context['product_plot'] = plots.plot_products()
    context['solver_time_plot'] = plots.plot_solver_time()

    return render(request, 'layouts/optimizer.html', context)
