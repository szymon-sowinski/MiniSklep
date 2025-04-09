from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

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

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        if name:
            Product.objects.create(name=name, price=price)
            request.session['message'] = "Produkt został dodany pomyślnie!"
            return redirect('add_product')

    products = Product.objects.all()
    message = request.session.pop('message', '')
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
            data = json.loads(request.body)
            product = Product.objects.get(id=data["id"])
            setattr(product, data["field"], data["value"])
            product.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_product(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"status": "success"})
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Produkt nie istnieje"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    
@csrf_exempt
def delete_selected_products(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ids = data.get("ids", [])
            if not isinstance(ids, list):
                return JsonResponse({"status": "error", "message": "Invalid IDs format"})
            Product.objects.filter(id__in=ids).delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def delete_all_products(request):
    if request.method == "POST":
        try:
            Product.objects.all().delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

