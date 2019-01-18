from django.contrib import admin
from .models import Transaction, Payment,Order

admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(Order)