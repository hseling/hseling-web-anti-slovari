from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    created_date = models.DateTimeField(
            default=timezone.now, verbose_name='Дата создания')
    published_date = models.DateTimeField(
            blank=True, null=True, verbose_name='Дата публикации')
    photo = models.ImageField('Фото', upload_to='photos', default='', blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
