from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from contacts.views import goto


urlpatterns = [
    path('', goto),
    path('admin/', admin.site.urls),
    path('contact-list/', include('contacts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
