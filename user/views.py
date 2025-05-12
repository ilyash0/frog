from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy

from frog_app.models import FrogUser
from .forms import SignUpForm, UserSettingsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView


class SignUpView(FormView):
    template_name = 'user/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')


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
