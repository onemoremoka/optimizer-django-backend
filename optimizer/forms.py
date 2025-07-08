from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Sube el archivo CSV con los datos del problema")