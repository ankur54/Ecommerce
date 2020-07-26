from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Message

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    # ('P', 'Paypal'),

)


class CheckoutForm(forms.Form):
    shipping_address1 = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(Select country)').formfield(required=False,
                                                                              widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100', 'id': 'shipping_country'}))
    shipping_zip = forms.CharField(required=False)
    billing_same_shipping_address = forms.BooleanField(required=False)
    save_as_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(required=False,
                                       widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

    billing_address1 = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(Select country)').formfield(required=False,
                                                                             widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100', 'id': 'billing_country'}))
    billing_zip = forms.CharField(required=False)
    save_as_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)


class PaymentForm(forms.Form):
    save_card_info = forms.BooleanField(required=True)
    stripeToken = forms.CharField(required=True)
    use_default_card = forms.BooleanField(required=False)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class AddCouponForm(forms.Form):
    code = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Use MINUS10",
                                                                   "aria-label": "Recipient's username", "aria-describedby": "basic-addon2"}))


class RequestRefundForm(forms.Form):
    ref_code = forms.CharField()
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    email = forms.EmailField()
