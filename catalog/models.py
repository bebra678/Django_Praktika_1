from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import datetime


class Design(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    name = models.CharField(max_length=30, help_text='название', verbose_name='Название')
    info = models.CharField(max_length=50, help_text='Введите описание', verbose_name='Описание', null=True)
    image = models.ImageField(upload_to='images/',  verbose_name='Изображение', null=False)
    date = models.DateField(default=datetime.today(), null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True,
                             to_field='id')
    comment = models.TextField(max_length=400, verbose_name='Комментарий', null=False, blank=True)

    NEW = 'new'
    LOAD = 'load'
    READY = 'ready'
    LOAN_STATUS = (
        (NEW, 'Новая'),
        (LOAD, 'Принято в работу'),
        (READY, 'Выполнено'),
    )

    status = models.CharField(max_length=30, choices=LOAN_STATUS, default='new', help_text='Статус',
                              verbose_name='Статус')

    SKETCH = 'sketch'
    TWO_D = '2_D'
    THREE_D = '3_D'
    CATEGORIES = (
        (SKETCH, 'Эскиз'),
        (TWO_D, '2D'),
        (THREE_D, '3D'),
    )

    category = models.CharField(max_length=30, choices=CATEGORIES, default='Эскиз', help_text='Категории',
                                verbose_name='Категории')

    def __str__(self):
        return self.name


