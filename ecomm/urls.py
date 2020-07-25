from django.conf import settings
from django.conf.global_settings import MEDIA_URL
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import (AddCoupon, CheckOut, ItemDetailView, ItemListView,complete_order,my_order_detail,
                        OrderSummary, PaymentView, RemoveCoupon, shop_grid_new,shop_by_category,my_orders,
                        RequestRefundView, add_one_item_to_cart, add_to_cart, add_to_compare, get_results,shop_by_price,
                        home, products, remove_coupon, remove_from_cart, search_products,shop_by_color,
                        remove_one_from_cart, remove_whole_item_from_cart, compare, remove_from_compare,
                        MensBikesView, shoesView, shop_grid, contact, add_to_wishlist, WishListView, add_one_item_to_cart_from_wishlist, add_to_cart_from_shop)
from ecomm.settings import STATIC_ROOT

urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('shop/', shop_grid_new, name='shop'),
#     path('shop-by-color/<value>', shop_by_color, name='shop-by-color'),
    path('shop-by-category/<value>', shop_by_category, name='shop-by-category'),
    path('shop-by-price/<value>', shop_by_price, name='shop-by-price'),
    path('contact/', contact, name='contact'),
    path('complete-order/', complete_order, name='complete-order'),
    path('my-orders/', my_orders, name='my-orders'),
    path('order-detail/<int:pk>/', my_order_detail, name='order-detail'),
    #     path('cart/', contact , name='cart'),

    path('cart/', OrderSummary.as_view(), name='order-summary'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('add-one-item-to-cart-from-wishlist/<slug>/',
         add_one_item_to_cart_from_wishlist, name='add-one-item-to-cart-from-wishlist'),
    path('add-to-cart/<slug>/', add_to_cart_from_shop,
         name='add-to-cart-from-shop'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product_detail'),
    path('compare/', compare, name='compare'),
    path('add-to-compare/<slug>/', add_to_compare, name='add-to-compare'),
    path('remove-from-compare/<slug>/',
         remove_from_compare, name='remove-from-compare'),
    path('search-products/', search_products, name='search-products'),
    path('get-grid-with-pagination-and-sort/', get_results,
         name='get-grid-with-pagination-and-sort'),



    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('mens-bikes/', MensBikesView, name='mensbikes'),
    path('shoes/', shoesView, name='shoes'),
    path('checkout/', CheckOut.as_view(), name='checkout'),
    path('products/', products, name='products'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
    path('add-coupon/', AddCoupon.as_view(), name='add-coupon'),
    path('remove-coupon/', remove_coupon, name='remove-coupon'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-wishlist/<slug>/', add_to_wishlist, name='add-to-wishlist'),
    path('add-one-to-cart/<slug>/', add_one_item_to_cart, name='add-one-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-one-from-cart/<slug>/',
         remove_one_from_cart, name='remove-one-from-cart'),
    path('remove-whole-item-from-cart/<slug>/',
         remove_whole_item_from_cart, name='remove-whole-item-from-cart'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
