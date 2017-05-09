from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
  context = { }
  return render(request, 'client_home/home.html', context)

def login(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request, username=username, password=password)

  if user is not None:
      login(request, user)
      # Redirect to a success page.
      return redirect('/member/')
  else:
    a = 1
      # Return an 'invalid login' error message.
  context = { }
  return render(request, 'client_home/login.html', context)

def how_it_works(request):
  context = { }
  return render(request, 'client_home/how_it_works.html', context)

def learn_to_share(request):
  context = { }
  return render(request, 'client_home/learn_to_share.html', context)

def why_to_help(request):
  context = { }
  return render(request, 'client_home/why_to_help.html', context)

#def contact(request):
#  context = { }
#  return render(request, 'client_home/contact.html', context)

#def about(request):
#  context = { }
#  return render(request, 'client_home/about.html', context)
