from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def login_page(request):
    return render(request, 'registration/login.html')