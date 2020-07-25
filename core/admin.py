from django.contrib import admin

from core.models import Address, Payment, WishList, Message

from .models import Item, Order, OrderItem, Coupon, Refund, UserProfile, Category, CompareList, Color

# Register your models here.


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_granted=True)


make_refund_accepted.short_description = 'Update Order as Refund Granted '


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'ordered', 'being_delivered',
#                     'received', 'refund_requested', 'refund_granted',
#                     'billing_address',
#                     'shipping_address',
#                     'payment',
#                     'coupon',
#                     )

#     list_display_links = ('billing_address',
#                           'payment',  'billing_address',
#                           'shipping_address',
#                           'coupon',)
#     list_filter = ('ordered', 'being_delivered',
#                    'received', 'refund_requested', 'refund_granted',)

#     search_fields = ('user__username', 'ref_code')

# actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip_code',
        'address_type',
        'default',

    ]
    list_filter = ['default', 'address_type', 'country']

    search_fields = ['user',
                     'street_address',
                     'apartment_address',
                     'country',
                     'zip_code', ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['ref_code','user']

# Transaction I'd, user id, product, quantity, price, discounted price


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)
admin.site.register(Address, AddressAdmin)
# admin.site.register(Payment)
# admin.site.register(Coupon)
# admin.site.register(Refund)
admin.site.register(UserProfile)
# admin.site.register(WishList)
admin.site.register(Category)
# admin.site.register(CompareList)
admin.site.register(Message)
admin.site.register(Color)
