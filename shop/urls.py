from django.urls import path
from .views import home_view, signup_view, login_view, logout_view, buy_fruit, cart_detail, add_to_cart, \
    cart_detail, update_cart, remove_from_cart, checkout, process_checkout, order_success, cart_count

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('buy/<int:fruit_id>/', buy_fruit, name='buy_fruit'),
    path("cart/", cart_detail, name="cart_detail"),
    path("cart/add/<int:fruit_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:fruit_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:fruit_id>/", update_cart, name="update_cart"),
    path("checkout/", checkout, name="checkout"),
    path("checkout/process/", process_checkout, name="process_checkout"),
    path("order_success/", order_success, name="order_success"),
    path("cart/count/", cart_count, name="cart_count"),
]
