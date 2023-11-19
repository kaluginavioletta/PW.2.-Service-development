from django.urls import path

from .views import index, profile, LogoutView, LoginView, RegisterDoneView, RegisterUserView, profile_request_add, \
   profile_request_delete

app_name = 'serv'


urlpatterns = [
   path('', index, name='index'),
   path('accounts/login/', LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('accounts/profile/', profile, name='profile'),
   path('register/done/', RegisterDoneView.as_view(), name='register_done'),
   path('register/', RegisterUserView.as_view(), name='register'),
   path('profile/add/', profile_request_add, name='profile_request_add'),
   path('profile/delete/', profile_request_delete, name='profile_request_delete'),
]
