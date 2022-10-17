from django.conf import settings
from django.conf.urls.static import static
from . views import SignUpView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView, DeleteAccountView
from django.urls import path

urlpatterns = [
    path('register/', SignUpView.as_view()),
    path('csrf_cookie/', GetCSRFToken.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('status/', CheckAuthenticatedView.as_view()),
    path('delete/', DeleteAccountView.as_view()),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
                document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
                document_root=settings.MEDIA_ROOT)