from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from .models import Product, Customer,Order,OrderItem,ShippingAddress
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,guestOrder
# Create your views here.

def store(request):
    products = Product.objects.all()
    try: 
            cart = json.loads(request.COOKIES['cart'])
    except:
            cart = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        print(order)
        cartItems = order.get_cart_items
        shipping = order.shipping
        context = {
            'products' : products,
            'cartItems':cartItems,
            'shipping' : shipping,
        } 
    else:
        cookieData = cookieCart(request)
        cookieData['products'] = products
        context = cookieData
    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer,complete=False)
        print(order[0])
        items = order[0].orderitem_set.all()
        cartItems = order[0].get_cart_items
        context = {'items':items, 'order':order[0], 'cartItems':cartItems}
    else: 
        cookieData = cookieCart(request)
        context = cookieData
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        isLogged = True if request.user.is_authenticated else False
        return render(request,'store/checkout.html',{'order':order, 'items':items, 'isLogged': isLogged,'cartItems':cartItems})
    else:
        cookieData = cookieCart(request)
        isLogged = True if request.user.is_authenticated else False
        cookieData['isLogged'] = isLogged
        context = cookieData
        return render(request,'store/checkout.html',context)


def update_cart(request):
    content = json.loads(request.body)
    print(type(content))
    productId = content['productId']
    action = content['action']
    print(productId, action)
    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        orderItem,created = OrderItem.objects.get_or_create(product=product, order=order)

        if action=="add":
            orderItem.quantiy += 1
        else: 
            orderItem.quantiy -=1
        
        if orderItem.quantiy<=0:
            orderItem.delete()
        
        orderItem.save()
    return JsonResponse("This is it",safe=False)


def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        print(data['shipping'])
        if(order.shipping==True):
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    else:
        print("You aren't logged in")
        order,customer = guestOrder(request,data)

    total = (data['form']['total'])
    order.transaction_id = transaction_id
    print(float(total)==float(order.get_cart_total))
    if(float(total)==float(order.get_cart_total)):
        order.complete = True
    order.save()      
    return JsonResponse('Order is being processed..',safe=False)