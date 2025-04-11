from django.contrib import admin
from django.urls import path, include

from Admin_app.views import register_user

urlpatterns = [
    path('Admin/', admin.site.urls),
    path('', include('Admin_app.urls')),
    path('register/', register_user, name='register'),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
