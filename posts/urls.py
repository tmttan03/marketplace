from django.urls import path
from .views import (
	UserProductsListView,
	PostListView, 
	PostView, 
	DetailView, 
	UpdateView, 
	MessageView, 
	DeleteView,
	BoughtProductsListView,
	ProfileView,
	PublishDraftView,
	MarkAvailableView,
	MarkSoldView,
	RestockView,
	AddToFavorites,
	RemoveFromFavorites,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post-home'),
    path('create/', PostView.as_view(), name='post-create'),
    path('item/<int:product_id>/', DetailView.as_view(), name='view-post'),
    path('delete/<int:product_id>/', DeleteView.as_view(), name='delete-post'),
    path('publish/<int:product_id>/', PublishDraftView.as_view(), name='publish-draft'),
    path('available/<int:product_id>/', MarkAvailableView.as_view(), name='mark-available'),
    path('sold/<int:product_id>/', MarkSoldView.as_view(), name='mark-sold'),
    path('restock/<int:product_id>/', RestockView.as_view(), name='restock'),
    path('message/', MessageView.as_view(), name='message'),
    path('update/<int:product_id>/', UpdateView.as_view(), name='post-update'),
    path('selling/', UserProductsListView.as_view(), name='user-products'),
    path('buying/', BoughtProductsListView.as_view(), name='bought-products'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('favorite/<int:product_id>/', views.AddToFavorites, name='favorite'),
    path('unfavorite/<int:product_id>/', views.RemoveFromFavorites, name='unfavorite'),
]
