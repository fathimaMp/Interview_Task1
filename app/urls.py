from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('products/', views.product_master, name='product_master'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('purchase/', views.purchase_form, name='purchase_form'),
]