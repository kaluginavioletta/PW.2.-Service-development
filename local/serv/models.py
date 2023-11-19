from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class ServUser(AbstractUser):
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    name = models.CharField(max_length=255, verbose_name='Имя')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество')
    username = models.CharField(max_length=255, unique=True, verbose_name='Логин')
    email = models.EmailField(unique=True, verbose_name='Email')
    consent = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')


    def clean(self):
        if not self.consent:
            raise ValidationError('Необходимо дать согласие на обработку персональных данных')

class Category(models.Model):
    category_title = models.CharField(max_length=200, unique=True, help_text='Напишите категорию для дизайна интерьера')

    def __str__(self):
        return self.category_title

class DesignRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, null=True)
    photo = models.ImageField(upload_to='static/design_photos/', max_length=2*1024*1024)
    desc = models.CharField(max_length=255)
    choises = (
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('сompleted', 'Выполнено'),
    )
    status = models.CharField(max_length=100, choices=choises, default='new')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def is_completed(self):
        return self.status == 'Выполнено'

    def save(self, *args, **kwargs):
        if self.photo.size > 2*1024*1024:
            raise ValidationError("Размер файла фото превышает 2Мб")

        image = Image.open(self.photo)
        image_format = image.format.lower()
        if image_format not in ['jpeg', 'jpg', 'png', 'bmp']:
            raise ValidationError("Фото должно быть в формате JPEG, JPG, PNG или BMP")

        super(DesignRequest, self).save(*args, **kwargs)


