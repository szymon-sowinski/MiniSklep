"""
URL configuration for MiniSklep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MiniSklepApp.views import add_product, display_products, login_view, logout_view, update_product, delete_product, delete_selected_products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', add_product, name='home'),
    path('add_product/', add_product, name='add_product'),
    path('display_products/', display_products, name='display_products'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("update-product/", update_product, name="update_product"),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('delete-selected/', delete_selected_products, name='delete_selected_products'),
]
