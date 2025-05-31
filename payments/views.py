from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order, OrderItem
import stripe
from django.conf import settings



stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    """Главная страница со списком всех товаров"""
    items = Item.objects.all()
    context = {
        'items': items,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payments/home.html', context)


def item_detail(request, item_id):
    """Отображение страницы товара с кнопкой покупки"""
    item = get_object_or_404(Item, id=item_id)
    context = {
        'item': item,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payments/item_detail.html', context)


@csrf_exempt
def create_checkout_session(request, item_id):
    """Создание Stripe Checkout Session для товара"""
    if request.method == 'GET':
        item = get_object_or_404(Item, id=item_id)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': item.get_display_price(),
                            'product_data': {
                                'name': item.name,
                                'description': item.description,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri(f'/item/{item.id}/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def create_order_checkout_session(request, order_id):
    """Создание Stripe Checkout Session для заказа"""
    if request.method == 'GET':
        order = get_object_or_404(Order, id=order_id)
        
        try:
            line_items = []
            for order_item in order.orderitem_set.all():
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order_item.item.get_display_price(),
                        'product_data': {
                            'name': order_item.item.name,
                            'description': order_item.item.description,
                        },
                    },
                    'quantity': order_item.quantity,
                })
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri(f'/order/{order.id}/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def order_detail(request, order_id):
    """Отображение страницы заказа с кнопкой покупки"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payments/order_detail.html', context)


def success_view(request):
    """Страница успешной оплаты"""
    return render(request, 'payments/success.html')


def cancel_view(request):
    """Страница отмененной оплаты"""
    return render(request, 'payments/cancel.html')
