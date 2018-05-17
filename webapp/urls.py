from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^homes/$', views.dashboard, name='dashboard'),
    url(r'^posture/$', views.alerts, name='alerts'),
    url(r'^available/$', views.available, name='available'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': 'login'}, name='logout'),
    url(r'^config/filter/$', views.configure_filter, name="config_filter"),
    url(r'^config/filter/(?P<instance>[^/]+)/$', views.configure_target_filter, name="config_target_filter"),
    url(r'^config/sensor/(?P<instance>[^/]+)/$', views.configure_target_sensor, name="config_target_sensor"),
    url(r'^config/sensor/$', views.configure_sensor, name="config_sensor"),
    url(r'^config/manage/$', views.manage_instances, name="manage_instances"),
    url(r'^config/admin/$', views.admin_controls, name="admin_controls"),
    url(r'^tools/dashboard/$', views.monitor_overview, name="tools"),
    url(r'^tools/dashboard/visualise/$', views.monitor_visualise, name="monitor_visualise"),
    url(r'^tools/dashboard/analysis/$', views.monitor_analysis, name="monitor_analysis"),
    url(r'^tools/dashboard/overview/$', views.monitor_overview, name="monitor_overview"),
    url(r'^holding/', views.holding, name='holding'),
    url(r'^testbed/', views.testbed, name='testbed')
]

