#formulario de registro ventas

from django import forms
from .models import DetalleVenta, Venta

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'subtotal']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['fecha_venta','cliente']
        widgets = {
            'fecha_venta': forms.DateInput(attrs={'type': 'date'}),
        }