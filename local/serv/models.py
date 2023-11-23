from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class ServUser(AbstractUser):
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    name = models.CharField(max_length=255, verbose_name='Имя')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество')
    username = models.CharField(max_length=255, unique=True, verbose_name='Логин', db_column='username')
    email = models.EmailField(unique=True, verbose_name='Email')
    consent = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')

    def clean(self):
        if not self.consent:
            raise ValidationError('Необходимо дать согласие на обработку персональных данных')


# from django.db.models.signals import pre_delete
# from django.dispatch import receiver

class Category(models.Model):
    category_title = models.CharField(max_length=200, unique=True, help_text='Напишите категорию для дизайна интерьера')

    def __str__(self):
        return self.category_title



    def delete(self, *args, **kwargs):
        for request in DesignRequest.objects.filter(category=self):
            request.delete()
        super(Category, self).delete(*args, **kwargs)

from django.core.validators import FileExtensionValidator, validate_image_file_extension


class DesignRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='design_photos/', validators=[validate_image_file_extension, FileExtensionValidator(['bmp', 'jpg', 'jpeg', 'png'], message='Allowed datatypes: bmp, jpg, jpeg, png')])
    image_design = models.ImageField(upload_to='image_designs/', validators=[validate_image_file_extension, FileExtensionValidator(['bmp', 'jpg', 'jpeg', 'png'], message='Allowed datatypes: bmp, jpg, jpeg, png')], blank=True)
    desc = models.CharField(max_length=255)
    choices = (
        ('Новый', 'Новый'),
        ('Принято в работу', 'Принято в работу'),
        ('Выполнено', 'Выполнено'),
    )
    status = models.CharField(max_length=20, choices=choices, default='Новый', blank=True)
    comment = models.TextField(max_length=3000, help_text='Введите произвольный комментарий', blank=True)
    user = models.ForeignKey('ServUser', on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def is_completed(self):
        return self.status == 'Выполнено'

from django.contrib import admin
class RequestAdmin(admin.ModelAdmin):
    list_display = ('category')