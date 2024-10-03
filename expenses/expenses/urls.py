"""
URL configuration for py_reimburse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from expenses import views, settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('converter/', include('converter.urls', namespace='converter')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "django.views.defaults.bad_request"
handler404 = "django.views.defaults.page_not_found"
handler403 = "django.views.defaults.permission_denied"
handler500 = "django.views.defaults.server_error"
