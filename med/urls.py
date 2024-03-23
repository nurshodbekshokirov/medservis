
from django.contrib import admin
from django.urls import path, include
from asosiy.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register("mijozlar",MIjozMODELVIEW)
schema_view = get_schema_view(
   openapi.Info(
      title="MED API",
      default_version='v1',
      description="O'quv maqsadlarida foydalanish uchun MED API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact("Nurshodbek Shokirov,<nurshodbekshokirov@gmail.com>"),

   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0)),
    path("register/", RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutApiview.as_view()),
    path("", include(router.urls)),
    path('api/token/ber/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
