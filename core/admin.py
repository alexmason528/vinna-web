from django.contrib import admin

from core.models import Language
from core.models import Country
from core.models import State

# Register your models here.
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(State)
