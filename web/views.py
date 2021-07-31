from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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
        following = False
        if Relationship.objects.filter(user=self.request.user, following_user=self.object).count() > 0:
            following = True
        context["following"] = following
        context["form"] = RelationshipForm(initial={'user':self.request.user, 'following_user':self.object})
        return context
    
class FollowingListView(ListView):
    model = Relationship
    template_name = 'following_list.html'
    
    def get_queryset(self, **kwargs):
        queryset = Relationship.objects.filter(user=self.kwargs['pk'])
        return queryset
    

class RelationshipProcess(LoginRequiredMixin, View):

    def post(self, request):
        form = RelationshipForm(request.POST)
        if form.is_valid():
            relationship = form.save()
            messages.success(request, "Successfully follow {0}".format(relationship.following_user))
            return HttpResponseRedirect(reverse('profile', kwargs={'pk':relationship.following_user.id}))
        else:
            messages.error(request, "An error has occured, please try again")
            return HttpResponseRedirect(reverse('profile', kwargs={'pk':relationship.following_user.id}))

# create the unfollow process
class UnfollowProcess(LoginRequiredMixin, View):

    def post(self, request):
        id = request.POST.get('id')
        relationship = Relationship.objects.get(id=id)
        relationship.delete()
        relationship.save() 
        print(id)

        return HttpResponseRedirect(reverse('profile', kwargs={'pk':self.kwargs['pk']}))

class RelationshipCreateView(LoginRequiredMixin, CreateView):
    model = Relationship
    fields = '__all__'
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('profile', kwargs={'pk':self.kwargs['pk']})
