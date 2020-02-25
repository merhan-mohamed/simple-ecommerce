from django.urls import path

from .views import product_list, product_details, index
app_name = 'products'

urlpatterns = [
    path('', product_list,name='product'),
    path('product_details/<slug:slug>/', product_details, name='product_details'),
    path('index/', index, name='index'),



]





