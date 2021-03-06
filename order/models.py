from ckeditor.fields import RichTextField
from django.db import models

class Order_days(models.Model):
    order_day = models.DateField(default='1900-01-01')
    reibekuchen = models.BooleanField(default=False)
    spiessbraten = models.BooleanField(default=False)

    def __str__(self):
        order_day_string = str(self.order_day)
        return order_day_string

class Order_times(models.Model):
    order_time = models.DateTimeField()
    reserved = models.BooleanField(default=False)
    booked = models.BooleanField(default=False)

    def __str__(self):
        order_time_string = str(self.order_time)
        return order_time_string

class Order(models.Model):
    name = models.CharField(max_length=100, blank=False)
    callnumber = models.CharField(max_length=25, blank=False)
    email = models.CharField(max_length=75, blank=True)
    order_day = models.DateField(default='1900-01-01')
    order_time = models.DateTimeField(default='1900-01-01 00:00:00')
    order_long = models.CharField(max_length=500, blank=True)
    wishes = models.TextField(blank=True)
    price = models.CharField(max_length=10, blank=True)
    session = models.CharField(max_length=100, blank=True)
    session_time = models.DateTimeField(default='1900-01-01 00:00:00')

    def __str__(self):
        return self.name

#Dieses model wird aktuell nicht verwendet
class Order_details(models.Model):
    product = models.CharField(max_length=100, blank=False)
    product_count = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.PROTECT)

    def __str__(self):
        return self.product


class Content_text(models.Model):
    content_kurz = models.CharField(max_length=256, default='')
    content_lang = RichTextField()

    def __str__(self):
        return self.content_kurz