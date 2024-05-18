from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render

from products.models import Basket, Product, ProductCategory
from users.models import User


def index(request):
    context = {
        'title': 'Store',
        'is_promotion': False,
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    context = {
        'title': 'Store - Каталог',
        'products': products,
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


@login_required()
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required()
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
