"""EventMgtSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path,include
from Users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Users/password_reset_complete.html'), name='password_reset_complete'),      
    path('profile/', user_views.profile,name= 'profile'),
    path('create_event/', user_views.create_event,name= 'create_event'),
    path('view_event/', user_views.view_event,name= 'view_event'),
    path('update_event/<str:pk>/', user_views.update_event, name="update_event"),
    path('delete_event/<str:pk>/', user_views.delete_event, name="delete_event"),
    path('create_guests_list/', user_views.create_guests_list,name= 'create_guests_list'),
    path('view_guests_list/', user_views.view_guests_list,name= 'view_guests_list'),
    path('update_guests_list/<str:pk>/', user_views.update_guests_list, name="update_guests_list"),
    path('delete_guests_list/<str:pk>/', user_views.delete_guests_list, name="delete_guests_list"),
    path('login/', auth_views.LoginView.as_view(template_name = 'Users/user_login.html'),name= 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'Users/logout.html'),name= 'logout'),
    path('print_events/', user_views.generate_pdf_events,name ='generate_pdf_events'),
    path('print_guests/', user_views.generate_pdf_guests,name ='generate_pdf_guests'),
    path('send_mail/<int:id>/', user_views.sendmail,name ='send_mail'),
    path('',include('Events.urls'))
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

