from django.db import models
from .product import Product


class Lesson(models.Model):
    """
    Класс-модель урока
    """
    product = models.ForeignKey(Product,
                                verbose_name='Продукт',
                                on_delete=models.CASCADE,
                                related_name='products')
    name = models.CharField(verbose_name='Название',
                            max_length=100)
    link_video = models.CharField(verbose_name='Ссылка на видео',
                                  max_length=200)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name
