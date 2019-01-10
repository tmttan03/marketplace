from django.urls import path
from .views import UserProductsListView , PostListView, PostView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post-home'),
    path('create/', PostView.as_view(), name='post-create'),
    path('selling/<str:username>', UserProductsListView.as_view(), name='user-products'),

]
