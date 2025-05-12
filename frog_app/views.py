from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction
from datetime import date

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


class RandomFrogView(TemplateView):
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
