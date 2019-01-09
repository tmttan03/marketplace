from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import TemplateView , DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product , Category
from django.contrib.auth.models import User


class PostListView(TemplateView):
    template_name = 'posts/home.html'

    def get_context_data(self, **kwargs):
         context = super(PostListView, self).get_context_data(**kwargs)
         context['products'] = Product.objects.all()
         context['categories'] = Category.objects.all()
         return context

class UserProductsListView(ListView):
	model = Product
	template_name = 'posts/user_products.html'
	context_object_name = 'products'

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Product.objects.filter(author=user).order_by('-created_at')