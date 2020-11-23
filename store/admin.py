from django.contrib import admin
from .models import *

# Register your models here.
# Register Product and ProductAdmin
class BookAdmin(admin.ModelAdmin):
   list_display = ['title', 'price', 'discount_price', 'created']
   list_filter = ['title', 'created']
   list_editable = ['discount_price']
   prepopulated_fields = {'slug': ('title',)}
admin.site.register(Book, BookAdmin)

class OrderAdmin(admin.ModelAdmin):
   list_display = ['user', 'ordered', 'received', 'shipping_address', 'ordered_date']
   list_filter = ['ordered', 'ordered_date']
   search_fields = ['user__username', 'ref_code']
   #actions = [make_refund_accepted]
admin.site.register(Order, OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
   list_display = ['user', 'amount', 'timestamp', 'stripe_charge_id']
admin.site.register(Payment, PaymentAdmin)