import datetime
import json
import os
import random
import string

from django import conf
from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from backend import task_handler
from reposity import models
from utils.send_file import send_zipfile


# Create your views here.
def use_report(request):
    """cpu memory 显示页"""
    return render(request, 'use_report.html')


@csrf_exempt
def use_ajax(request):
    """cpu,memory ajax 请求数据"""
    idc_id = request.POST.get('IDC')  # idc 对应的nid
    group_id = request.POST.get('Group')
    host_id = request.POST.get('Host')
    now_time = datetime.datetime.now()
    begin_cpu_time = now_time - datetime.timedelta(minutes=settings.CPU_TIME)  # 10分钟之前的时间
    begin_mem_time = now_time - datetime.timedelta(minutes=settings.MEMORY_TIME)  # 10分钟之前的时间
    cpu_list = list(
        models.Cpu.objects.filter(cpu_title_info__host_info_id=host_id, cpu_title_info__host_info__idc_id=idc_id,
                                  cpu_title_info__host_info__hostuserbind__hostgroup=group_id).filter(
            ct_time__gte=begin_cpu_time).
            extra(select={'ct_t': "strftime('%%s',strftime('%%H:%%M:%%S',ct_time))"}).
            values_list('ct_t', 'cpu_num_info'))

    cpu_use_list = list(map(lambda x: [int(x[0]) * 1000, x[1]], cpu_list))
    memory_list = list(models.Memory.objects.filter(host_info_id=host_id, host_info__idc_id=idc_id,
                                                    host_info__hostuserbind__hostgroup=group_id).filter(
        Memory_time__gte=begin_mem_time).
                       extra(select={'memory_t': "strftime('%%s',strftime('%%H:%%M:%%S',memory_time))"}).
                       values_list('memory_t', 'me_num'))
    memory_use_list = list(map(lambda x: [int(x[0]) * 1000, x[1]], memory_list))
    try:
        cpu_avg_num = cpu_use_list[-1][1]
    except Exception as e:
        cpu_avg_num = 0
    try:
        memory_avg_num = memory_use_list[-1][1]
    except Exception as e:
        memory_avg_num = 0
    day_time = now_time.strftime('%Y-%m-%d')
    hour_time = now_time.strftime('%H:%M:%S')
    data = [
        {
            'label': 'CPU-USE',
            'data': cpu_use_list,
            'lines': {
                'show': True
            },
            'color': "rgb(255,50,50)",
        },
        {
            'label': 'Memory-USE',
            'data': memory_use_list,
            'lines': {
                'show': True
            },
            'color': "rgb(50,50,255)",
        }
    ]
    return HttpResponse(json.dumps({'data': data, 'cpu_avg_num': cpu_avg_num, 'memory_avg_num': memory_avg_num,
                                    'day_time': day_time, 'hour_time': hour_time,
                                    'updateInterval': settings.UPDATE_TIME}))


def use_select(request):
    """动态生成下拉框"""
    idc_id = request.POST.get('IDC')  # idc 对应的nid
    group_id = request.POST.get('Group')
    host_id = request.POST.get('Host')
    idc_list = list(
        models.IDC.objects.extra(select={'text': 'reposity_idc.name'}, select_params=['id', ]).distinct().values('id',
                                                                                                                 'text'))
    if idc_id == '00':
        group_list = None
        host_list = None
    else:
        group_list = list(models.HostGroup.objects.filter(host_user_binds__host__idc_id=idc_id). \
                          extra(select={'text': 'reposity_hostgroup.name'}).distinct().values('id', 'text'))
        if group_id == '00':
            host_list = None
        else:
            host_list = list(models.Host.objects.filter(idc_id=idc_id, hostuserbind__hostgroup=group_id). \
                             extra(select={'text': 'reposity_host.host_name'}).distinct().values('id', 'text'))
    response = {
        'IDC': idc_list,
        'Group': group_list,
        'Host': host_list,
    }
    return HttpResponse(json.dumps(response))


def host_list(request):
    """主机列表起始页"""
    account_obj = models.Account.objects.filter(user_id=request.session.get('user_info').get('nid')).first()
    return render(request, 'hostlist.html', {'account_obj': account_obj})


def get_host_list(request):
    """主机页面 ajax请求"""
    gid = request.GET.get('gid')
    account_obj = models.Account.objects.filter(user_id=request.session.get('user_info').get('nid')).first()
    if gid:
        if gid == '-1':  # 未分组
            host_list = account_obj.host_user_binds.all()
        else:
            group_obj = account_obj.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()
        data = json.dumps(
            list(host_list.values('id', 'host__host_name', 'host__idc__name', 'host__ip_addr', 'host__port',
                                  'host_user__username')))
        return HttpResponse(data)


def get_token(request):
    """和网页版shellinabox交互，需要随机生成验证码，并且只有5分钟有效"""
    bind_host_id = request.POST.get('bind_host_id')
    account_obj = models.Account.objects.filter(user_id=request.session.get('user_info').get('nid')).first()
    time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300)  # 5mins ago
    exist_token_objs = models.Token.objects.filter(account=account_obj,
                                                   host_user_bind_id=bind_host_id,
                                                   date__gt=time_obj)

    if exist_token_objs:
        token_data = {'token': exist_token_objs[0].val}
    else:
        token_val = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))

        token_obj = models.Token.objects.create(
            host_user_bind_id=bind_host_id,
            account=account_obj,
            val=token_val
        )
        token_data = {'token': token_val}

    return HttpResponse(json.dumps(token_data))


def multi_cmd(request):
    """多任务处理页"""
    account_obj = models.Account.objects.filter(user_id=request.session.get('user_info').get('nid')).first()
    return render(request, 'multi_cmd.html', {'account_obj': account_obj})


def multitask(request):
    """任务处理"""
    task_obj = task_handler.Task(request)
    if task_obj.is_valid():
        task_obj = task_obj.run()
        return HttpResponse(json.dumps({'task_id': task_obj.id, 'timeout': task_obj.timeout}))
    return HttpResponse(json.dumps(task_obj.errors))


def multitask_result(request):
    """任务处理结果"""
    task_id = request.GET.get('task_id')
    task_obj = models.Task.objects.get(id=task_id)
    results = list(task_obj.tasklog_set.values('id', 'status',
                                               'host_user_bind__host__host_name',
                                               'host_user_bind__host__ip_addr',
                                               'result'
                                               ))

    return HttpResponse(json.dumps(results))


def multi_file_transfer(request):
    random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
    account_obj = models.Account.objects.filter(user_id=request.session.get('user_info').get('nid')).first()
    # return render(request,'multi_file_transfer.html',{'random_str':random_str})
    return render(request, 'multi_file_transfer.html', locals())


@csrf_exempt
def task_file_upload(request):
    """上传文件"""
    random_str = request.GET.get('random_str')
    upload_to = "%s/%s/%s" % (conf.settings.FILE_UPLOADS, request.user.account.id, random_str)
    if not os.path.isdir(upload_to):
        os.makedirs(upload_to, exist_ok=True)

    file_obj = request.FILES.get('file')
    f = open("%s/%s" % (upload_to, file_obj.name), 'wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    print(file_obj)
    return HttpResponse(json.dumps({'status': 0}))


def task_file_download(request):
    """下载文件"""
    task_id = request.GET.get('task_id')
    print(task_id)
    task_file_path = "%s/%s" % (conf.settings.FILE_DOWNLOADS, task_id)
    wrapper, zip_file_name = send_zipfile(request, task_id, task_file_path)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % zip_file_name
    response['Content-Length'] = os.path.getsize(zip_file_name)
    return response
