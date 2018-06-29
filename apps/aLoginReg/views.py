# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
	return render(request, 'aLoginReg/index.html')

def register(request):
	registerResult = User.objects.validateRegistration(request.POST)

	if type(registerResult) == list:
		for err in registerResult:
			messages.error(request, err)
		return redirect('/')
	return render(request, 'aLoginReg/homepage.html')

def login(request):
	loginResult = User.objects.validateLogin(request.POST)

	if type(loginResult) == list: 
		for err in loginResult: 
			messages.error(request, err)
		return redirect('/')
	return render(request, 'aLoginReg/homepage.html')
