import datetime

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import Http404
from django.views.generic import TemplateView , DetailView, ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import PostForm, UpdatePostForm, ImageFieldForm, StockForm
from .models import Product , Category, ProductAlbum, Stock, Favorite

from transactions.models import Transaction, Payment, Order
from transactions.forms import ToCartForm


class PostListView(TemplateView):
    """Displays the list of products in the market."""
    template_name = 'posts/home.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(status='1', is_draft=False).order_by('created_at')
        context['categories'] = Category.objects.all()
        context['productalbum'] = ProductAlbum.objects.all()
        if self.request.user.is_authenticated:
            trans_no = Transaction.objects.filter(buyer=self.request.user, status='1')
            if trans_no.exists(): 
                no = Transaction.objects.get(buyer=self.request.user, status='1')
                context['counter'] = Order.objects.filter(transaction=no,status='1').count()
            else:
                context['counter'] = 0
        return context


class UserProductsListView(LoginRequiredMixin, TemplateView):
    """Displays the list of products the user is selling."""
    template_name = 'posts/user_products.html'

    def get_context_data(self, **kwargs):
        context = super(UserProductsListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['products'] = Product.objects.filter(seller=user, status='1').order_by('created_at')
        context['sold_products'] = Product.objects.filter(seller=user, status='2').order_by('created_at')
        context['stocks']  = Stock.objects.filter(status='1')
        #import pdb; pdb.set_trace()

        #if self.request.user.is_authenticated:
        trans_no = Transaction.objects.filter(buyer=user, status='1')
        if trans_no.exists(): 
            no = Transaction.objects.get(buyer=user, status='1')
            context['counter'] = Order.objects.filter(transaction=no, status='1').count()
            return context
        else:
            context['counter'] = 0
            return context
           

class BoughtProductsListView(LoginRequiredMixin, TemplateView):
    """Displays the list of products the user purchased."""
    template_name = 'posts/buying.html'

    def get_context_data(self, **kwargs):
        context = super(BoughtProductsListView, self).get_context_data(**kwargs)
        user = self.request.user
        #Trans = Transaction.objects.filter(buyer=user, status='0') 
        transactions = Transaction.objects.filter(buyer=user, status='0')
        orders = Order.objects.all()
        context['transactions'] = Transaction.objects.filter(buyer=user, status='0')
        context['orders'] = Order.objects.filter(status='1').all()
        
        counter = 0
        context['current_count'] =  {}
        for transaction in transactions:
            for order in orders:
                if transaction == order.transaction:
                    counter = counter + 1
                    context['current_count'] = counter
        
        #if self.request.user.is_authenticated:
        trans_no = Transaction.objects.filter(buyer=user, status='1')
            #if self.kwargs.get('user_id') == self.request.user.id:
        if trans_no.exists(): 
            no = Transaction.objects.get(buyer=self.request.user, status='1')
            context['counter'] = Order.objects.filter(transaction=no,status='1').count()
            return context
        else:
            context['counter'] = 0
            return context
            #raise Http404
 

class PostView(LoginRequiredMixin, TemplateView):
    """Create a Product"""
    template_name = 'posts/includes/create-post-modal.html'
    form = PostForm
    i_form = ImageFieldForm
    s_form = StockForm

    def get_context_data(self, **kwargs):
        if self.request.is_ajax():
             context = super(PostView, self).get_context_data(**kwargs)
             context['form'] = self.form()
             #context['i_form'] = self.i_form()
             context['s_form'] = self.s_form()
             return context
        raise Http404

    def post(self,*args,**kwargs):
        form = self.form(self.request.POST)
        s_form = self.s_form(self.request.POST)
        #i_form = self.i_form(self.request.POST,self.request.FILES)
        if form.is_valid() and s_form.is_valid():
            product = form.save(commit=False)
            product.seller = self.request.user
            product.save()

            stock = s_form.save(commit=False)
            #import pdb; pdb.set_trace()
            stock.stock_no = "Stock#" +  str(datetime.datetime.now())
            stock.product = product
            stock.stock_on_hand = s_form.cleaned_data.get('stock_total')
            stock.save()

            #import pdb; pdb.set_trace()
            messages.success(self.request, f'Successfully Added a New Item')
            return redirect('message')        
        return render(self.request, self.template_name,{'form': form, 's_form': s_form})


class MessageView(TemplateView):
    """Message Content for Modal Info"""
    template_name = 'posts/messages.html'

    def get_context_data(self, **kwargs):
         context = super(MessageView, self).get_context_data(**kwargs)
         context['products'] = Product.objects.filter(status='1')
         context['categories'] = Category.objects.all()
         return context


class DeleteView(LoginRequiredMixin, TemplateView):
    """Delete a Product."""
    model = Product
    template_name = 'posts/includes/warning-del-modal.html'

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            product = get_object_or_404(Product, id=self.kwargs.get('product_id'), seller=self.request.user)
            return render(self.request, self.template_name, {'product': product})
        raise Http404

    def post(self,*args,**kwargs):
        product = Product.objects.filter(id=self.kwargs.get('product_id'), seller=self.request.user)
        if product.exists():
            product.update(status='0')
            messages.success(self.request, f'Item Deleted')
        else:
            messages.error(self.request, f'Product Does not Exist')
        return redirect('user-products')


class UpdateView(LoginRequiredMixin, TemplateView):
    """Update Product Details."""
    template_name = 'posts/includes/update-post-modal.html'
    form = UpdatePostForm

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            context = super(UpdateView, self).get_context_data(**kwargs)
            context['form'] = UpdatePostForm(instance=Product.objects.get(pk=self.kwargs.get('product_id')))
            return render(self.request, self.template_name, context)
        raise Http404

    def post(self,*args,**kwargs):
        form = UpdatePostForm(self.request.POST, instance=Product.objects.get(pk=self.kwargs.get('product_id')))
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Item Updated')
            return redirect('message')
        return render(self.request, self.template_name, {'form': form}) 


class DetailView(TemplateView):
    """Show Details of a Product"""
    template_name = 'posts/includes/create-post-modal-body.html'
    form = ToCartForm

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            context = super(DetailView, self).get_context_data(**kwargs)
            context['product'] = Product.objects.get(pk=self.kwargs.get('product_id'))
            context['form'] = ToCartForm()
            try:
                stock = Stock.objects.get(status='1',product=self.kwargs.get('product_id'))
                context['stock'] = stock
            except Stock.DoesNotExist:
                context['stock'] = {'stock_on_hand': 0}

            if self.request.user.is_authenticated:
                try:
                    favorites = Favorite.objects.get(product=self.kwargs.get('product_id'), user=self.request.user)
                    context['is_favorite'] = favorites
                except Favorite.DoesNotExist:
                    context['is_favorite'] = {'is_favorite': False}

            #import pdb; pdb.set_trace()
            return render(self.request, self.template_name, context)
        raise Http404

    def post(self,*args,**kwargs):
        form = self.form(self.request.POST)
        if form.is_valid(): 
            item = form.save(commit=False)
            item.product = Product.objects.get(pk=self.kwargs['product_id'])
            item.reference_no = "Ref" + str(datetime.datetime.now())
            try:
                trans_no = Transaction.objects.get(buyer=self.request.user, status='1')
                item.transaction = trans_no
            except Transaction.DoesNotExist:
                no = "Trans" +  str(datetime.datetime.now())
                trans = Transaction(no=no, buyer=self.request.user)
                trans.save()
                item.transaction = trans
            item.save()
            messages.success(self.request, f'Item Added to Cart')
            return redirect('post-home')        
        return render(self.request, self.template_name, {'form': form})


class ProfileView(TemplateView):
    """Displays the list of products in the market."""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['user_name'] = user
        product = Product.objects.filter(status='1', is_draft=False, seller=user).order_by('created_at')
        on_sale = product.count()
        context['on_sale'] = on_sale
        context['products'] = product
        context['categories'] = Category.objects.all()
        context['productalbum'] = ProductAlbum.objects.all()
        context['favorites'] = Favorite.objects.filter(user=user,is_favorite=True)
        if self.request.user.is_authenticated:
            trans_no = Transaction.objects.filter(buyer=self.request.user, status='1')
            if trans_no.exists(): 
                no = Transaction.objects.get(buyer=self.request.user, status='1')
                context['counter'] = Order.objects.filter(transaction=no,status='1').count()
            else:
                context['counter'] = 0
        return context


def AddToFavorites(request, product_id):
    """Add to Favorites a Product"""
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        favorite = Favorite.objects.filter(product=product, user=request.user)
        if favorite.exists():
            favorite.update(is_favorite=True)
        else:
            no = "Fav" +  str(datetime.datetime.now())
            favorite = Favorite(product=product, user=request.user, favorite_no=no)
            favorite.save()
        messages.success(request, f'Added to My Favorites')

        return redirect('/')
    return redirect('login')


def RemoveFromFavorites(request, product_id):
    """Remove from Favorites a Product"""
    if request.user.is_authenticated:
        favorite = Favorite.objects.filter(product=product_id, user=request.user)
        favorite.update(is_favorite=False)
        messages.success(request, f'Removed from My Favorites')
        return redirect('/')
    return redirect('login')

    
class PublishDraftView(LoginRequiredMixin, TemplateView):
    """Publish a Draft."""
    model = Product
    template_name = 'posts/selling-page/warning-publish.html'

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            product = get_object_or_404(Product, id=self.kwargs.get('product_id'), seller=self.request.user)
            return render(self.request, self.template_name, {'product': product})
        raise Http404

    def post(self,*args,**kwargs):
        product = Product.objects.filter(id=self.kwargs.get('product_id'), seller=self.request.user)
        if product.exists():
            product.update(is_draft=False)
            messages.success(self.request, f'Published Post')
        else:
            messages.error(self.request, f'Product Does not Exist')
        return redirect('user-products')


class MarkAvailableView(LoginRequiredMixin, TemplateView):
    """Publish a Draft."""
    model = Product
    template_name = 'posts/selling-page/warning-available.html'

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            product = get_object_or_404(Product, id=self.kwargs.get('product_id'), seller=self.request.user)
            return render(self.request, self.template_name, {'product': product})
        raise Http404

    def post(self,*args,**kwargs):
        product = Product.objects.filter(id=self.kwargs.get('product_id'), seller=self.request.user)
        if product.exists():
            product.update(status='1')
            messages.success(self.request, f'Renewed Post')
        else:
            messages.error(self.request, f'Product Does not Exist')
        return redirect('user-products')


class MarkSoldView(LoginRequiredMixin, TemplateView):
    """Publish a Draft."""
    model = Product
    template_name = 'posts/selling-page/warning-sold.html'

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            product = get_object_or_404(Product, id=self.kwargs.get('product_id'), seller=self.request.user)
            return render(self.request, self.template_name, {'product': product})
        raise Http404

    def post(self,*args,**kwargs):
        product = Product.objects.filter(id=self.kwargs.get('product_id'), seller=self.request.user)
        if product.exists():
            product.update(status='2')
            #messages.success(self.request, f'')
        else:
            messages.error(self.request, f'Product Does not Exist')
        return redirect('user-products')


class RestockView(LoginRequiredMixin, TemplateView):
    """Restock Item."""
    s_form = StockForm
    template_name = 'posts/selling-page/restock-modal.html'

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            product = get_object_or_404(Product, id=self.kwargs.get('product_id'), seller=self.request.user)
            s_form = self.s_form()
            return render(self.request, self.template_name, {'product': product, 's_form' : s_form})
        raise Http404

    def post(self,*args,**kwargs):
        s_form = self.s_form(self.request.POST)
        product = Product.objects.get(id=self.kwargs.get('product_id'))
        stocks = Stock.objects.filter(product_id=self.kwargs.get('product_id'),status='1',stock_on_hand=0)
        if stocks.exists():
            if s_form.is_valid():
                stocks.update(status='2')
                stock = s_form.save(commit=False)
                stock.stock_no = "Stock#" +  str(datetime.datetime.now())
                stock.product = product
                stock.stock_on_hand = s_form.cleaned_data.get('stock_total')
                stock.save()
                messages.success(self.request, f'Successfully restocked item')
                return redirect('user-products')        
            return render(self.request, self.template_name,{'s_form': s_form})
        raise Http404



    