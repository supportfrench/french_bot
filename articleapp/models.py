from django.db import models
from datetime import datetime

# Create your models here.


class OrderHistoryModel(models.Model):
    orderId = models.CharField(max_length=200, help_text='order id')
    initial = models.CharField(
        max_length=200, help_text='inital product to update')
    final = models.CharField(max_length=200, help_text='final product')
    status = models.CharField(max_length=200, help_text='status of the update')
    date = models.DateTimeField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.orderId
