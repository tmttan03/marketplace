from django.urls import path
from .views import CartListView, DeleteItemView, UpdateItemView, PaymentView, MarketListView, ProductMarketView
from . import views


urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart'),
    path('market/', MarketListView.as_view(), name='market'),
    path('market/<int:product_id>/', ProductMarketView.as_view(), name='market-product'),
    path('delete/item/<int:order_id>/', DeleteItemView.as_view(), name='delete-item'),
    path('update/item/<int:order_id>/', UpdateItemView.as_view(), name='update-item'),
    path('checkout/', PaymentView.as_view(), name='checkout'),
    path('check/', views.checkout, name='check'),
]

