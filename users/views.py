from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from transactions.models import Transaction, Payment, Order


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to login.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html',{'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		if request.user.is_authenticated:
			trans_no = Transaction.objects.filter(buyer=request.user, status='1')
			if trans_no.exists(): 
				no = Transaction.objects.get(buyer=request.user, status='1')
				counter = Order.objects.filter(transaction=no,status='1').count()
			counter = 0
       
	context = {
		'u_form' : u_form,
		'p_form' : p_form,
		'counter' : counter,
	}
	return render(request, 'users/profile.html', context)



