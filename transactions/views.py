import datetime

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import Http404
from django.views.generic import TemplateView , DetailView, ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User

from transactions.models import Transaction, Payment, Order
from transactions.forms import ToCartForm



class CartListView(LoginRequiredMixin, TemplateView):
    """Displays the unpaid orders of the user"""
    template_name = 'transactions/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartListView, self).get_context_data(**kwargs)
        user = self.request.user
        trans_no = Transaction.objects.get(buyer=user, status='1')
        context['orders'] = Order.objects.filter(transaction=trans_no,status='1')
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




       

     