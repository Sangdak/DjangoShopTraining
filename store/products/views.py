from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView

from products.models import Basket, Product, ProductCategory
from users.models import User


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'
        context['is_promotion'] = False
        return context


def products(request, category_id=None, page_number=1):
    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        prods = Product.objects.filter(category=category)
    else:
        prods = Product.objects.all()
    items_per_page = 3
    paginator = Paginator(prods, items_per_page)
    prods_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': prods_paginator,
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
