from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^ajax_for_tokens_list', views.ajax_for_tokens_list, name='ajax_for_tokens_list'),
    url(r'^ajax_for_save_tagged_tokens', views.ajax_for_save_tagged_tokens, name='ajax_for_save_tagged_tokens'),
    url(r'^ajax_tag_model_list_get', views.ajax_tag_model_list_get, name='ajax_tag_model_list_get'),
    url(r'^ajax_tag_model_get', views.ajax_tag_model_get, name='ajax_tag_model_get'),
    # url(r'^export_data_do', views.export_data_do, name='export_data_do'),
    url(r'^export_data_do/$', views.export_data_do, name='export_data_do'),

              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)