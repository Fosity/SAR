# -*- coding: utf-8 -*-  
from django.http.request import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe

from carry.service import carry
from reposity import models


class BasefuncModal(carry.BaseCarryModal):
    def edit_field(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        else:

            edit_url = reverse('{0}:{1}_{2}_change'.format(self.site.namespace, self.app_label, self.model_name),
                               args=(obj.pk,))
            del_url = reverse('{0}:{1}_{2}_delete'.format(self.site.namespace, self.app_label, self.model_name),
                              args=(obj.pk,))
            detail_url = reverse('{0}:{1}_{2}_detail'.format(self.site.namespace, self.app_label, self.model_name),
                                 args=(obj.pk,))

            param_url = ""
            if len(self.request.GET):
                _change = QueryDict(mutable=True)
                _change['_change_filter'] = self.request.GET.urlencode()
                param_url = "?{0}".format(_change.urlencode())

            tpl = "<a href='{0}{3}'>编辑</a> | <a href='{1}{3}'>删除</a> | <a href='{2}{3}'>查看详细</a>".format(edit_url,
                                                                                                         del_url,
                                                                                                         detail_url,
                                                                                                         param_url)
            return mark_safe(tpl)


class AuditLogAdmin(carry.BaseCarryModal):
    list_display = ['session', 'cmd', 'date', BasefuncModal.edit_field]


class SessionLogAdmin(carry.BaseCarryModal):
    list_display = ['id', 'account', 'host_user_bind', 'start_date', 'end_date', BasefuncModal.edit_field]


class TaskLogAdmin(carry.BaseCarryModal):
    list_display = ['id', 'task_id', 'host_user_bind_id', 'result', 'date', BasefuncModal.edit_field]


class IDCAdmin(carry.BaseCarryModal):
    list_display = ['name', BasefuncModal.edit_field]


class TaskAdmin(carry.BaseCarryModal):
    list_display = ['task_type', 'content', 'timeout', 'date', BasefuncModal.edit_field]


class CpuAdmin(carry.BaseCarryModal):
    list_display = ['ct_time', 'cpu_num_info', BasefuncModal.edit_field]


class CpuNameAdmin(carry.BaseCarryModal):
    list_display = ['title', BasefuncModal.edit_field]


class MemoryAdmin(carry.BaseCarryModal):
    list_display = ['me_num', 'Memory_time', BasefuncModal.edit_field]


class AccountAdmin(carry.BaseCarryModal):
    list_display = ['name', BasefuncModal.edit_field]


class HostGroupAdmin(carry.BaseCarryModal):
    list_display = ['name', BasefuncModal.edit_field]


class HostUserAdmin(carry.BaseCarryModal):
    list_display = ['auth_type', 'username', 'password', BasefuncModal.edit_field]


class HostAdmin(carry.BaseCarryModal):
    list_display = ['host_name', 'ip_addr', 'port', 'enabled', BasefuncModal.edit_field]
class TokenAdmin(carry.BaseCarryModal):
    list_display = ['host_user_bind', 'val', 'account', 'expire', 'date',BasefuncModal.edit_field]

carry.site.register(models.Host, HostAdmin)
carry.site.register(models.HostUser, HostUserAdmin)
carry.site.register(models.HostGroup, HostGroupAdmin)
carry.site.register(models.HostUserBind)
carry.site.register(models.Account, AccountAdmin)
carry.site.register(models.IDC, IDCAdmin)
carry.site.register(models.AuditLog, AuditLogAdmin)
carry.site.register(models.SessionLog, SessionLogAdmin)
carry.site.register(models.Task, TaskAdmin)
carry.site.register(models.Cpu, CpuAdmin)
carry.site.register(models.CpuName, CpuNameAdmin)
carry.site.register(models.Memory, MemoryAdmin)
carry.site.register(models.TaskLog, TaskLogAdmin)
carry.site.register(models.Token, TokenAdmin)
