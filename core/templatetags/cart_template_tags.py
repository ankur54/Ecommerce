from django import template
from core.models import OrderItem
from django.db.models import Sum


register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        # return OrderItem.objects.filter(user=user,ordered=False).count()
        # return OrderItem.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return OrderItem.objects.filter(user=user,ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0
    else:
        return 0