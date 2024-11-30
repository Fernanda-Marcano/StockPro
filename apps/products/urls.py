from django.urls import path
from . import views

urlpatterns = [
    #* ================= HIERARCHY URLS ================== *#
    path('create-hierar/', views.HierarchyCreateView.as_view(), name='create-hierarchy'),
    path('list-hierar/', views.HierarchyListView.as_view(), name='list-hierarchy'),
    path('update-hierar/<int:pk>/', views.HierarchyUpdateView.as_view(), name='update-hierarchy'),
    
    #* ================= VALUE URLS ================== *#
    path('create-val/', views.ValueCreateView.as_view(), name='create-value'), 
    path('list-val/', views.ValueListView.as_view(), name='list-value'),
    path('update-val/<int:pk>/', views.ValueUpdateView.as_view(), name='update-value'),
    
    #* ================= PRODUCT URLS ================== *#
    path('create-pdt/', views.ProductCreateView.as_view(), name='create-product'), 
    path('list-pdt/', views.ProductListView.as_view(), name='list-product'),
    path('detail-pdt/<int:pk>/', views.ProductDetailView.as_view(), name='detail-product'),
]