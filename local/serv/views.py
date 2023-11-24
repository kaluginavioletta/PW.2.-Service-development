from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.views import View

from .models import DesignRequest

from django.contrib.auth.views import LoginView

from .forms import forms, LoginUserForm, CompletedFormStatus, DoneFormStatus
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
    return render(request, 'main/index.html', {'design_requests': design_requests,
                                               'in_progress_count': in_progress_count})

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

def all_requests(request):
    design_requests = DesignRequest.objects.all()
    return render(request, 'admin/all_requests.html', {'design_requests': design_requests})

@login_required
def request_add(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            messages.add_message(request, messages.SUCCESS, 'Заявка добавлена')
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

class ChangeStatusToDoneView(View):
    def get(self, request, id):
        design_request = DesignRequest.objects.get(id=id)
        form = DoneFormStatus(instance=design_request)
        return render(request, 'admin/status_done.html', {'form': form})

    def post(self, request, id):
        design_request = DesignRequest.objects.get(id=id)
        form = DoneFormStatus(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            design_request.status = 'Выполнено'
            design_request.image_design = form.cleaned_data['image_design']
            design_request.save()
            return redirect('serv:all_requests')
        return render(request, 'admin/status_done.html', {'form': form})

class ChangeStatusToCompletedView(View):
    def get(self, request, id):
        design_request = DesignRequest.objects.get(id=id)
        form = CompletedFormStatus(instance=design_request)
        return render(request, 'admin/status_completed.html', {'form': form})

    def post(self, request, id):
        design_request = DesignRequest.objects.get(id=id)
        form = CompletedFormStatus(request.POST, instance=design_request)
        if form.is_valid():
            design_request.status = 'Принято в работу'
            design_request.comment = form.cleaned_data['comment']
            design_request.save()
            return redirect('serv:all_requests')
        return render(request, 'admin/status_completed.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Категория добавлена')
            return redirect('serv:category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

class DeleteCategoryView(LoginRequiredMixin, DeleteView):
   pk_url_kwarg = 'id'
   model = Category
   template_name = 'admin/category_delete.html'
   success_url = reverse_lazy('serv:category_list')
