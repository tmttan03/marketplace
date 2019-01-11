from django.urls import path
from .views import UserProductsListView , PostListView, PostView, DetailView, UpdateView, MessageView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post-home'),
    path('create/', PostView.as_view(), name='post-create'),
    path('item/<int:pk>/', DetailView.as_view(), name='view-post'),
    path('message/', MessageView.as_view(), name='message'),
    path('update/<int:pk>/', UpdateView.as_view(), name='post-update'),
    path('selling/<str:username>', UserProductsListView.as_view(), name='user-products'),

]
