from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import SignUpForm, ProfileForm, UserForm

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    #success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, self.request.FILES)
        else:
            context['profile_form'] = ProfileForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        if profile_form.is_valid():
            self.object = form.save()
            profile = profile_form.save(commit=False)
            profile.user = self.object
            profile.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView): 
    model = Profile 
    form_class = ProfileForm 
    template_name = 'registration/edit_profile.html' 
    #success_url = reverse_lazy('profile') 
    
    def get_object(self): 
        return self.request.user.profile_user
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        if self.request.POST: 
            context['user_form'] = SignUpForm(self.request.POST, instance=self.request.user) 
        else: 
            context['user_form'] = SignUpForm(instance=self.request.user) 
            return context 
        
    def form_valid(self, form):
        context = self.get_context_data() 
        user_form = context['user_form'] 
        if user_form.is_valid(): 
            user_form.save() 
            profile_form = form 
            profile_form.instance.user = self.request.user 
            profile_form.save()
            return super().form_valid(form)
        else: 
            return self.form_invalid(form)

def custom_logout(request):
    logout(request)
    return redirect('list-hierarchy')