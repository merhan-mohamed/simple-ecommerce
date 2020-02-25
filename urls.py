from django.urls import path

from Cart.views import OrderSummaryView, CheckoutView, PaymentView, AddCouponView, RequestRefundView
from . import views
app_name = 'Cart'
urlpatterns = [

    path('add_to_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('remove_single_item_from_cart/<slug:slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<str:payment_option>/', PaymentView.as_view(), name='payment'),
    path('add_coupon/',AddCouponView.as_view(), name='add_coupon'),
    path('RequestRefund/',RequestRefundView.as_view(), name='RequestRefund')
 ]