import pytest
from django.urls import reverse
from products.models import Product, Category


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    'products:catalog',
    'products:discount'
])
def test_product_views(client, url, create_product):
    category, product = create_product
    assert Category.objects.count() == 1
    assert Product.objects.count() == 1
    temp_url = reverse(url)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_product_search(auto_login_user, create_product):
    client, user = auto_login_user()
    category, product = create_product
    url = reverse('products:search')
    assert Category.objects.count() == 1
    assert Product.objects.count() == 1
    resp = client.get(url, data={'search': 'qw'})
    assert resp.status_code == 200


@pytest.mark.django_db
def test_product_detail(auto_login_user, create_product):
    client, user = auto_login_user()
    category, product = create_product
    assert Category.objects.count() == 1
    assert Product.objects.count() == 1
    url = reverse('products:game',  kwargs={'product_slug': product.slug})
    resp = client.get(url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_category_detail(auto_login_user, create_product):
    client, user = auto_login_user()
    category, product = create_product
    assert Category.objects.count() == 1
    assert Product.objects.count() == 1
    url = reverse('products:category',  kwargs={'category_slug': category.slug})
    resp = client.get(url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_product_favorite(auto_login_user, create_product):
    client, user = auto_login_user()
    category, product = create_product
    url = reverse('products:add-remove-favorite',  kwargs={'product_slug': product.slug})
    assert Category.objects.count() == 1
    assert Product.objects.count() == 1
    assert Product.objects.filter(favorite=user.profile).first() is None
    resp = client.get(url, HTTP_REFERER='/products/product/asd', follow=True)
    assert Product.objects.filter(favorite=user.profile).first() == product
    assert resp.status_code == 200


@pytest.mark.django_db
def test_product_cart(auto_login_user, create_product):
    client, user = auto_login_user()
    category, product = create_product
    url = reverse('products:add-remove-cart',  kwargs={'product_slug': product.slug})
    assert Category.objects.count() == 1
    assert Product.objects.count() == 1
    assert Product.objects.filter(shopping_cart=user.profile).first() is None
    resp = client.get(url, HTTP_REFERER='/products/product/asd', follow=True)
    assert Product.objects.filter(shopping_cart=user.profile).first() == product
    assert resp.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    'shopping-cart',
    'favorite'
])
def test_profile_cart(auto_login_user, create_product, url):
    client, user = auto_login_user()
    category, product = create_product
    temp_url = reverse(f'profiles:{url}')
    assert Category.objects.count() == 1
    assert Product.objects.count() == 1
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_profile_detail(auto_login_user):
    client, user = auto_login_user()
    url = reverse('profiles:myprofile', kwargs={'profile_slug': user.profile.slug})
    response = client.get(reverse('profiles:myprofile', kwargs={'profile_slug': user.profile.slug}))

    assert response.status_code == 200
