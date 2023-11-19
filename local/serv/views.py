from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from . import forms
from .forms import RegisterUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView

from django.views.generic import CreateView

from django.views.generic import TemplateView

from .models import DesignRequest, ServUser


def index(request):
   design_requests = DesignRequest.objects.all()[:4]
   return render(request, 'main/index.html', {'design_requests': design_requests})

class LoginView(LoginView):
   template_name = 'main/login.html'


@login_required
def profile(request):
    design_requests = DesignRequest.objects.filter()
    return render(request, 'main/profile.html', {'design_requests': design_requests})

class LogoutView(LoginRequiredMixin, LogoutView):
   template_name = 'main/logout.html'

class RegisterUserView(CreateView):
   model = ServUser
   template_name = 'main/register_user.html'
   form_class = RegisterUserForm
   success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
   template_name = 'main/register_done.html'


from django.shortcuts import render, redirect
from .models import DesignRequest

def create_design_request(request):
    if request.method == 'POST':
        form = DesignRequest(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            return redirect('my_requests')
    else:
        form = DesignRequest()
    return render(request, 'create_design_request.html', {'form': form})


def my_requests(request):
   requests = DesignRequest.objects.filter(user=request.user)
   return render(request, 'profile_request_add.html', {'requests': requests})

from .forms import RequestForm

@login_required
def profile_request_add(request):
   if request.method == 'POST':
       form = RequestForm(request.POST, request.FILES)
       if form.is_valid():
           DesignRequest = form.save()
           formset = RequestForm(request.POST, request.FILES, instance=DesignRequest)
           if formset.is_valid():
               formset.save()
               messages.add_message(request, messages.SUCCESS,
                                    'Объявление добавлено')
               return redirect('main:profile')
   else:
       form = RequestForm(initial={'author': request.user.pk})
       formset = RequestForm()
   context = {'form': form, 'formset': formset}
   return render(request, 'requests/profile_request_add.html', context)




@login_required
def profile_request_delete(request, pk):
    DesignRequest = get_object_or_404(RequestForm, pk=pk)
    if not request.user.is_author(DesignRequest):
       return redirect('serv:profile')
    if request.method == 'POST':
       DesignRequest.delete()
       messages.add_message(request, messages.SUCCESS,
                            'Объявление удалено')
       return redirect('serv:profile')
    else:
       context = {'RequestForm': RequestForm}
       return render(request, 'request/profile_request_delete.html', context)

def Requests(request):
    context = {
        'Requests': DesignRequest.objects.filter(username=request.user)
    }
    status = forms.ModelChoiceField(queryset=DesignRequest.objects.all())
    return render(request, 'main/profile.html', context)
