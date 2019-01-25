from django import forms
from .models import Transaction, Order
from django.contrib.auth.models import User

class ToCartForm(forms.ModelForm):
	#no = forms.CharField(max_length=500,label='')
	qty = forms.IntegerField(widget=forms.TextInput(attrs={'min':'1','type':'number','value':1}))
	comment = forms.CharField(max_length=500,label='', widget=forms.Textarea(attrs={'placeholder':'Comment','rows':'3'}))

	class Meta:
		model = Order
		fields = ['qty','comment']

class UpdateItemForm(forms.ModelForm):
	#qty = forms.IntegerField(label='')
	qty = forms.IntegerField(widget=forms.TextInput(attrs={'min':'1','type':'number'}))
	comment = forms.CharField(max_length=500,label='', widget=forms.Textarea(attrs={'placeholder':'Comment','rows':'3'}))

	class Meta:
		model = Order
		fields = ['qty','comment']