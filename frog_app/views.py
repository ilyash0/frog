from django.views.generic import TemplateView, ListView, DetailView

from frog_app.models import Frog


class HomeView(TemplateView):
    template_name = 'frog_app/home.html'


class FrogsListView(ListView):
    model = Frog
    template_name = 'frog_app/frog_list.html'


class FrogsDetailView(DetailView):
    model = Frog
    template_name = 'frog_app/frog_detail.html'
    ordering = ['rarity__id']
# Create your views here.
