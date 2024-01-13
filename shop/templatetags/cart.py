from django import template

register = template.Library()

@register.filter(name="is_in_cart")
def is_in_cart(product,cart):
    keys = cart.keys()
    for id in keys:
        
        if int(id) == product.id :       
            return True
    return False


@register.filter(name="cart_qty")
def cart_qty(product,cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return False

@register.filter(name="price_total")
def price_total(product,cart):
    return product.price*cart_qty(product,cart)

@register.filter(name="total_cart_price")
def total_cart_price(products,cart):
    sum=0
    for s in products:
        sum = sum + price_total(s,cart)
    return sum

@register.filter(name="cart_show_qty")
def cart_show_qty(cart):
    sum = 0
    prod = cart.values()
    for s in prod:
        sum = sum + s
    return sum

