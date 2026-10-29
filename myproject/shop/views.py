from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Cart, CartItem


def index(request):
    products = Product.objects.filter(is_active=True)
    
    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.get_item_count()
    
    return render(request, 'shop/index.html', {
        'title': 'Интернет-магазин',
        'products': products,
        'cart_count': cart_count
    })


@login_required
def add_to_cart(request, product_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product = get_object_or_404(Product, id=product_id)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Товар добавлен в корзину',
            'item_count': cart.get_item_count()
        })
    
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('shop:cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('shop:cart')


@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
    
    return redirect('shop:cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = cart.get_total_price()
    
    return render(request, 'shop/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    total = cart.get_total_price()
    
    if request.method == 'POST':
        cart.items.all().delete()
        return render(request, 'shop/order_success.html', {
            'message': 'Заказ успешно оформлен!'
        })
    
    return render(request, 'shop/checkout.html', {
        'items': items,
        'total': total
    })