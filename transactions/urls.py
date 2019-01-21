from django.urls import path
from .views import CartListView, DeleteItemView, UpdateItemView

urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart'),
    path('delete/item/<int:order_id>/', DeleteItemView.as_view(), name='delete-item'),
    path('update/item/<int:order_id>/', UpdateItemView.as_view(), name='update-item'),
]

