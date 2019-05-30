"""talkhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from blogapp import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.main_page, name='main_page'),
    url(r'^chat/', include(('blogapp.urls', 'blogapp'), namespace='blogapp')),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit-profile/$', views.edit_profile, name='edit_profile'),
    url(r'^like/$', views.like_post, name='like_post'),
    url(r'^comment-delete/(?P<id>\d+)/(?P<comid>\d+)/$', views.comment_delete, name='comment_delete'),
    url(r'^profile/(?P<id>\d+)/$', views.profile, name='profile'),
    url(r'^profile/delete/(?P<id>\d+)/$', views.user_delete, name='user_delete'),
    url(r'^lending/$', views.lending, name='lending'),
    url(r'^check/$', views.check, name='check'),


    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),


    # url(r'^password-reset/$', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    # url(r'^password-reset/done/$', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    # url(r'^password-reset/confirm/(?P<uid64>[\w-]+)/(?P<token>[\w-]+)/$', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    # url(r'^password-reset/complete/$', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
