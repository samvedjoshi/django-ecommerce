import json
from .models import *


def cookieCart(request):
    try: 
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(cart)
    items = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems = 0
    for key in cart:
        try:
            cartItems += cart[key]['quantiy']
            product = Product.objects.get(id=key)
            total = product.price*cart[key]['quantiy']
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[key]['quantiy']
            item = {
            'product':{
                'id' : product.id,
                'price' : product.price,
                'image' : product.image,
                'name' : product.name,
            },
            'quantiy' : cart[key]['quantiy'],
            'get_total' : total,
            }
            items.append(item)
            if product.digital==False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems,'order':order,'items':items}



def guestOrder(request,data):
    name = data['form']['name']
    email = data['form']['email']
    cartData = cookieCart(request)
    items = cartData['items']
    customer,created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer = customer,
        complete = False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        quantity = item['quantiy']
        orderItems = OrderItem.objects.create(
            product = product,
            order = order,
            quantiy = quantity,
        )
    return order,customer