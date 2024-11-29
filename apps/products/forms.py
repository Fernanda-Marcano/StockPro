from django import forms
from models import Hierarchy, Value, Product, Sale


class HierarchyForm(forms.ModelForm):
    """Form definition for Hierarchy."""
    hierar_sup = forms.ModelChoiceField(queryset=Hierarchy.objects.all(), label='Jerarquía Superior', empty_label=None, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        """Meta definition for Hierarchyform."""

        model = Hierarchy
        exclude = ['hierar_id']
        labels = {
            'hierar_name':'Nombre de la Jerarquía',
            'hierar_description':'Descripción de Jerarquía',
            'hierar_icon':'Icono de la Jerarquía'
        }


class ValueForm(forms.ModelForm):
    """Form definition for Value."""
    val_sup = forms.ModelChoiceField(queryset=Value.objects.all(), label='Valor Superior', empty_label=None, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    hierar_id = forms.ModelChoiceField(queryset=Hierarchy.objects.all(), label='Jerarquía', empty_label=None, required=True, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        """Meta definition for Valueform."""

        model = Value
        exclude = ['val_id']
        labels = {
            'val_name':'Nombre del Valor', 
            'val_description':'Descripción del Valor',
            'val_icon':'Icono del Valor', 
            'val_order':'Orden del Valor'
        }


class ProductForm(forms.ModelForm):
    """Form definition for Product."""
    id_product = forms.ModelChoiceField(queryset=Value.objects.all(), label='Tipo Producto', empty_label=None, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    id_category = forms.ModelChoiceField(queryset=Value.objects.all(), label='Categoría', empty_label=None, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    id_brand = forms.ModelChoiceField(queryset=Value.objects.all(), label='Marca', empty_label=None, required=True, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        """Meta definition for Productform."""

        model = Product
        exclude = ['pdt_id']
        labels = {
            'pdt_model':'Modelo del Producto',
            'pdt_name':'Nombre del Producto', 
            'pdt_serial':'Serial del Producto', 
            'pdt_stock':'Cantidad de Producto', 
            'pdt_price':'Precio del Producto', 
            'pdt_description':'Descripción del Producto', 
            'pdt_image':'Imagen del Producto'
        }


class SaleForm(forms.ModelForm):
    """Form definition for Sale."""
    product_id = forms.ModelChoiceField(queryset=Product.objects.all(), label='Producto', empty_label=None, required=True, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        """Meta definition for Saleform."""

        model = Sale
        exclude = ['sale_id', 'sale_date']
        labels = {
            'sale_quantity':'Cantidad de Venta',
        }


