from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin


from .models import Product, Category, Review
from .forms import AddReviewForm


class CategoryView(ListView):
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'products/detail_category.html'
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug')
        cat = Category.objects.get(slug=slug)
        context['title'] = cat
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.filter(cat=cat)
        return context


class ProductsView(ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Игры'
        context['categories'] = Category.objects.all()
        return context


class ProductDetail(DetailView, FormMixin):
    model = Product
    template_name = 'products/detail_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    form_class = AddReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('product_slug')
        context['title'] = Product.objects.get(slug=slug)
        product = Product.objects.get(slug=slug)
        context['reviews'] = Review.objects.filter(product=product)
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('products:game', kwargs={'product_slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = form.save(commit=False)

        if Review.objects.filter(product=self.get_object()).filter(user=self.request.user.profile).exists():
            raise ValidationError("Нельзя создавать больше одного отзыва к одной и той же игре")
        elif form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.product = self.get_object()
        self.object.user = self.request.user.profile
        self.object.save()
        return super().form_valid(form)


class DiscountProduct(ListView):
    model = Product
    template_name = 'products/discount.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.exclude(discount=0)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Товары по скидкам'
        return context


class SearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.filter(title__icontains=self.request.GET.get('search'))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        return context