from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
from PIL import Image

class Category(models.Model):
	title = models.CharField(max_length=100)

	def __str__(self):
		return self.title


class Product(models.Model):
	DELETED = '0'
	AVAILABLE = '1'
	SOLD = '2'

	STATUS_CHOICES = (
		(DELETED, "Deleted"),
		(AVAILABLE, "Available"),
		(SOLD, "Sold"),
	)

	name = models.CharField(max_length=100)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	location = models.CharField(max_length=250, default="Davao")
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	is_draft = models.BooleanField(default=False)
	#stock_on_hand = models.PositiveIntegerField(default=1)
	status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=AVAILABLE,
    )
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class ProductAlbum(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='product_images/')
	uploaded_at = models.DateTimeField(auto_now_add=True)


class Stock(models.Model):
	DELETED = '0'
	AVAILABLE = '1'
	SOLD = '2'

	STATUS_CHOICES = (
		(DELETED, "Deleted"),
		(AVAILABLE, "Available"),
		(SOLD, "Sold"),
	)

	stock_no = models.CharField(max_length=100)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	stock_total = models.PositiveIntegerField(default=1)
	stock_on_hand = models.PositiveIntegerField()
	status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=AVAILABLE,
    )
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.stock_no


class Favorite(models.Model):
	favorite_no = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	is_favorite = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.favorite_no


class Comment(models.Model):
	INACTIVE = '0'
	ACTIVE = '1'

	STATUS_CHOICES = (
		(INACTIVE, "Inactive"),
		(ACTIVE, "Active"),
	)

	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	