from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . views import GetUserProfileView, UpdateUserProfileView

urlpatterns = [
    path('user-profile/', GetUserProfileView.as_view()),
    path('update-profile/', UpdateUserProfileView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
                document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
                document_root=settings.MEDIA_ROOT)