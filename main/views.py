from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.forms import ProductForm
from main.models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        "product_list": product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {
        "product": product,
    }
    return render(request, "show_product.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'user_id': product.user.id if product.user else None,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
  try:
    data = Product.objects.filter(pk=product_id)
    return HttpResponse(serializers.seralize("xml", data), content_type="application/xml")
  except Product.DoesNotExist:
        return HttpResponse(status=404)
     
def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'user_id': product.user.id if product.user else None,
            'user_username': product.user.username if product.user else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been successfully created!')
            # Add script to show toast
            messages.success(request, 'register_toast')  # Special message to trigger toast
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login_ajax.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    messages.success(request, 'logout_toast')  # Special message to trigger toast
    return response

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)  # don't save yet
        product_entry.user = request.user        # attach logged-in user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_product_ajax(request):
    try:
        # Get form data
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category = request.POST.get("category")
        thumbnail = request.POST.get("thumbnail")
        is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
        user = request.user

        # Validate required fields
        if not all([name, price, description, category]):
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields'
            }, status=400)

        # Create new product
        new_product = Product(
            name=name,
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()

        # Return success response
        return JsonResponse({
            'success': True,
            'message': 'Product created successfully',
            'product': {
                'id': str(new_product.id),
                'name': new_product.name,
                'price': new_product.price,
                'description': new_product.description,
                'category': new_product.category,
                'thumbnail': new_product.thumbnail,
                'is_featured': new_product.is_featured,
                'user_id': new_product.user.id if new_product.user else None,
            }
        }, status=201)

    except Exception as e:
        # Return error response
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_POST
def edit_product_ajax(request, id):
    try:
        # Get product
        product = get_object_or_404(Product, pk=id)
        
        # Check if user owns this product
        if product.user != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You do not have permission to edit this product'
            }, status=403)

        # Update product fields
        product.name = request.POST.get("name", product.name)
        product.price = request.POST.get("price", product.price)
        product.description = request.POST.get("description", product.description)
        product.category = request.POST.get("category", product.category)
        product.thumbnail = request.POST.get("thumbnail", product.thumbnail)
        product.is_featured = request.POST.get("is_featured") == 'on'
        
        product.save()

        # Return success response
        return JsonResponse({
            'success': True,
            'message': 'Product updated successfully',
            'product': {
                'id': str(product.id),
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'category': product.category,
                'thumbnail': product.thumbnail,
                'is_featured': product.is_featured,
                'user_id': product.user.id if product.user else None,
            }
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
