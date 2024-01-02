from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Category, Product
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ProductSerializer


def store(request):
    all_products=Product.objects.all()
    context={'my_products':all_products}
    return render(request, 'store/store.html', context)

def categories(request):
    all_categories=Category.objects.all()
    return {'all_categories':all_categories}




def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products=Product.objects.filter(category=category)
    return render(request,'store/list-category.html', {'category':category, 'products':products})




def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {"product": product}
    return render(request, 'store/product-info.html', context)

def handle_not_found(request, exception):
    return render(request, 'store/404.html')


class ProductAPIPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

class Product_view(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductAPIPagination