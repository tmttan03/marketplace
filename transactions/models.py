from django.db import models
from django.contrib.auth.models import User
from .models import Product , Category


class Transaction(models.Model):
	SOLD = '0'
	PENDING = '1'
	AVAILABLE = '2'

	STATUS_CHOICES = (
		(SOLD, "Sold"),
		(PENDING, "Pending"),
		(AVAILABLE, "Available"),
	)

	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	qty = models.IntegerKey(max_digits=100)
	status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=AVAILABLE,
    )
	start_transaction = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Payment(models.Model):
	transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
	amount_due = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	purchased_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name