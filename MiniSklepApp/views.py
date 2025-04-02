from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add_product')
        else:
            return render(request, 'login.html', {'error': 'Nieprawidłowe dane logowania'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_product(request):
    if not request.user.is_staff: 
        return redirect('login')

    message = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        if name:
            Product.objects.create(name=name, price=price)
            message = "Produkt został dodany pomyślnie!"
            return redirect('add_product')

    products = Product.objects.all()
    return render(request, 'add_product.html', {'products': products, 'message': message})

def display_products(request):
    products = Product.objects.all()
    return render(request, 'display_products.html', {'products': products})
