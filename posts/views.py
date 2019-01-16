from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import TemplateView , DetailView, ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import PostForm, UpdatePostForm, ImageFieldForm
from .models import Product , Category, ProductAlbum


class PostListView(TemplateView):
    template_name = 'posts/home.html'

    def get_context_data(self, **kwargs):
         context = super(PostListView, self).get_context_data(**kwargs)
         context['products'] = Product.objects.filter(status="1")
         context['categories'] = Category.objects.all()
         context['productalbum'] = ProductAlbum.objects.all()
         return context
  
class UserProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'posts/user_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Product.objects.filter(author=user,status="1").order_by('-created_at')


class PostView(LoginRequiredMixin, TemplateView):
    template_name = 'posts/includes/create-post-modal.html'
    form = PostForm
    i_form = ImageFieldForm

    def get_context_data(self, **kwargs):
         context = super(PostView, self).get_context_data(**kwargs)
         context['form'] = self.form()
         #context['i_form'] = self.i_form()
         return context

    def post(self,*args,**kwargs):
    	form = self.form(self.request.POST)
    	if form.is_valid(): 
            product = form.save(commit=False)
            product.author = self.request.user
            product.save()
            #i_form.save()
            messages.success(self.request, f'Successfully Added a New Item')
            return redirect('message')        
    	return render(self.request, self.template_name,{'form': form})


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product
    template_name = 'posts/includes/update-post-modal.html'
    form = UpdatePostForm

    def get_context_data(self, **kwargs):
         context = super(UpdateView, self).get_context_data(**kwargs)
         context['form'] = UpdatePostForm(instance=Product.objects.get(pk=self.kwargs['pk']))
         return context

    def post(self,*args,**kwargs):
        form = UpdatePostForm(self.request.POST, instance=Product.objects.get(pk=self.kwargs['pk']))
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Item Updated')
            return redirect('message')
        return render(self.request, self.template_name, {'form': form}) 

    def test_func(self):
        post = Product.objects.get(pk=self.kwargs['pk'])
        if self.request.user == post.author:
            return True
        return False    


class DetailView(DetailView):
    model = Product
    template_name = 'posts/includes/create-post-modal-body.html'


class MessageView(TemplateView):
    template_name = 'posts/messages.html'

    def get_context_data(self, **kwargs):
         context = super(MessageView, self).get_context_data(**kwargs)
         context['products'] = Product.objects.filter(status="1")
         context['categories'] = Category.objects.all()
         return context

class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product
    template_name = 'posts/includes/warning-del-modal.html'

    def post(self,*args,**kwargs):
        form = Product.objects.filter(pk=self.kwargs['pk']).update(status='Inactive')
        messages.success(self.request, f'Item Deleted')
        return redirect('user-products', self.request.user.id)
       
    def test_func(self):
        post = Product.objects.get(pk=self.kwargs['pk'])
        if self.request.user == post.author:
            return True
        return False   