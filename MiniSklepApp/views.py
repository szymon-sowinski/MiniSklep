from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

@login_required
def display_products(request):
    if not request.user.is_staff: 
        return redirect('login')

    products = Product.objects.all()
    return render(request, 'display_products.html', {'products': products})

@csrf_exempt
def update_product(request):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=request.POST["id"])
            setattr(product, request.POST["field"], request.POST["value"])
            product.save()
            return HttpResponse("success")
        except Exception:
            return HttpResponse("error")

def delete_product(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return HttpResponse("success")
        except Product.DoesNotExist:
            return HttpResponse("error")
    return HttpResponse("error")
    
@csrf_exempt
def delete_selected_products(request):
    if request.method == "POST":
        ids = request.POST.get("ids", "")
        if ids:
            ids_list = ids.split(",")
            Product.objects.filter(id__in=ids_list).delete()
            return HttpResponse("success")
    return HttpResponse("error")

def delete_all_products(request):
    if request.method == "POST":
        Product.objects.all().delete()
        return redirect('display_products')
    return HttpResponse("error")
