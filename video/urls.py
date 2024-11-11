from django.urls import path
from . import views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="xxx",
      default_version='v1',
      description="API documentation for your Django project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourdomain.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
app_name = 'video'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('detail/<int:pk>/', views.VideoDetailView.as_view(), name='detail'),
    path('like/', views.like, name='like'),
    path('collect/', views.collect, name='collect'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]