from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """
    Класс-модель продукта
    """
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='products')
    name = models.CharField(verbose_name='Название',
                            max_length=100)
    started_at = models.DateTimeField(verbose_name='Дата и время старта')
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=8,
                                decimal_places=2)
    max_count_users = models.PositiveIntegerField(verbose_name='Максимальное число пользователей в группе')
    min_count_users = models.PositiveIntegerField(verbose_name='Минимальное число пользователей в группе')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

