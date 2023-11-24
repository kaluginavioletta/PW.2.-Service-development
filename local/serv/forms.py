from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.urls import reverse_lazy, reverse

from .models import ServUser, DesignRequest, Category

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class RegisterUserForm(forms.ModelForm):
   class Meta:
       model = ServUser
       fields = ['surname', 'name', 'patronymic', 'username', 'email', 'password', 'password2', 'consent']

   email = forms.EmailField(required=True,
                            label='Адрес электронной почты')
   password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
   password2 = forms.CharField(label='Пароль (повторно)',
                               widget=forms.PasswordInput,
                               help_text='Повторите тот же самый пароль еще раз')


   def clean_surname(self):
       surname = self.cleaned_data['surname']
       if not surname.isalpha():
           raise forms.ValidationError("Фамилия должна состоять только из букв")
       return surname

   def clean_name(self):
       name = self.cleaned_data['name']
       if not name.isalpha():
           raise forms.ValidationError("Имя должно состоять только из букв")
       return name

   def clean_patronymic(self):
       patronymic = self.cleaned_data['patronymic']
       if not patronymic.isalpha():
           raise forms.ValidationError("Отчество должно состоять только из букв")
       return patronymic

   def clean_username(self):
       username = self.cleaned_data['username']
       if not username.isalnum():
           raise forms.ValidationError("Логин должен состоять только из латинских букв и цифр")
       if ServUser.objects.filter(username=username).exists() and not self.instance:
           raise forms.ValidationError("Пользователь с таким логином уже существует")
       return username

   def clean_email(self):
       email = self.cleaned_data['email']
       if ServUser.objects.filter(email=email).exists():
           raise forms.ValidationError("Пользователь с таким почтовым адресом уже существует")
       return email

   def clean(self):
       super().clean()
       password = self.cleaned_data.get('password')
       password2 = self.cleaned_data.get('password2')
       if password and password2 and password != password2:
           self.add_error('password2', ValidationError(
               'Введенные пароли не совпадают', code='password_mismatch'
           ))
       return self.cleaned_data

   def save(self, commit=True):
       user = super().save(commit=False)
       if 'password' in self.cleaned_data:
           user.set_password(self.cleaned_data['password'])
       user.is_active = False
       user.is_activated = False
       if commit:
           user.save()
       return user

class RequestForm(forms.ModelForm):
    user = forms.HiddenInput()
    class Meta:
       model = DesignRequest
       fields = ['title', 'category', 'desc', 'photo']
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Это изображение превышает 2 Мб")
        return photo

    def save(self, commit=True, user=None):
        request = super().save(commit=False)
        request.user = user
        if commit:
            request.save()
        return request


class DoneFormStatus(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['image_design']

    def clean_image_design(self):
        image_design = self.cleaned_data.get('image_design')
        if image_design:
            if image_design.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Это изображение превышает 2 Мб")
        else:
            raise forms.ValidationError('Необходимо добавить изображение')
        return image_design

class CompletedFormStatus(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['comment']
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment:
            raise forms.ValidationError('Необходимо написать комментарий')
        return comment

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_title']
