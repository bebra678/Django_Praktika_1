from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import datetime


class Category(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    name = models.CharField(max_length=30, unique=True, default='Эскиз', help_text='Категории', verbose_name='Категории', error_messages={'unique': "Такая категория уже существует!"})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Design(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    name = models.CharField(max_length=30, unique=True, help_text='название', verbose_name='Название', error_messages={'unique': "Такая заявка уже существует!"})
    info = models.CharField(max_length=50, help_text='Введите описание', verbose_name='Описание', null=True)
    image = models.ImageField(upload_to='images/',  verbose_name='Изображение', null=False, blank=False)
    date = models.DateField(default=datetime.today(), null=True, verbose_name='Дата')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True, to_field='id')
    # blank=False определяет, будет ли поле обязательным в формах.
    comment = models.TextField(max_length=400, verbose_name='Комментарий', null=False, blank=False)
    # on_delete=models.CASCADE = если категория поста будет удалена, то удалятся и посты
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категории')
    NEW = 'new'
    LOAD = 'load'
    READY = 'ready'
    LOAN_STATUS = (
        (NEW, 'Новая'),
        (LOAD, 'Принято в работу'),
        (READY, 'Выполнено'),
    )

    status = models.CharField(max_length=30, choices=LOAN_STATUS, default='new', help_text='Статус', verbose_name='Статус')

    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.name


