from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token

from .views import custom_obtain_jwt_token, custom_verify_jwt_token


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


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.



urlpatterns = [
    url(r'^api/member/', include('server.member.urls')),
    url(r'^api/business/', include('server.business.urls')),
    url(r'^api/notification/', include('server.notification.urls')),
    url(r'^api/media/', include('server.media.urls')),
    url(r'^api/review/', include('server.review.urls')),
    url(r'^api/', include('server.account.urls')),

    url(r'^purple/admin/', admin.site.urls),
    url(r'^business/', include('client.client_business.urls')),
    url(r'^member/', include('client.client_member.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', custom_obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', custom_verify_jwt_token),

#    url(r'^about/', include('client.client_member.urls')),
#    url(r'^contact/', include('client.client_member.urls')),

#    url(r'^', include('client.client_home.urls')),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static('/', document_root='angularjs/src')
