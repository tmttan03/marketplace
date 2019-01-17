import datetime

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import TemplateView , DetailView, ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User

from transactions.models import Transaction, Payment, Order
from transactions.forms import ToCartForm


class CartListView(ListView):
    model = Order
    template_name = 'transactions/cart.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        trans_no = Transaction.objects.get(buyer=self.request.user, status='1')
        return Order.objects.filter(transaction=trans_no,status='1')


class DeleteItemView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'transactions/includes/warning-cart-del-modal.html'

    def post(self,*args,**kwargs):
        form = Order.objects.filter(pk=self.kwargs['pk']).update(status='Inactive')
        messages.success(self.request, f'Item Deleted')
        return redirect('cart')
       
    #def test_func(self):
        #post = Product.objects.get(pk=self.kwargs['pk'])
        #if self.request.user == post.author:
            #return True
        #return False   