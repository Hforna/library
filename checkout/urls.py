from django.urls import path
from .views import *

urlpatterns = [
    path("/cart", cart, name="cart"),
    path("/cart/delete/<int:pk>", delete_item_cart, name="delete_item_cart"),
    path("/shipping", shipping, name="shipping"),
    path("/new_shipping", edit_shipping, name="new_shipping"),
    path("/create-checkout-sessions/<str:id>", create_session, name="create_checkout"),
    path("/config", stripe_config),
    path("/success", SuccessPayment.as_view()),
    path("/cancelled", CancelledPayment.as_view()),
    path("/webhook", stripe_webhook)
]