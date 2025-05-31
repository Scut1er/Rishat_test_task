from django.core.management.base import BaseCommand
from payments.models import Item, Order, OrderItem, Discount, Tax


class Command(BaseCommand):
    help = 'Загружает тестовые данные в базу'

    def handle(self, *args, **options):
        # Создаем товары
        item1, created = Item.objects.get_or_create(
            name="MacBook Pro 16",
            defaults={
                'description': "Мощный ноутбук для профессионалов с процессором M1 Pro",
                'price': 2499.99
            }
        )
        
        item2, created = Item.objects.get_or_create(
            name="iPhone 15 Pro",
            defaults={
                'description': "Новейший смартфон Apple с камерой Pro",
                'price': 999.99
            }
        )
        
        item3, created = Item.objects.get_or_create(
            name="AirPods Pro 2",
            defaults={
                'description': "Беспроводные наушники с активным шумоподавлением",
                'price': 249.99
            }
        )
        
        item4, created = Item.objects.get_or_create(
            name="Magic Mouse",
            defaults={
                'description': "Беспроводная мышь Apple с поддержкой жестов",
                'price': 79.99
            }
        )

        # Создаем заказ с несколькими товарами
        order, created = Order.objects.get_or_create(id=1)
        if created:
            OrderItem.objects.create(order=order, item=item1, quantity=1)
            OrderItem.objects.create(order=order, item=item3, quantity=2)
            OrderItem.objects.create(order=order, item=item4, quantity=1)

        # Создаем скидки
        discount1, created = Discount.objects.get_or_create(
            name="Скидка 10%",
            defaults={
                'percent': 10.00,
                'stripe_coupon_id': 'discount_10_percent'
            }
        )
        
        discount2, created = Discount.objects.get_or_create(
            name="Скидка для студентов",
            defaults={
                'percent': 15.00,
                'stripe_coupon_id': 'student_discount'
            }
        )

        # Создаем налоги
        tax1, created = Tax.objects.get_or_create(
            name="НДС",
            defaults={
                'percent': 20.00,
                'stripe_tax_rate_id': 'vat_20_percent'
            }
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно загружены тестовые данные:\n'
                f'- Товары: {Item.objects.count()}\n'
                f'- Заказы: {Order.objects.count()}\n'
                f'- Скидки: {Discount.objects.count()}\n'
                f'- Налоги: {Tax.objects.count()}'
            )
        ) 