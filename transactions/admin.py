from django.contrib import admin
from .models import Transaction, Payment

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Payment)