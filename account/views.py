from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render

from core.models import Language

# Create your views here.
def index(request):
  return HttpResponse("Hello, world. You're at the account index.")

def register(request):
  context = { 'languages' : Language.objects.all().order_by('text') }
  return render(request, 'account/register.html', context)
