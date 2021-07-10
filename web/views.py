from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from .forms import SignUpForm, TweetForm, RelationshipForm
from .models import Profile, Tweet, Relationship

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        form = TweetForm(initial={'user':request.user})
        tweets = Tweet.objects.all()
        return render(request, self.template_name, {'form':form, 'tweets':tweets})
    
    def post(self, request):
        form = TweetForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RelationshipForm(initial={'user':self.request.user, 'following_user':self.object})
        return context
    

class RelationshipCreateView(LoginRequiredMixin, CreateView):
    model = Relationship
    fields = '__all__'
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('profile', kwargs={'pk':self.kwargs['pk']})
