from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction
from datetime import date

from frog_app.forms import GiftFrogForm
from frog_app.models import Frog, FrogUser, FrogAcquisition


class HomeView(TemplateView):
    template_name = 'frog_app/home.html'


class FrogsListView(ListView):
    model = Frog
    template_name = 'frog_app/frog_list.html'


class FrogsDetailView(DetailView):
    model = Frog
    template_name = 'frog_app/frog_detail.html'
    ordering = ['rarity__id']


class RandomFrogView(LoginRequiredMixin, TemplateView):
    template_name = 'frog_app/home.html'

    def post(self, request, *args, **kwargs):
        if date.today().weekday() == 2:
            already = FrogAcquisition.objects.filter(
                user=request.user,
                date=date.today()
            ).exists()

            if already:
                messages.error(request, 'Вы уже получили сегодня свою лягушку.')
                return redirect('home')

            frog = Frog.objects.order_by('?').first()

            if frog:
                with transaction.atomic():
                    frog_user, created = FrogUser.objects.get_or_create(
                        user=request.user,
                        frog=frog,
                        defaults={'quantity': 1}
                    )

                    if not created:
                        frog_user.quantity += 1
                        frog_user.save()

                    FrogAcquisition.objects.create(user=request.user, frog=frog)
                    messages.success(request, f'Поздравляем! Вы получили лягушку «{frog.name}».')
        else:
            messages.error(request, 'Новые лягушки выдаются только по средам.')

        return redirect('home')


class GiftFrogView(LoginRequiredMixin, FormView):
    template_name = 'frog_app/gift.html'
    form_class = GiftFrogForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['label_suffix'] = ''
        return kwargs

    def form_valid(self, form):
        sender = self.request.user
        recipient = form.get_recipient()
        frog = form.cleaned_data['frog']
        # message = form.cleaned_data['message']

        with transaction.atomic():
            giver_frog = FrogUser.objects.get(user=sender, frog=frog)
            giver_frog.quantity -= 1
            giver_frog.save()
            if giver_frog.quantity <= 0:
                giver_frog.delete()

            recv_record, created = FrogUser.objects.get_or_create(
                user=recipient, frog=frog, defaults={'quantity': 1}
            )
            if not created:
                recv_record.quantity += 1
                recv_record.save()

        return super().form_valid(form)
