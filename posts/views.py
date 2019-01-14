from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import TemplateView , DetailView, ListView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import PostForm, UpdatePostForm
from .models import Product , Category


class PostListView(TemplateView):
    template_name = 'posts/home.html'

    def get_context_data(self, **kwargs):
         context = super(PostListView, self).get_context_data(**kwargs)
         context['products'] = Product.objects.filter(status="1")
         context['categories'] = Category.objects.all()
         return context
  
class UserProductsListView(ListView):
	model = Product
	template_name = 'posts/user_products.html'
	context_object_name = 'products'

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Product.objects.filter(author=user,status="1").order_by('-created_at')

class PostView(TemplateView):
    template_name = 'posts/includes/create-post-modal.html'
    form = PostForm

    def get_context_data(self, **kwargs):
         context = super(PostView, self).get_context_data(**kwargs)
         context['form'] = self.form()
         return context

    def post(self,*args,**kwargs):
    	form = self.form(self.request.POST)
    	if form.is_valid():
            product = form.save(commit=False)
            product.author = self.request.user
            product.save()
            messages.success(self.request, f'Successfully Added a New Item')
            return redirect('message') 
    	return render(self.request, self.template_name,{'form': form})


class UpdateView(DetailView):
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

class DeleteView(DetailView):
    model = Product
    template_name = 'posts/includes/warning-del-modal.html'

    def post(self,*args,**kwargs):
        form = Product.objects.filter(pk=self.kwargs['pk']).update(status='Inactive')
        messages.success(self.request, f'Item Deleted')
        return redirect('user-products', self.request.user.username)
        #return render(self.request, self.template_name, {'form': form}) 

