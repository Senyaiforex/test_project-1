from django.db import models
from django.contrib.auth.models import User, Group
from .product import Product


class GroupLearn(models.Model):
    """
    Класс-модель группы
    """
    users = models.ManyToManyField(User,
                                   verbose_name='Пользователи',
                                   related_name='groups_learn',
                                   null=True)
    name = models.CharField(verbose_name='Название',
                            max_length=50)
    product = models.ForeignKey(Product,
                                verbose_name='Продукт',
                                on_delete=models.CASCADE,
                                related_name='groups')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name
