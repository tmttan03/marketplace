from django import forms
from .models import Product, Category
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	name = forms.CharField(max_length=100)
	description = forms.CharField(widget=forms.Textarea)
	price = forms.DecimalField(max_digits=10, decimal_places=2)
	category = forms.ModelChoiceField(Category.objects.all())

	class Meta:
		model = Product
		fields = ['name','price','category','description']


