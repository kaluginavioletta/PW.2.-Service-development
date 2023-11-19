from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django import forms

from .models import ServUser, DesignRequest


class RegisterUserForm(forms.ModelForm):
   class Meta:
       model = ServUser
       fields = ('surname', 'name', 'patronymic', 'username', 'email', 'password1', 'password2', 'consent')

   email = forms.EmailField(required=True,
                            label='Адрес электронной почты')
   password1 = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput,
                               help_text=password_validation.password_validators_help_text_html())
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

   def clean_password1(self):
       if 'password1' in self.cleaned_data:
           password1 = self.cleaned_data['password1']
           if password1:
               password_validation.validate_password(password1)
           return password1
       return ''

   def clean(self):
       super().clean()
       password1 = self.cleaned_data.get('password1')
       password2 = self.cleaned_data.get('password2')
       if password1 and password2 and password1 != password2:
           self.add_error('password2', ValidationError(
               'Введенные пароли не совпадают', code='password_mismatch'
           ))
       return self.cleaned_data

   def save(self, commit=True):
       user = super().save(commit=False)
       if 'password1' in self.cleaned_data:
           user.set_password(self.cleaned_data['password1'])
       user.is_active = False
       user.is_activated = False
       if commit:
           user.save()
       return user


class RequestForm(forms.ModelForm):
   class Meta:
       model = DesignRequest
       fields = ['title', 'category', 'desc', 'photo']
       widgets = {'author': forms.HiddenInput}