from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from frog_app.models import FrogUser
from .forms import SignUpForm, CustomAuthenticationForm, UserSettingsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Замените 'home' на нужный URL
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings_form'] = UserSettingsForm(instance=self.request.user)
        frog_users = FrogUser.objects.select_related('frog', 'frog__rarity').filter(user=self.request.user)
        context['frog_users'] = frog_users
        return context

    def post(self, request, *args, **kwargs):
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        context = self.get_context_data()
        context['settings_form'] = form
        return self.render_to_response(context)
