from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import Item, Order, OrderItem, Discount, Tax


class Command(BaseCommand):
    help = 'Load initial data for production'

    def handle(self, *args, **options):
        # Создать суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Суперпользователь создан'))

        # Создать товары
        if not Item.objects.exists():
            items_data = [
                {
                    'name': 'MacBook Pro 16"',
                    'description': 'Профессиональный ноутбук Apple с процессором M3 Pro',
                    'price': 2499.00
                },
                {
                    'name': 'iPhone 15 Pro',
                    'description': 'Новейший смартфон Apple с камерой Pro',
                    'price': 999.00
                },
                {
                    'name': 'AirPods Pro',
                    'description': 'Беспроводные наушники с активным шумоподавлением',
                    'price': 249.00
                },
                {
                    'name': 'Magic Mouse',
                    'description': 'Беспроводная мышь Apple с Multi-Touch поверхностью',
                    'price': 79.00
                }
            ]
            
            for item_data in items_data:
                Item.objects.create(**item_data)
            
            self.stdout.write(self.style.SUCCESS('Товары созданы'))

        # Создать заказ с несколькими товарами
        if not Order.objects.exists():
            order = Order.objects.create()
            
            # Добавить товары в заказ
            items = Item.objects.all()[:3]  # Первые 3 товара
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=1
                )
            
            self.stdout.write(self.style.SUCCESS('Заказ создан'))

        # Создать скидки
        if not Discount.objects.exists():
            Discount.objects.create(
                name='Скидка новому клиенту',
                percent=10.00
            )
            self.stdout.write(self.style.SUCCESS('Скидки созданы'))

        # Создать налоги
        if not Tax.objects.exists():
            Tax.objects.create(
                name='НДС',
                percent=20.00
            )
            self.stdout.write(self.style.SUCCESS('Налоги созданы'))

        self.stdout.write(self.style.SUCCESS('Начальные данные загружены!')) 