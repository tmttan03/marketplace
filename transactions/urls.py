from django.urls import path
from .views import CartListView, DeleteItemView
from . import views

urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart'),
    path('delete/item/<int:order_id>/', DeleteItemView.as_view(), name='delete-item'),
    #path('update/item/<int:pk>/', views.UpdateItemView, name='update-item'),
]

