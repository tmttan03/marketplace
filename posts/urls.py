from django.urls import path
from .views import PostListView, UserProductsListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post-home'),
    path('selling/<str:username>', UserProductsListView.as_view(), name='user-products'),
]
