"""project_Kahoot_zeon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

# Standard libraries
from django.contrib import admin
from django.urls import path, include

# Libraries for SWAGGER
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Libraries for Images
from django.conf import settings
from django.conf.urls.static import static

#Libraries from Serializers


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  # v1 will notify one way of writing a view (Function-Based View) for a serializer
                  path('', include('quiz.urls')),
                  # path('quiz/', include('quiz.urls', namespace='quiz'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
