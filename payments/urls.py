from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('buy/<int:item_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('buy_order/<int:order_id>/', views.create_order_checkout_session, name='create_order_checkout_session'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
] 