from django.shortcuts import render

def index(request):
   return render(request, 'main/index.html')

# from django.shortcuts import redirect
# from django.contrib.auth import authenticate, login, logout
# from .forms import UserRegistrationForm

# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return redirect('accounts:login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'main/register/registration.html', {'form': form})
#
# def user_login(request):
#     if request.method == 'POST':
#         login_username = request.POST.get('login')
#         login_password = request.POST.get('password')
#         user = authenticate(request, username=login_username, password=login_password)
#         if user is not None:
#             login(request, user)
#             return redirect('main_page')
#         else:
#             return render(request, 'main/register/login.html', {'error_message': 'Неправильный логин или пароль'})
#     else:
#         return render(request, 'main/register/login.html')
#
# def user_logout(request):
#     logout(request)
#     return redirect('main_page')
