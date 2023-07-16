from django import forms


class ProductCSVImportForm(forms.Form):
    csv_file_product = forms.FileField()
