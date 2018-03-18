import datetime
import json

from django.db import transaction
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from reposity import models
from utils.decryption import decryption, decrypt

api_key_record = {}


@csrf_exempt
def asset(request):
    """
    和client端接口：
    验证，获取数据解密
    :param request:
    :return:
    """
    flag = decryption(request, api_key_record)
    if not flag:
        return HttpResponse('Wrong password!')
    if request.method == "GET":
        return HttpResponse('..GET..')
    elif request.method == "POST":
        server_info = json.loads(decrypt(request.body))
        hostname = server_info.get('hostname')
        """
        {'cpu_use': {'status': True, 'data': {'all': 97.655, '0': 97.32, '1': 98.155}}, 
        'memory_use': {'status': True, 'data': {'memory_avg': '66.40'}}, 'hostname': 'cw.com'}"""

        hostname_obj = models.Host.objects.filter(host_name=hostname).first()
        for k, v in server_info.get('cpu_use').get('data').items():
            cpu_title = hostname_obj.cpuname_set.filter(title=k)
            cpu_title = cpu_title.first()
            if not cpu_title:
                cpu_title = hostname_obj.cpuname_set.create(title=k)
            models.Cpu.objects.create(cpu_title_info=cpu_title, cpu_num_info=v)
        models.Memory.objects.create(me_num=server_info.get('memory_use').get('data').get('memory_avg'),
                                     host_info=hostname_obj)

        now_time = datetime.datetime.now()
        if int(now_time.timestamp() % 1000) == 3:
            end_time = now_time - datetime.timedelta(minutes=setting.DELETEDBTIME)
            with transaction.atomic():
                models.Cpu.objects.filter(ct_time__lte=end_time).delete()
                models.Memory.objects.filter(Memory_time__lte=end_time).delete()
        return HttpResponse('.')
