from django.contrib import admin
from .models import Order, Order_days, Order_times, Order_details, Content_text

admin.site.register(Order)
admin.site.register(Order_days)
admin.site.register(Order_times)
admin.site.register(Order_details)
admin.site.register(Content_text)


