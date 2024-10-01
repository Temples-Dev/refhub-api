# urls.py

from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="REFHUB Project API",
      default_version='v1',
      description="API documentation for REFHUB Project",
    
      contact=openapi.Contact(email="euggene@refhub.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


