from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    content = CKEditor5Field('Содержание', config_name='extends', blank=True, null=True)

    def __str__(self):
        return f'{self.author} - {self.title[:25]}'

    def get_absolute_url(self):
        return reverse('ann_detail', args=[str(self.id)])

    class Meta:
        ordering = ('-dateCreation',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('category', args=[str(self.id)])


class Respond(models.Model):
    respond_ann = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    respond_user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Text')
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-dateCreation',)
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'