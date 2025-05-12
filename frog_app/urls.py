from django.urls import path
from .views import HomeView, FrogsListView, RandomFrogView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('frogs', FrogsListView.as_view(), name='frogs'),
    path('get-frog', RandomFrogView.as_view(), name='get-frog'),
]
