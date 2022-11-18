from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import datetime


class Design(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    name = models.CharField(max_length=30, unique=True, help_text='название', verbose_name='Название',
                            error_messages={'unique':"Такая заявка уже существует!"})
    info = models.CharField(max_length=50, help_text='Введите описание', verbose_name='Описание', null=True)
    image = models.ImageField(upload_to='images/',  verbose_name='Изображение', null=False)
    ready_images = models.ImageField(upload_to='ready/', verbose_name='Готовый дизайн', null=False, blank=True)
    date = models.DateField(default=datetime.today(), null=True, verbose_name='Дата')
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

    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.name


