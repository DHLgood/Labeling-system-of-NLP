"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^tagging/', include('tagging.urls')),

    url(r'^destribution/$', views.destribution, name='destribution'),
    url(r'^superlogin/$', views.super_login, name='superlogin'),
    url(r'^SuperUserCheck/$', views.SuperUserCheck, name='SuperUserCheck'),
    url(r'^ajax_for_tokens_list', views.ajax_for_tokens_list, name='ajax_for_tokens_list'),
    url(r'^ajax_for_save_tagged_tokens', views.ajax_for_save_tagged_tokens, name='ajax_for_save_tagged_tokens'),
    url(r'^ajax_tag_model_list_get', views.ajax_tag_model_list_get, name='ajax_tag_model_list_get'),
    url(r'^ajax_tag_model_get', views.ajax_tag_model_get, name='ajax_tag_model_get'),
    url(r'^back_check', views.back_check, name='back_check'),
    url(r'^check_result', views.check_result, name='check_result'),
    url(r'^seen_result_html/', views.seen_result_html, name='seen_result_html'),
    url(r'^passcheck', views.passcheck, name='passcheck'),
    url(r'^no_pass', views.no_pass, name='no_pass'),

    url(r'^all_data_source', views.all_data_source, name='all_data_source'),
    url(r'^export_data_from_database/$', views.export_data_from_database, name='export_data_from_database'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
