from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.forms import ProductForm
from main.models import Product

def show_main(request):
    product_list = Product.objects.all()
    context = {
        "product_list": product_list,
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {
        "product": product,
    }
    return render(request, "main/show_product.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
  try:
    data = Product.objects.filter(pk=product_id)
    return HttpResponse(serializers.seralize("xml", data), content_type="application/xml")
  except Product.DoesNotExist:
        return HttpResponse(status=404)
     
def show_json_by_id(request, product_id):
  try:
    data = Product.objects.filter(pk=product_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
  except Product.DoesNotExist:
        return HttpResponse(status=404)


