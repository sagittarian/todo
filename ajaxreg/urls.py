from django.conf.urls import include, patterns, url

from ajaxreg import views

urlpatterns = patterns('',
    url(r'^register/$', views.login_view,
       {'create_user': True}, name='ajaxreg_register'),
    url(r'^login/$', views.login_view,
       {'create_user': False}, name='ajaxreg_login'),
    url(r'^logout/$', views.logout_view, name='ajaxreg_logout'),
    url(r'^password/change/$', views.password_change,
       name='ajaxreg_password_change'),
    url(r'^password/reset/$', views.password_reset,
       name='ajaxreg_password_reset'),
    url(r'^', views.info, name='ajaxreg_info')
)
