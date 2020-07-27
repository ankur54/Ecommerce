from django import template
from core.models import OrderItem,WishList
from django.db.models import Sum,Count


register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        return OrderItem.objects.filter(user=user,ordered=False).aggregate(Sum('quantity'))['quantity__sum'] or 0
    else:
        return 0

@register.filter
def is_item_in_cart(user,item):
    if user.is_authenticated:
        return len(OrderItem.objects.filter(user=user,item=item,ordered=False)) != 0
    else:
        return 0

@register.filter
def is_item_in_wishlist(user,itemId):
    if user.is_authenticated:
        return len(WishList.objects.filter(user=user,items__id=itemId)) != 0
    else:
        return 0




@register.filter
def wishlist_item_count(user):
    if user.is_authenticated:
        # Keyword.objects.all().annotate(article_count=models.Count('article'))[0].article_count
        # return WishList.objects.filter(user=user).annotate(item_count=Count('items')) or 0
        return WishList.objects.filter(user=user).annotate(item_count=Count('items'))
        WishList.objects.filter(user=user).annotate(cnt=Count('items')).order_by('-cnt')[0]
    else:
        return 0