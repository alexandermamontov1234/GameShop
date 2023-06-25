from django.urls import path
from .views import ProductsView, ProductDetail, CategoryView, CategoryDetail, DiscountProduct, SearchView, \
    add_remove_cart, add_remove_favorite

app_name = 'products'

urlpatterns = [
    path('', CategoryView.as_view(), name='categories'),
    path('catalog', ProductsView.as_view(), name='catalog'),
    path('category/<slug:category_slug>', CategoryDetail.as_view(), name='category'),
    path('discount/', DiscountProduct.as_view(), name='discount'),
    path('search/', SearchView.as_view(), name='search'),
    path('product/<slug:product_slug>', ProductDetail.as_view(), name='game'),
    path('product/add-favorite/<slug:product_slug>', add_remove_favorite, name='add-remove-favorite'),
    path('product/add-cart/<slug:product_slug>', add_remove_cart, name='add-remove-cart')
]
