from django.urls import path
from .views import index, profile, ServLogoutView, register, LoginUser, request_add, design_request_list, \
   request_detail, change_status, category_list, add_category, DeleteCategoryView
from .views import DeleteRequestView

app_name = 'serv'


urlpatterns = [
   path('', index, name='index'),
   path('login/', LoginUser.as_view(), name='login'),
   path('logout/', ServLogoutView.as_view(), name='logout'),
   path('accounts/profile/', profile, name='profile'),
   path('register/', register, name='register'),
   path('request/add/', request_add, name='request_add'),
   path('request/delete/<int:id>/', DeleteRequestView.as_view(), name='profile_request_delete'),
   path('request/list/', design_request_list, name='design_request_list'),
   path('request/detail/', request_detail, name='request_detail'),
   path('status/change_status/', change_status, name='change_status'),
   path('category/list/', category_list, name='category_list'),
   path('category/add/', add_category, name='add_category'),
   path('category/delete/<int:id>/', DeleteCategoryView.as_view(), name='delete_category'),
]
