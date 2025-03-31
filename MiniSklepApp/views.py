from django.shortcuts import render, redirect
from .models import Product

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')

        if name:
            Product.objects.create(name=name, price=price)
            return redirect('/add_product/')

    products = Product.objects.all()
    return render(request, 'add_product.html', {'products': products})

def display_products(request):
    message = ''
    
    products = Product.objects.all()
    return render(request, 'display_products.html', {'products': products, 'message': message})
