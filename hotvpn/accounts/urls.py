
from django.urls import path, include

from .views import login_page


urlpatterns = [
    # user pages urls
    path('login/', login_page)


]