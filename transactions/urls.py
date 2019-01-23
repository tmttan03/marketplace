from django.urls import path
from .views import CartListView, DeleteItemView, UpdateItemView, PaymentView
from . import views


urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart'),
    path('delete/item/<int:order_id>/', DeleteItemView.as_view(), name='delete-item'),
    path('update/item/<int:order_id>/', UpdateItemView.as_view(), name='update-item'),
    path('checkout/', PaymentView.as_view(), name='checkout'),
    path('check/', views.checkout, name='check'),
]

