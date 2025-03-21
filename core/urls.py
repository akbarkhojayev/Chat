from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from main.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Chat API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += [
   path('token/', token_obtain_pair),
   path('token/refresh/', token_refresh),
]
urlpatterns += [
   path('register/', RegisterView.as_view(), name='register'),
   path('users/', UserListView.as_view(), name='users'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('api/chats/create/', PrivateChatCreateView.as_view(), name='create-chat'),
   path('api/chats/<int:chat_id>/messages/', MessageListCreateView.as_view(), name='chat-messages'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)