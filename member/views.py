from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render

from core.models import Language

# Create your views here.
def index(request):
  return HttpResponse("Hello, world. You're at the members index.")

def register(request):
  context = { 'languages' : Language.objects.all().order_by('text') }
  return render(request, 'member/register.html', context)

def login(request):
  return HttpRedirect("Login Successful")

def detail(request):
  return HttpResponse("Hello, world. You're at the polls index.")
