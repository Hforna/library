from django.urls import path
from .views import *

urlpatterns = [
    path("/cart", cart, name="cart"),
    path("/cart/delete/<int:pk>", delete_item_cart, name="delete_item_cart"),
    path("/shipping", shipping, name="shipping"),
    path("/new_shipping", edit_shipping, name="new_shipping"),
    path("/payment", payment, name="payment"),
    path("/create-checkout-sessions", create_session, name="create_checkout"),
    path("/config", stripe_config)
]