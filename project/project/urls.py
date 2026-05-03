from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("escola/", include("escola.urls")),
    path("", include("portfolioPWEB.urls")),
    path("portfolio/", include("portfolioPWEB.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("accounts/", include("accounts.urls")),   # ← adiciona
    path("artigos/", include("artigos.urls")), 
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)