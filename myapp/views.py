from django.shortcuts import render, redirect
from .models import Product
from django.views.generic import DetailView
import smtplib

# Create your views here.


def home(request):
    product = Product.objects.all()
    context = {
        'product': product
    }
    cart = request.session.get('cart')
    print(cart)
    return render(request, template_name='myapp/home.html', context=context)


class ProductDetailSlugViews(DetailView):

    queryset = Product.objects.all()
    template_name = "myapp/details.html"


def add_to_cart(request, slug):
    user = None
    item_id = None
    cart = request.session.get('cart')
    if cart is None:
        cart = []
    item = Product.objects.get(slug=slug)
    flag = True
    for cart_obj in cart:
        item_id = cart_obj.get('item')
        if item_id == item.id:
            flag = False
            cart_obj['quentity'] = cart_obj['quentity']+1
    if flag:
        cart_obj = {
            'item': item.id,
            'quentity': 1
        }
        cart.append(cart_obj)
    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    return redirect(return_url)


def cart(request):
    cart = request.session.get('cart')
    if request.method == "POST":
        product_id = int(request.POST['product-id'])
        quentity = request.POST['quentity']
        if cart is None:
            cart = []
        for i in range(len(cart)):
            if cart[i]['item'] == product_id:
                del cart[i]
                break
    if cart is None:
        cart = []
    for c in cart:
        item_id = c.get('item')
        item = Product.objects.get(id=item_id)
        c['item'] = item
    return render(request, template_name='myapp/cart.html', context={'cart': cart})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('mesg')
        name_sms = name + ':'+msg
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("login@gmail.com", "password")
        server.sendmail("login@gmail.com", email, name_sms)
        server.quit()

        return redirect('/')
    else:
        return render(request, template_name='myapp/home.html')
