import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm
from optimizer.core.data_loader import DataLoader
from optimizer.core.optimization_model import OptimizationModel
from optimizer.core.results_handler import HtmlResultsHandler

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
                model.build_model_optimazer()
                model.solve()

                results = model.results
                html_handler = HtmlResultsHandler(results)
                context['results_html'] = html_handler.display()

            except Exception as e:
                context['error'] = str(e)
    else:
        form = UploadFileForm()

    context['form'] = form
    return render(request, 'optimizer/optimizer.html', context)

