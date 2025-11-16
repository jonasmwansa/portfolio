"""
portfolioproject/urls.py

URL configuration for portfolioproject project.

"""
from django.contrib import admin
from django.urls import path, include

# Imports for serving static/media files in development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    # Include the portfolio application's URLs
    path('', include('portfolio.urls')),
]

# -----------------------------------------------------------------
# DEVELOPMENT SERVER STATIC/MEDIA FILE SERVING
# ONLY runs if DEBUG=True in settings.
# -----------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)