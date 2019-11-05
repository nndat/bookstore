from django.contrib import admin
from .models import Item, OrderList, Bill, BillItem


admin.site.register(Item)
admin.site.register(OrderList)
admin.site.register(Bill)
admin.site.register(BillItem)
