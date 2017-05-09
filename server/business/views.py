## TODO Delete Account App - Move to Member App

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render

from core.models import Language

# Create your views here.
def index(request):
  return HttpResponse("Hello, world. You're at the members index.")
