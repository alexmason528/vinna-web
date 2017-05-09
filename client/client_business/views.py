from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render

from core.models import Language

# Create your views here.


def index(request):
  return render(request, 'business/index.html', context)

######## PUBLIC

# Business Directory / Listing
def directory(request):
  context = {  }
  return render(request, 'business/directory.html', context)
#  return HttpResponse("Hello, world. You're at the business directory.")

# Business Profile - Hello Page - Introduction Message + Business Photos/Videos
def profile_hello(request):
  context = {  }
  return render(request, 'business/profile_hello.html', context)

# Business Profile - In Touch - Social Links, Phone, Address, Hours
def profile_intouch(request):
  context = {  }
  return render(request, 'business/profile_intouch.html', context)

# Business Profile - Reviews - Member to write review, read reviews, like reviews. 
def profile_review(request):
  context = {  }
  return render(request, 'business/profile_review.html', context)


# Business Media (Photos + Videos) | return JSON
def media(request):
  # REST - INSERT / UPDATE / DISABLE
  context = {  }
  return { } 

# Business Categories | returns JSON
def category(request):
  context = { 'languages' : Language.objects.all().order_by('text') }
  return { }



# ----------------
######## PRIVATE

# Business Registration
def register(request):
  context = { 'languages' : Language.objects.all().order_by('text') }
  return render(request, 'business/register.html', context)

# Business Welcome after Registration
def welcome(request):
  return render(request, 'business/index.html', context)

# Business Transactions (View is here, but Model is in Transactions App)
def transactions(request):
  context = {  }
  return render(request, 'business/transactions.html', context)

# Business Notifications (View is here, but Model is in Notifications App)
def notifications(request):
  context = {  }
  return render(request, 'business/notifications.html', context)

# Business Settings 
def settings(request):
  context = {  }
  return render(request, 'business/settings.html', context)
