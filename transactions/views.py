import datetime
import stripe
import math 

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import Http404
from django.views.generic import TemplateView , DetailView, ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User

from transactions.models import Transaction, Payment, Order
from transactions.forms import ToCartForm, UpdateItemForm

#stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key = "sk_test_LWtBD1TOvlfIMzdIawpJvHzj"


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


def checkout(request):
    #get all the exisiting orders of the user
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            amount = request.POST['totalAmount']
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Example Charge',
                source = token,
            )
            return redirect('cart')
        except stripe.CardError as e:
            message.info(request, "Your card has been declined.")

    context = {
        'order' : 100,
        'STRIPE_PUBLISHABLE_KEY' : publishKey
    }

    return render(request, 'transactions/checkout.html', context)


class PaymentView(LoginRequiredMixin, TemplateView):
    """Process payment"""
    template_name = 'transactions/checkout.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(PaymentView, self).get_context_data(**kwargs)
            user = self.request.user
            trans_no = Transaction.objects.filter(buyer=self.request.user, status='1')
            if trans_no.exists(): 
                no = Transaction.objects.get(buyer=user, status='1')
                context['orders'] = Order.objects.filter(transaction=no,status='1')
                context['counter'] = Order.objects.filter(transaction=no,status='1').count()
                return context
            else:
                raise Http404

    def post(self,*args,**kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        user = self.request.user
        trans_no = Transaction.objects.filter(buyer=self.request.user, status='1')
        if trans_no.exists(): 
            no = Transaction.objects.get(buyer=user, status='1')
            payment_no = "Payment" +  str(datetime.datetime.now())
            amount = round(float(self.request.POST['grndtotal1'])*100)
            token = self.request.POST['stripeToken']
            description = "Payment for " + no.no
            name = user.first_name + " "+ user.last_name
            payment = Payment(no=payment_no, transaction=no, amount_due=amount)
            payment.save()
            trans_no.update(status='0')
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description=description,
                source=token,
                #customer=name,
            )
            messages.success(self.request, f'Succesfully Purchased the items')
            return redirect('cart')
        else:
            messages.info(self.request, f"Add items to cart first")
            return redirect('post-home')


            
            
           

            
        
        




    