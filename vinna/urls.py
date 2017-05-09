from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

"""vinna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [

    url(r'^api/account/', include('server.account.urls')),
    url(r'^api/member/', include('server.member.urls')),
    url(r'^api/business/', include('server.business.urls')),

    url(r'^purple/admin/', admin.site.urls),

    url(r'^business/', include('client.client_business.urls')),
    url(r'^member/', include('client.client_member.urls')),


#    url(r'^about/', include('client.client_member.urls')),
#    url(r'^contact/', include('client.client_member.urls')),

#    url(r'^', include('client.client_home.urls')),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static('/', document_root='angularjs/src')
