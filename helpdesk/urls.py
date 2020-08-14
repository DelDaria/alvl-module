from django.contrib import admin
from django.urls import path, include
from users.views import index
# from users.views import ObtainTokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index_page'),
    path('users/', include('users.urls')),
    path('issues/', include('issues.urls')),
    path('api/', include('api.urls')),

]


