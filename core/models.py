from django.conf import settings
from django.utils.translation import gettext as _
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
    ('T', 'Shirts'),
    ('E', 'Shoes'),
)

LABEL_CHOICES = (
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Orange', 'Orange'),
    ('Black', 'Black'),
)


ADDRESS_CHOICES = (
    ('B', 'Billing Address'),
    ('S', 'Shippng Address'),
)




class Color(models.Model):
    color_name = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.color_name

class Category(models.Model):

    """Model definition for Category."""
    name = models.CharField(_("Category Name"), max_length=50)
    description = models.CharField(_("Category Description"), max_length=50)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(
        max_length=100, null=True, blank=True)
    one_click_purchasing = models.BooleanField(default=False
                                               )


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    items = models.ManyToManyField('Item')

    def __str__(self):
        return self.user.username


class CompareList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    items = models.ManyToManyField('Item')

    def __str__(self):
        return self.user.username

class MODELNAME(models.Model):
    """Model definition for MODELNAME."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'MODELNAME'
        verbose_name_plural = 'MODELNAMEs'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        pass



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    ref_code = models.CharField(max_length=20, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField('OrderItem')
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transaction'

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total = total - self.coupon.amount

        return total

    def get_total_order_savings(self):
        order_items = self.items.all()
        total_order_savings = 0
        for item in order_items:
            total_order_savings += item.get_total_savings()
        return total_order_savings

    def get_user_default_shipping_address(self):
        qs = Address.objects.filter(
            user=self.user, address_type='S', default=True)
        if qs.exists():
            return qs[0]
        return None

    def get_user_default_billing_address(self):
        qs = Address.objects.filter(
            user=self.user, address_type='B', default=True)
        if qs.exists():
            return qs[0]
        return None


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True,blank=True)
    # label = models.CharField(choices=LABEL_CHOICES,
    #                          max_length=10, null=True, blank=True)
    # color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={"slug": self.slug})

    def get_add_to_wishlist_url(self):
        return reverse('add-to-wishlist', kwargs={"slug": self.slug})

    def get_add_to_compare_url(self):
        return reverse('add-to-compare', kwargs={"slug": self.slug})

    def get_remove_from_compare_url(self):
        return reverse('remove-from-compare', kwargs={"slug": self.slug})

    def get_add_to_cart_url_from_shop(self):
        return reverse('add-to-cart-from-shop', kwargs={"slug": self.slug})

    def get_add_one_to_cart_url(self):
        return reverse('add-one-to-cart', kwargs={"slug": self.slug})

    def get_add_one_to_cart_url_from_wishlist(self):
        return reverse('add-one-item-to-cart-from-wishlist', kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={"slug": self.slug})

    def get_remove_one_from_cart_url(self):
        return reverse('remove-one-from-cart', kwargs={"slug": self.slug})

    def get_whole_item_from_cart_url(self):
        return reverse('remove-whole-item-from-cart', kwargs={"slug": self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item} * {self.quantity}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_total_savings(self):
        if self.item.discount_price:
            return (self.item.price - self.item.discount_price) * self.quantity
        else:
            return 0

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        else:
            return self.get_total_item_price()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()

    def __str__(self):
        return f'{self.code} - {self.amount}'


class Refund(models.Model):
    order = models.ForeignKey(Order,  on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.pk}"


class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.name


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
