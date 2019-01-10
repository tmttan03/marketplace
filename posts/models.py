from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 


class Category(models.Model):
	title = models.CharField(max_length=100)

	def __str__(self):
		return self.title

class Product(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

