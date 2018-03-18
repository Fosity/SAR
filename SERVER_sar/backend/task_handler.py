# -*- coding: utf-8 -*-  

import json
import subprocess

from django.conf import settings
from django.db.transaction import atomic

from reposity import models


class Task(object):
    """处理批量任务，包括命令和文件传输"""

    def __init__(self, request):
        self.request = request
        self.errors = []
        self.task_data = None

    def is_valid(self):
        """
        1. 验证命令、主机列表合法
        :return:
        """
        task_data = self.request.POST.get('task_data')
        if task_data:
            self.task_data = json.loads(task_data)
            if self.task_data.get('task_type') == 'cmd':
                if self.task_data.get('cmd') and self.task_data.get('selected_host_ids'):
                    return True
                self.errors.append({'invalid_argument': 'cmd or host_list is empty.'})
            elif self.task_data.get('task_type') == 'file_transfer':
                return True
            else:
                self.errors.append({'invalid_argument': 'task_type is invalid.'})
        self.errors.append({'invalid_data': 'task_data is not exist '})

    def run(self):
        """start task , and return task id """
        task_func = getattr(self, self.task_data.get('task_type'))
        task_obj = task_func()
        return task_obj

    @atomic
    def cmd(self):
        """批量任务"""
        task_obj = models.Task.objects.create(
            task_type=0,
            account=self.request.user.account,
            content=self.task_data.get('cmd'),

        )
        tasklog_objs = []
        host_ids = set(self.task_data.get("selected_host_ids"))
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(task_id=task_obj.id,
                               host_user_bind_id=host_id,
                               status=3
                               )
            )
        models.TaskLog.objects.bulk_create(tasklog_objs, 100)

        cmd_str = "python %s %s" % (settings.MULTI_TASK_SCRIPT, task_obj.id)
        multitask_obj = subprocess.Popen(cmd_str,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)

        return task_obj

    def file_transfer(self):
        """批量文件"""

        task_obj = models.Task.objects.create(
            task_type=1,
            account=self.request.user.account,
            content=json.dumps(self.task_data),
        )
        tasklog_objs = []
        host_ids = set(self.task_data.get("selected_host_ids"))
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(task_id=task_obj.id,
                               host_user_bind_id=host_id,
                               status=3
                               )
            )
        models.TaskLog.objects.bulk_create(tasklog_objs, 100)

        cmd_str = "python %s %s" % (settings.MULTI_TASK_SCRIPT, task_obj.id)
        multitask_obj = subprocess.Popen(cmd_str,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)

        return task_obj
