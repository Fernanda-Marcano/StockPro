from django.shortcuts import render, redirect
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import SignUpForm, ProfileForm, UserForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        print(form)
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})


class UserProfileUpdateView(LoginRequiredMixin, UpdateView): 
    model = Profile 
    form_class = ProfileForm 
    template_name = 'registration/edit_profile.html' 
    success_url = reverse_lazy('detail-profile') 
    
    def get_object(self): 
        return self.request.user.profile_user
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        if self.request.POST: 
            context['user_form'] = UserForm(self.request.POST, instance=self.request.user) 
        else: 
            context['user_form'] = UserForm(instance=self.request.user) 
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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/detail_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


def custom_logout(request):
    logout(request)
    return redirect('list-hierarchy')