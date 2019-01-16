from django import forms
from .models import Product, Category, ProductAlbum
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'What are you selling?'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Describe your item', 'rows':'3'}), label='')
	price = forms.DecimalField(max_digits=10, decimal_places=2, label='', widget=forms.TextInput(attrs={'placeholder':'Price'}))
	category = forms.ModelChoiceField(Category.objects.all(), label='')
	#location= forms.CharField(label='',widget=forms.TextInput(attrs={'id':'autocomplete','onFocus':'geolocate()','autocomplete':'off'}))

	class Meta:
		model = Product
		fields = ['name','price','category','description']

class UpdatePostForm(forms.ModelForm):
	name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder':'What are you selling?'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Describe your item', 'rows':'3'}), label='')
	price = forms.DecimalField(max_digits=10, decimal_places=2, label='', widget=forms.TextInput(attrs={'placeholder':'Price'}))
	category = forms.ModelChoiceField(Category.objects.all(), label='')


	class Meta:
		model = Product
		fields = ['name','price','category','description'] 


class ImageFieldForm(forms.Form):
    img_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='')

    class Meta:
    	model = ProductAlbum
    	fields = ['img_field'] 

