from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def _common_tests(self, response, title: str, template_name: str):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], title)
        self.assertTemplateUsed(response, template_name)

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        items_per_page = response.context_data['paginator'].per_page

        self._common_tests(response, 'Store - Каталог', 'products/products.html')
        self.assertQuerysetEqual(
            response.context_data.get('object_list'),
            self.products[:items_per_page],
            # ordered=True
        )

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response, 'Store - Каталог', 'products/products.html')
        self.assertQuerysetEqual(
            response.context_data.get('object_list'),
            self.products.filter(category__id=category.id),
            # ordered=True
        )
