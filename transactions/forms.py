from django import forms
from .models import Transaction, Order
from django.contrib.auth.models import User

class ToCartForm(forms.ModelForm):
	#no = forms.CharField(max_length=500,label='')
	comment = forms.CharField(max_length=500,label='', widget=forms.Textarea(attrs={'placeholder':'Comment','rows':'3'}))

	class Meta:
		model = Order
		fields = ['qty','comment']

class UpdateItemForm(forms.ModelForm):
	qty = forms.CharField(label='', widget=forms.TextInput(attrs={'id':'target'}))
	comment = forms.CharField(max_length=500,label='', widget=forms.Textarea(attrs={'placeholder':'Comment','rows':'3', 'id':'target'}))

	class Meta:
		model = Order
		fields = ['qty','comment']