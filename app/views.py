from django.shortcuts import render,redirect
from .models import Category, Product
from django.http import JsonResponse
from app.forms import ProductModelForm,FormModelComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from app.utils import filter_by_price
from django.db.models import Avg


# Create your views here.

def index(request,category_id = None):
    search_query = request.GET.get('q','')
    filter_type = request.GET.get('filter_type','')
    
    
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()
        
    if search_query:
        products = products.filter(Q(name__icontains = search_query) | Q(description__icontains=search_query))
    
    products = filter_by_price(filter_type,products)

    context = {
        'categories':categories,
        'products':products
    }
    return render(request,'app/home.html',context)


def detail(request,product_id):
    product = Product.objects.get(id = product_id)
    comments = product.comments.filter(is_handle=False)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).order_by('-created_at')[:4]
    context={
        'product' : product,
        'comments' : comments,
        'related_products' : related_products
    }
    return render(request,'app/detail.html',context)


@login_required(login_url='/admin/')
def create_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Product successfully created ✅"
            )
            # add messages
            
            return redirect('app:create')
    else:
        form = ProductModelForm()
        
                
    context = {
        'form':form
    }
    return render(request,'app/create.html',context)

def delete_product(request,pk):
    product = Product.objects.get( id=pk )
    if product:
        product.delete()
        return redirect('app:index')
    
    return render(request,'app/detail.html')


def update_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            form.save()
            return redirect('app:detail',pk)
    else:
        form = ProductModelForm(instance=product)
        
    context = {
        'form':form,
        'product':product
    }
    return render(request,'app/update.html',context)



def create_comment(request,product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = FormModelComment(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()

            return redirect('app:detail.html', product_id=product.id)

    else:
        form = FormModelComment()

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'app/detail.html', context)


def rating(request):
    products = Product.objects.annotate(
        avg_rating=Avg('comments__rating')
    ).order_by('-avg_rating')

    context = {
        'products' : products
    }

    return render(request, 'app/home.html', context)