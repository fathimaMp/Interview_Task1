from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Purchase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
# Index Page
def index(request):
    return render(request, 'index.html')

# Product Master: View & Add
@login_required
def product_list(request):
    products = Product.objects.all()
    if request.method == "POST":
        Product.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            price=request.POST['price'],
            tax_percentage=request.POST['tax']
        )
        return redirect('product_list')
    return render(request, 'products.html', {'products': products})

# Product Edit
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.price = request.POST['price']
        product.tax_percentage = request.POST['tax']
        product.save()
        return redirect('product_list')
    return render(request, 'edit_product.html', {'product': product})

# Purchase Form
@login_required
def purchase_form(request):
    products = Product.objects.all()
    if request.method == "POST":
        Purchase.objects.create(
            supplier_name=request.POST['supplier'],
            date=request.POST['date'],
            invoice_number=request.POST['invoice'],
            product_id=request.POST['product'],
            quantity=int(request.POST['qty']),
            rate=float(request.POST['rate'])
        )
        return redirect('index')
    return render(request, 'purchase.html', {'products': products})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
