from django.urls import path
from .views import HomeView, FrogsListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('frogs', FrogsListView.as_view(), name='frogs'),
]
