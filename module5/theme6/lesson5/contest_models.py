from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Contest(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.IntegerField(
        verbose_name='Цена',
        help_text='Рекомендованная розничная цена',
        validators=[
        	MinValueValidator(10),
        	MaxValueValidator(100),
        ],
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,  # Поле необязательно
        null=True    # Разрешены NULL-значения
    )

    def __str__(self):
        return self.title
