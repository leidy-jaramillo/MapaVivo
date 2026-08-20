from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

admin.site.site_header = 'Administración Mapa Vivo'
admin.site.site_title = 'Administración Mapa Vivo'
admin.site.index_title = 'Panel de administración'

urlpatterns = [
    path('', include('portal.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]