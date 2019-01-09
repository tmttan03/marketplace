from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product 
from django.contrib.auth.models import User


class PostListView(ListView):
	model = Product
	template_name = 'posts/home.html'
	context_object_name = 'products'
	ordering = ['-created_at']

