from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.core.paginator import Paginator

def index(request):
    return render(request, 'base.html', {})


def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 2)
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    return render(request,'Product/product_list.html',{'product_list':product_list})

def product_details(request,slug):
    data = Product.objects.get(PRDSlug=slug)
    return render(request,'Product/product_details.html',{'product_details':data})



