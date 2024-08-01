
from django.urls import path
from .views import login_view, callback_view, home

urlpatterns = [
    path('login/', login_view, name='accounts_login'),
    path('callback', callback_view, name='accounts_callback'),
    path('', home, name='home'),
]
