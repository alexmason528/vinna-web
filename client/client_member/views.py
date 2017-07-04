## TODO Delete Account App - Move to Member App

from django.utils.translation import ugettext as _
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
import json
import requests
from requests.auth import HTTPBasicAuth
import re
from server.member.models import MemberReferral
import jwt
from core.models import Language

from .forms import UserForm, AccountForm, DownloadForm
from ipware.ip import get_real_ip, get_ip

# Create your views here.
def index(request):
  return HttpResponse("Hello, world. You're at the members index.")

# Express Member Registration | Step 1
def register_step_1(request):
  if request.method == "POST":
#        print(request.POST)
    form_user = UserForm(request.POST)
    form_account = AccountForm(request.POST)

    user_is_valid = form_user.is_valid()
    account_is_valid = form_account.is_valid()
    
    if user_is_valid and account_is_valid :
      print('valid')
      form_user.save()
      
      user = authenticate(request=request, username=request.POST['email'], password=request.POST['password'])
      if user is not None:
        print('logging user in')
        login(request, user)
      else:
        print('unable to log in user')

#      new_user = User.objects.create_user(**form_user.cleaned_data)
#            login(new_user)

      # redirect, or however you want to get to the main view
      return HttpResponseRedirect('/member/download')
    else:
      print('invalid')
  else:
    form_user = UserForm()
    form_account = AccountForm()

  context = { 'languages' : Language.objects.all().order_by('text'), 'form_account' : form_account, 'form_user' : form_user }

  return render(request, 'client_member/register.html', context)

def logoff(request):
  logout(request)
  return HttpResponseRedirect('/')

# Complete Member Registration | Step 2 
def register_step_2(request):
  context = { 'languages' : Language.objects.all().order_by('text') }
  return render(request, 'client_member/register_step_2.html', context)

# Member Welcome Page after Registration
def welcome(request):
  context = {  }
  return render(request, 'client_member/welcome.html', context)

# Download App
def download(request):
  if request.user.is_authenticated:
    print ('yay!')
  else:
    print ('boo!')

  if request.method == "POST":
    form_download = DownloadForm(request.POST)

    if (form_download.is_valid()):
      email = form_download.cleaned_data.get('email')
      phone = form_download.cleaned_data.get('email')
      member = form_download.cleaned_data.get('member')
      phone = phone.replace("-", "")
      phone = phone.replace("(", "")
      phone = phone.replace(")", "")

      if (not phone.startswith('1')):
        phone = '1' + phone

      if (not re.match("^\d+$", phone)):
        print ('sending email')
        send_mail(
            'Download Vinna App',
            'Downlad the Vinna App to your phone.',
            'kenneth@vinna.me',
            [form_download.cleaned_data.get('email')],
            fail_silently=False,
        )
      else:
        data = {'src':'15612641630','dst':phone,'text':'Download link: http://www.vinna.me/downloadapp'}
        print ('sending text message')
        url = 'http://debug.local/' #'https://api.plivo.com/v1/Account/SAMZC0MGI3MTAWNZIXMT/Message/'
        resp = requests.post(url, data=data, auth=HTTPBasicAuth('SAMZC0MGI3MTAWNZIXMT', 'ODc5ZDU0ZTVjMjViMjAwOGU4MTQ0NTE3NGRmMWYx'))
        print (resp)

      if member:
        if email:
          member_data = {
            'member_id': member,
            'friend_email_or_phone': email,
            'friend_ip': get_ip(request),
            'friend_user_agent': request.META['HTTP_USER_AGENT'],
            'friend_referrer': request.META['HTTP_REFERER']
          }
          
          member_referral = MemberReferral.objects.create(**member_data)

    else:
      print (form_download._errors)
      print ('failed email')

  elif request.method == "GET":
    if 'referral' in request.GET:
      referral = request.GET['referral']

    if referral:
      member_id = jwt.decode(request.GET['referral'], 'secret')

    if request.user.is_authenticated:
      print ('authenticated.')
    else:
      print ('not authenticated.')

    if member_id:
      form_download = DownloadForm({'member': member_id['id']})
    else:
      forms_download = DownloadForm()

  context = { 'form_download': form_download }
  return render(request, 'client_member/download.html', context)

# Member Transactions (View is here, but Model is in Transactions App)
def transactions(request):
  context = {  }
  return render(request, 'client_member/transactions.html', context)

# Member Notifications (View is here, but Model / logic is in Notifications App)
def notifications(request):
  context = {  }
  return render(request, 'client_member/notifications.html', context)

# Settings for Member and Base Account
def settings(request):
  context = {  }
  return render(request, 'client_member/settings.html', context)

# Connect a new Member
def connect_member(request):
  context = {  }
  return render(request, 'client_member/connect_member.html', context)
