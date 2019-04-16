from django.contrib import admin
from django.urls import path, include

from contacts.views import goto


urlpatterns = [
    path('', goto),
    path('admin/', admin.site.urls),
    path('contact-list/', include('contacts.urls')),
]
