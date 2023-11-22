from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from .models import DesignRequest

from django.contrib.auth.views import LoginView

from .forms import forms, LoginUserForm, ChangeStatus
from .forms import RegisterUserForm, CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from .forms import RequestForm

from django.views.generic import CreateView, DeleteView

from django.views.generic import TemplateView

from django.contrib.auth import login, authenticate

from .models import DesignRequest, ServUser, Category


def index(request):
    design_requests = DesignRequest.objects.filter(status='Выполнено').order_by('-timestamp')[:4]
    in_progress_count = DesignRequest.objects.filter(status='Принято в работу').count()
    return render(request, 'main/index.html', {'design_requests': design_requests, 'in_progress_count': in_progress_count})


class LoginUser(ServUser, LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    status = request.GET.get('status', '')
    current_user = request.user
    design_requests = DesignRequest.objects.filter(user=current_user)
    context = {'status': status, 'design_requests': design_requests}
    return render(request, 'main/profile.html', context)
class ServLogoutView(LoginRequiredMixin, LogoutView):
   template_name = 'main/logout.html'

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # Create User object
            ServUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                surname=form.cleaned_data['surname'],
                name=form.cleaned_data['name'],
                patronymic=form.cleaned_data['patronymic'],
            )
            messages.success(request, 'Registration successful.')
            return render(request, 'main/index.html')
    else:
        form = RegisterUserForm()
    return render(request, 'main/register_user.html', {'form': form})


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render



@login_required
def request_add(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            return redirect('serv:profile')
    else:
        form = RequestForm()
    return render(request, 'requests/profile_request_add.html', {'form': form })

class DeleteRequestView(LoginRequiredMixin, DeleteView):
   pk_url_kwarg = 'id'
   model = DesignRequest
   template_name = 'requests/profile_request_delete.html'
   success_url = reverse_lazy('serv:profile')

@login_required
def design_request_list(request):
    design_requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'design_requests': design_requests})

def request_detail(request, id):
    req = get_object_or_404(DesignRequest, id=id)
    return render(request, 'admin/request_detail.html', {'request': req})

def change_status(request, request_id):
    design_request = get_object_or_404(DesignRequest, request_id=request_id)
    if design_request.status == 'Новая':
        if request.method == 'POST':
            form = ChangeStatus(request.POST, request.FILES)
            if form.is_valid():
                design_request.status = 'Выполнено'
                design_request.photo = form.cleaned_data['photo']
                design_request.save()
                messages.success(request, 'Статус заявки изменен на "Выполнено"')
                return redirect('serv:profile')
        else:
            form = RequestForm()
        return render(request, 'requests/change_status_to_completed.html', {'form': form})
    else:
        messages.error(request, 'Нельзя изменить статус заявки с другим статусом')
        return redirect('serv:profile')



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

def delete_category(category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')