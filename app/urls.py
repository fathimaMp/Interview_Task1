from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Dashboard & Index
    path('', views.index, name='index'),

    # 2. Authentication (Registration, Login, Logout)
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 3. Product Master (View and Add)
    path('products/', views.product_master, name='product_master'),
    
    # 4. Product Edit (Using the Primary Key 'pk' to find the specific product)
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/view/<int:pk>/', views.view_product, name='view_product'),

    # 5. Purchase Form (The Multi-Product version)
    path('purchase/create/', views.create_purchase, name='purchase_form'),
    path('purchase/create/', views.purchase_form, name='purchase_form'),

    path('purchase/history/', views.purchase_history, name='purchase_history'),
]