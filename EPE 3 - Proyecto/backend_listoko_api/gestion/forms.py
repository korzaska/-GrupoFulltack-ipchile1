from django import forms
from .models import MovimientoInventario, ProductoBodega


class MovimientoForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=[('ENTRADA', 'Entrada'), ('SALIDA', 'Salida')],
        label='Tipo'
    )

    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'tipo', 'cantidad']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = ProductoBodega.objects.order_by('codigo')


class ProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoBodega
        fields = ['codigo', 'nombre', 'categoria', 'stock_actual']
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'categoria': 'Categoría',
            'stock_actual': 'Stock inicial',
        }
