from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from .forms import SignUpForm, TweetForm
from .models import Profile

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        form = TweetForm()
        return render(request, self.template_name, {'form':form})

class SignUpView(TemplateView):
    template_name = 'signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, self.template_name, {'form':form})

class ProfileView(LoginRequiredMixin, DetailView):
    model = User

    