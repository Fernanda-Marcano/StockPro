from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.db.models import Q
from django.contrib import messages

from .models import Hierarchy, Value, Product, Sale
from .forms import HierarchyForm, ValueForm, ProductForm, SaleForm


#* ------------- Definition of views Hierarchy --------------- *#
class HierarchyCreateView(LoginRequiredMixin, CreateView):
    model = Hierarchy
    form_class = HierarchyForm
    template_name = "hierarchy/form.html"
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form_hierarchy'] = self.form_class
        context['title'] = 'crear jerarquía'
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Información creada exitosamente')
                return redirect(to='list-hierarchy')
            else:
                messages.error(request, 'Ha ocurrido un error')
                return render(request, self.template_name, {'form_hierarchy':form})
        except Exception as e:
            print(f'Se ha producido el siguiente error {e}')


class HierarchyListView(LoginRequiredMixin, ListView):
    model = Hierarchy
    template_name = "hierarchy/list.html"
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = {}
        context['list_hierarchy'] = self.get_queryset()
        context['title'] = 'Lista de Jerarquías'
        context['title2'] = 'crear jerarquía'
        context['form_hierarchy'] = HierarchyForm()
        return context


class HierarchyUpdateView(LoginRequiredMixin, UpdateView):
    model = Hierarchy
    form_class = HierarchyForm
    template_name = "hierarchy/form.html"
    success_url = reverse_lazy('list-hierarchy')
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form_hierarchy'] = self.get_form()
        context['title'] = 'actualizar jerarquía'
        return context


def HierarchyDeleteView(request, pk):
    try:
        hierar = Hierarchy.objects.get(hierar_id = pk)
        hierar.delete()
        messages.success(request, 'Eliminado correctamente')
        return redirect(to='list-hierarchy')
    except Exception as e:
        print(f'Se ha producido el siguiente error {e}')

#* ------------- Definition of views Value --------------- *#
class ValueCreateView(LoginRequiredMixin, CreateView):
    model = Value
    form_class = ValueForm
    template_name = "value/form.html"
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form_value'] = self.form_class
        context['title'] = 'crear valor'
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Información creada exitosamente')
                return redirect(to='list-hierarchy')
            else:
                messages.error(request, 'Ha ocurrido un error')
                return render(request, self.template_name, {'form_value':form})
        except Exception as e:
            print(f'Se ha producido el siguiente error {e}')

class ValueCreateIdView(LoginRequiredMixin, CreateView):
    model = Value
    form_class = ValueForm
    template_name = "value/form.html"
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        query = self.model.objects.filter(hierar_id=pk)
        return query
    
    def get_context_data(self, **kwargs):
        context = {}
        pk = self.kwargs.get('pk')
        context['title'] = 'Crear valor de jerarquia'
        context['val_hierar'] = Hierarchy.objects.get(hierar_id=pk)
        context['form_value'] = self.form_class(initial={'hierar_id': context['val_hierar']})
        return context


class ValueListView(LoginRequiredMixin, ListView):
    model = Value
    template_name = "value/list.html"
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = {}
        context['list_value'] = self.get_queryset()
        context['title'] = 'lista de valores'
        return context


class ValueListIdView(LoginRequiredMixin, ListView): 
    model = Value 
    template_name = "value/list.html" 
    
    def get_queryset(self): 
        pk = self.kwargs.get('pk') 
        queryset = self.model.objects.filter(hierar_id=pk)
        return queryset 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        pk = self.kwargs.get('pk') 
        context['list_value'] = self.get_queryset() 
        context['title'] = 'lista de valores' 
        context['val_hierar'] = Hierarchy.objects.get(hierar_id=pk)
        return context


class ValueUpdateView(LoginRequiredMixin, UpdateView):
    model = Value
    form_class = ValueForm
    template_name = "value/form.html"
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form_value'] = self.get_form()
        context['title'] = 'actualizar valor'
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Información actualizada exitosamente')
                return redirect(to='list-hierarchy')
            else:
                messages.error(request, 'Ha ocurrido un error')
                return render(request, self.template_name, {'form_value':form})
        except Exception as e:
            print(f'Ha ocurrido el siguiente error {e}')


def ValueDeleteView(request, pk):
    try:
        val = Value.objects.get(val_id = pk)
        val.delete()
        messages.success(request, 'Eliminado correctamente')
        return redirect(to='list-hierarchy')
    except Exception as e:
        print(f'Se ha producido el siguiente error {e}')



#* ------------- Definition of views Product --------------- *#
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/form.html"
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form_product'] = self.form_class
        context['title'] = 'crear producto'
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Información creada exitosamente')
                return redirect(to='list-product')
        except Exception as e:
            print(f'Ha ocurrido el siguiente error {e}')


class ProductListView(ListView):
    model = Product
    template_name = "product/list.html"
    
    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = {}
        context['list_product'] = self.get_queryset()
        context['title'] = 'lista de productos'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/detail.html"
    
    def get_queryset(self):
        pk = self.kwargs.get('pk') 
        queryset = self.model.objects.filter(pdt_id=pk)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['d_product'] = self.get_queryset()
        context['sale_form'] = SaleForm()
        context['title'] = 'detalle del producto'
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            form = SaleForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto agregado correctamente')
                return redirect('list-product')
            else:
                messages.error(request, 'Ha ocurrido un error')
                return render(request, 'product/detail.html', {'sale_form':form})
        except Exception as e:
            print(f'Ha ocurrido el siguiente error {e}')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/form.html"
    success_url = reverse_lazy('list-product')
    
    def get_context_data(self, **kwargs):
        context = {}
        context['form_product'] = self.get_form()
        context['title'] = 'actualizar producto'
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                form.save()
                messages.success(request, 'Información actualizada exitosamente')
                return redirect(to='list-product')
            else:
                print(form.errors)
                messages.error(request, 'Ha ocurrido un error')
                return render(request, self.template_name, {'form_product': form})
        except Exception as e:
            print(f'Ha ocurrido el siguiente error {e}')

def DeleteProductView(request, pk):
    try:
        product = Product.objects.get(pdt_id=pk)
        product.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect(to='list-product')
    except Exception as e:
        print(f'Ha ocurrido un error {e}')



#* ------------- Definition of views Sale --------------- *#
class SaleDetailView(DetailView):
    model = Sale
    template_name = "sale/detail.html"
    
    def get_queryset(self, pk):
        queryset = self.model.objects.get(sale_id=pk)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = {}
        context['d_sale'] = self.get_queryset()
        context['title'] = 'detalle de la venta'
        return context


#* ------------- Definition of views Inventory --------------- *#
class InventoryProductView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.model.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inventario'
        context['invent_product'] = self.get_queryset()
        return context