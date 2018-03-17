# -*- coding: utf-8 -*-  
from django.conf.urls import url

from backend import views

urlpatterns = [
    url(r'^report.html$', views.use_report),
    url(r'^use_ajax/$', views.use_ajax),
    url(r'^use_select/$', views.use_select),
    url(r'^hostlist/$', views.host_list,name="host_list"),
    url(r'^api/hostlist/$', views.get_host_list, name="get_host_list"),
    url(r'^api/token/$', views.get_token, name="get_token"),

    url(r'^multitask/$', views.multitask, name="multitask"),

    url(r'^multitask/cmd/$', views.multi_cmd, name="multi_cmd"),
    url(r'^multitask/result/$', views.multitask_result, name="get_task_result"),
    url(r'^multitask/file_transfer/$', views.multi_file_transfer, name="multi_file_transfer"),
    url(r'^api/task/file_upload/$', views.task_file_upload, name="task_file_upload"),
    url(r'^api/task/file_download/$', views.task_file_download, name="task_file_download"),
]
