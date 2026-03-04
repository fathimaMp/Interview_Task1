from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, Purchase, Supplier, PurchaseItem

# 1. Index/Home
def index(request):
    return render(request, 'index.html')

# 2. Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 3. Product Master (View & Add)
@login_required
def product_master(request):
    products = Product.objects.all()
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            price=request.POST['price'],
            tax_percentage=request.POST['tax']
        )
        return redirect('product_master')
    return render(request, 'products.html', {'products': products})

# 4. Product Edit
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.price = request.POST['price']
        product.tax_percentage = request.POST['tax']
        product.save()
        return redirect('product_master')
    return render(request, 'edit_product.html', {'product': product})
@login_required
def view_product(request, pk):
    # This fetches the specific product or shows a 404 error if not found
    product = get_object_or_404(Product, pk=pk)
    
    # Optional: If you want to show how many times this product was bought
    purchase_history = PurchaseItem.objects.filter(product=product).order_by('-purchase__date')

    return render(request, 'view_product.html', {
        'product': product,
        'purchase_history': purchase_history
    })

# 5. Purchase Form
@login_required
def purchase_form(request):
    products = Product.objects.all()
    if request.method == 'POST':
        Purchase.objects.create(
            supplier_name=request.POST['supplier'],
            date=request.POST['date'],
            invoice_number=request.POST['invoice'],
            product_id=request.POST['product'],
            quantity=request.POST['qty'],
            rate=request.POST['rate']
        )
        return redirect('index')
    return render(request, 'purchase.html', {'products': products})

@login_required
def create_purchase(request):
    suppliers = Supplier.objects.all() # Fetch all suppliers for the dropdown
    products = Product.objects.all()   # Fetch all products for the rows

    if request.method == "POST":
        # 1. Create the Invoice Header
        pur = Purchase.objects.create(
            supplier_id=request.POST.get('supplier'),
            date=request.POST.get('date'),
            invoice_number=request.POST.get('invoice')
        )

        # 2. Get lists of items from the dynamic HTML rows
        product_ids = request.POST.getlist('product_id[]')
        qtys = request.POST.getlist('qty[]')
        rates = request.POST.getlist('rate[]')

        total_invoice_amt = 0

        # 3. Save each product attached to this invoice
        for i in range(len(product_ids)):
            prod = Product.objects.get(id=product_ids[i])
            q = int(qtys[i])
            r = float(rates[i])
            
            sub = q * r
            tax = (sub * float(prod.tax_percentage)) / 100
            
            PurchaseItem.objects.create(
                purchase=pur,
                product=prod,
                quantity=q,
                rate=r,
                tax_amount=tax,
                sub_total=sub + tax
            )
            total_invoice_amt += (sub + tax)

        # 4. Update the final total on the header
        pur.grand_total = total_invoice_amt
        pur.save()
        return redirect('index')

    return render(request, 'purchase.html', {'suppliers': suppliers, 'products': products})

@login_required
def purchase_history(request):
    # Fetching PurchaseItem instead of Purchase to show individual product details
    items = PurchaseItem.objects.all().order_by('-purchase__date')
    return render(request, 'purchase_history.html', {'purchase_items': items})