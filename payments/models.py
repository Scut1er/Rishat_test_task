from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return self.name
    
    def get_display_price(self):
        """Возвращает цену в центах для Stripe"""
        return int(self.price * 100)


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem', verbose_name="Товары")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    def __str__(self):
        return f"Заказ #{self.id}"
    
    def get_total_price(self):
        """Возвращает общую стоимость заказа"""
        total = sum(order_item.get_total_price() for order_item in self.orderitem_set.all())
        return total
    
    def get_display_total_price(self):
        """Возвращает общую стоимость в центах для Stripe"""
        return int(self.get_total_price() * 100)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    
    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
    
    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
    
    def get_total_price(self):
        """Возвращает стоимость товаров данного типа в заказе"""
        return self.item.price * self.quantity


class Discount(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название скидки")
    percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент скидки")
    stripe_coupon_id = models.CharField(max_length=100, blank=True, verbose_name="ID купона Stripe")
    
    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
    
    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Tax(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название налога")
    percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент налога")
    stripe_tax_rate_id = models.CharField(max_length=100, blank=True, verbose_name="ID налога Stripe")
    
    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"
    
    def __str__(self):
        return f"{self.name} ({self.percent}%)"
