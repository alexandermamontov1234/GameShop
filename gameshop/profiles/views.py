import stripe as stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView
from .models import Profile, User
from products.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY


class ShoppingCart(ListView):
    model = Product
    template_name = 'profiles/shopping_cart.html'
    # context_object_name = 'products'

    # def get_queryset(self):
    #     qs = Product.objects.filter(shopping_cart=self.request.user.profile)
    #     return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        products = Product.objects.filter(shopping_cart=self.request.user.profile)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['products'] = products
        total_price = 0
        for product in products:
            total_price += product.get_final_price
        context['total_price'] = total_price
#       context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY

        return context


class SuccessView(TemplateView):
    template_name = "profiles/success.html"


class CancelView(TemplateView):
    template_name = "profiles/cancel.html"


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        products = Product.objects.filter(shopping_cart=self.request.user.profile)
        YOUR_DOMAIN = "http://127.0.0.1:8000/profiles/"
        line_items = []
        metadata = {}
        for product in products:
            metadata[product.title] = 'product.url'
            line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.get_final_price),
                        'product_data': {
                            'name': product.title,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                })
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            metadata=metadata,
            mode='payment',
            success_url=YOUR_DOMAIN + 'success/',
            cancel_url=YOUR_DOMAIN + 'cancel/',
        )

        return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )
        customer_email = session["customer_details"]["email"]
        message = ""
        for key, value in session["metadata"].items():
            message += f"\nНазвание товара: {key}, ссылка для скачивания: {value}"
        print(session["metadata"])
        send_mail(
            subject="Вот Ваш продукт",
            message=f"Спасибо за покупку! Вот ваши товары:{message}",
            recipient_list=[customer_email],
            from_email="qwerty@mail.ru"
        )

    return HttpResponse(status=200)


class Favorite(ListView):
    model = Product
    template_name = 'profiles/favorite.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.filter(favorite=self.request.user.profile)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Избранное'
        return context


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profiles/myprofile.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'profile_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
        return context



