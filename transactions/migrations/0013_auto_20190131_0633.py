# Generated by Django 2.1.5 on 2019-01-31 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_auto_20190123_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='purchased_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]