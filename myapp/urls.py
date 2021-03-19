

from django.urls import path, re_path
from myapp.views import home, ProductDetailSlugViews, add_to_cart, cart, contact

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart),
    path('contact/', contact, name='contact'),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugViews.as_view()),
    path('addtocart/<str:slug>', add_to_cart),
    # path('cart/', cart),
]
