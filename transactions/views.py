import datetime

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import Http404
from django.views.generic import TemplateView , DetailView, ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User

from transactions.models import Transaction, Payment, Order
from transactions.forms import ToCartForm, UpdateItemForm


class CartListView(LoginRequiredMixin, TemplateView):
    """Displays the unpaid orders of the user"""
    template_name = 'transactions/cart.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(CartListView, self).get_context_data(**kwargs)
            user = self.request.user
            trans_no = Transaction.objects.filter(buyer=self.request.user, status='1')
            if trans_no.exists(): 
                no = Transaction.objects.get(buyer=user, status='1')
                context['orders'] = Order.objects.filter(transaction=no,status='1')
                context['counter'] = Order.objects.filter(transaction=no,status='1').count()
            else:
                context['counter'] = 0
            return context
        

class DeleteItemView(LoginRequiredMixin, TemplateView):
    """Delete an Order."""
    template_name = 'transactions/includes/warning-cart-del-modal.html'

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
            return render(self.request, self.template_name, {'order': order})
        raise Http404

    def post(self,*args,**kwargs):
        order = Order.objects.filter(id=self.kwargs.get('order_id'))
        if order.exists():
            order.update(status='0')
            messages.success(self.request, f'Item Deleted')
        else:
            messages.error(self.request, f'Product Does not Exist')
        return redirect('cart')


class UpdateItemView(LoginRequiredMixin, TemplateView):
    """Update Product Details."""
    template_name = 'transactions/includes/update-cart-modal.html'
    form = UpdateItemForm

    def get(self,*args,**kwargs):
        if self.request.is_ajax():
            context = super(UpdateItemView, self).get_context_data(**kwargs)
            context['form'] = UpdateItemForm(instance=Order.objects.get(pk=self.kwargs.get('order_id')))
            return render(self.request, self.template_name, context)
        raise Http404

    def post(self,*args,**kwargs):
        form = UpdateItemForm(self.request.POST, instance=Order.objects.get(pk=self.kwargs.get('order_id')))
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Cart Updated')
            return redirect('message')
        return render(self.request, self.template_name, {'form': form}) 


