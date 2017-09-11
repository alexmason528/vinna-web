## TODO Delete Account App - Move to Member App
import plivo

from django.utils.translation import ugettext as _
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.conf import settings as django_settings

import json
import requests
from requests.auth import HTTPBasicAuth
import re
from server.account.models import AccountReferral
import jwt
import short_url
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

# Redirect to iTunes or Google Play store depending on device.
def download_redirect(request):
  """
  # Let's assume that the visitor uses an iPhone...
  request.user_agent.is_mobile # returns True
  request.user_agent.is_tablet # returns False
  request.user_agent.is_touch_capable # returns True
  request.user_agent.is_pc # returns False
  request.user_agent.is_bot # returns False

  # Accessing user agent's browser attributes
  request.user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
  request.user_agent.browser.family  # returns 'Mobile Safari'
  request.user_agent.browser.version  # returns (5, 1)
  request.user_agent.browser.version_string   # returns '5.1'

  # Operating System properties
  request.user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
  request.user_agent.os.family  # returns 'iOS'
  request.user_agent.os.version  # returns (5, 1)
  request.user_agent.os.version_string  # returns '5.1'

  # Device properties
  request.user_agent.device  # returns Device(family='iPhone')
  request.user_agent.device.family  # returns 'iPhone'
  """
  version = '';
  if request.iPhone:
    device = 'iPhone'
  elif request.iPad:
    device = 'iPad'
  elif request.iPod:
    device = 'iPod'
  elif request.Android:
    device = 'Android'
    version = request.Android.version
  else:
    device = '---'

  context = { 'device':device, 'version':version }
  if request.Android:
    return redirect('https://play.google.com/apps/testing/com.vinna.mapp')
  elif request.iPhone:
    response = HttpResponse("", status=302)
    response['Location'] = "itms://itunes.apple.com/us/app/testflight/id899247664?mt=8#"
    return response
  else:
    return render(request, 'client_member/download_redirect.html', context)


# Download App
def download(request):
  referral_code = None
  message_sent = False

  if request.user.is_authenticated:
    print ('yay!')
  else:
    print ('boo!')

  if request.method == "POST":
    form_download = DownloadForm(request.POST)

    if (form_download.is_valid()):
      email = form_download.cleaned_data.get('email')
      phone = ''.join(str(x) for x in re.findall(r'\d+', form_download.cleaned_data.get('email')))
      account = form_download.cleaned_data.get('account')

      # normalize phone number
      phone_with_prefix = phone
      if (not phone.startswith('1')): phone_with_prefix = '1' + phone
      else: phone = phone[1:]

      if account:
        account_data = {
          'account_id': account,
          'friend_email_or_phone': email,
          'friend_ip': get_ip(request),
          'friend_user_agent': request.META['HTTP_USER_AGENT'],
          'friend_referrer': request.META['HTTP_REFERER']
        }

        # if phone number, set phone #          
        if len(phone) == 10:
          account_data['friend_email_or_phone'] = phone

        account_referral = AccountReferral.objects.create(**account_data)

      else: # No referral account provided.
        account_data = {
          'account_id': 1,
          'friend_email_or_phone': email,
          'friend_ip': get_ip(request),
          'friend_user_agent': request.META['HTTP_USER_AGENT'],
          'friend_referrer': request.META['HTTP_REFERER']
        }

        account_referral = AccountReferral.objects.create(**account_data)
      
        # TODO Check and ensure that response is good.
      version = '';
      if request.iPhone:
        device = 'iPhone'
      elif request.iPad:
        device = 'iPad'
      elif request.iPod:
        device = 'iPod'
      elif request.Android:
        device = 'Android'
        version = request.Android.version
      else:
        device = '---'

      context = { 'device':device, 'version':version }
      if request.Android:
        return redirect('https://play.google.com/apps/testing/com.vinna.mapp')
      elif request.iPhone:
        response = HttpResponse("", status=302)
        response['Location'] = "itms://itunes.apple.com/us/app/testflight/id899247664?mt=8#"
        return response
      else:
        return render(request, 'client_member/download_unsupported_device.html', context)      

    else:
      print (form_download._errors)
      print ('failed email or phone')

  elif request.method == "GET":
    if 'code' in request.GET:
      referral_code = request.GET['code']
    else:
      referral_code = None
# Verify that referral = None, member_id = None did not break functionality as expected.
    if referral_code:
      account_id = short_url.decode_url(referral_code)
    else:
      account_id = None

    if request.user.is_authenticated:
      print ('authenticated.')
    else:
      print ('not authenticated.')

    if account_id:
      form_download = DownloadForm({'account': account_id})
    else:
      form_download = DownloadForm()

  context = { 'form_download': form_download, 'referral': referral_code, 'message_sent':message_sent }

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
