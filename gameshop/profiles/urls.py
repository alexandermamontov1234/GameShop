from django.urls import path
from .views import ProfileDetail, ShoppingCart, Favorite, CancelView, SuccessView, CreateCheckoutSessionView, \
    stripe_webhook, edit_profile_view

app_name = 'profiles'

urlpatterns = [
    path('shopping_cart/', ShoppingCart.as_view(), name='shopping-cart'),
    path('favorite/', Favorite.as_view(), name='favorite'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    # path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path(f'success/', SuccessView.as_view(), name='success'),
    # path('success/', SuccessView.as_view(), name='success'),
    # path('', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('edit', edit_profile_view, name='edit-profile'),
    path('<slug:profile_slug>', ProfileDetail.as_view(), name='myprofile')
]
