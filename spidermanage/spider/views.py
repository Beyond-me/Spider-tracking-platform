#coding=utf-8

from django.shortcuts import render
from models import Spider, DatabaseType
import time
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Process
import subprocess
import os
import sys
import redis


def spiderstatus(request):

    all_spider = Spider.objects.all().order_by('-id')

    # 计算所有的　请求量／下载量／储存量

    requests_total = 0
    download_total = 0
    info_total = 0
    for spider_obj in all_spider:
        requests_total += spider_obj.spider_request_count
        download_total += spider_obj.spider_download_count
        info_total += spider_obj.spider_info_count

    spider_num = len(all_spider)

    run_time = int(time.time()) - 1506706534
    run_time = run_time//86400

    context = {
        'urlmark': 'spiderstatus',
        'all_spider':all_spider,
        'requests_total': requests_total,
        'download_total': download_total,
        'info_total': info_total,
        'spider_num': spider_num,
        'run_time': run_time,

    }
    return render(request, 'spider/spiderstatus.html', context)



def checktask(request):
    all_spider = Spider.objects.all().order_by('id')

    context = {
        'urlmark':'checktask',
        'all_spider':all_spider,
    }

    print(context['urlmark'])

    return render(request, 'spider/checkspidertask.html', context)


def runtask(request):

    all_spider = Spider.objects.all().order_by('id')

    content = all_spider[0].spider_content
    mark = all_spider[0].spider_mark

    context = {
        'urlmark':'runtask',
        'all_spider':all_spider,
        'content':content,
        'mark':mark,
    }

    return render(request, 'spider/runspidertask.html', context)


def startspiderbyid(request):

    sys.path.append("/home/python/Desktop/mysite/spidermanage/spider/spidermodule")

    spiserid =request.GET['title']
    spider_argv =request.GET['argvs']

    result = Spider.objects.filter(id=spiserid)

    if len(result) == 1:
        func_name = result[0].spider_runfunction

        mymodule = __import__(func_name)
        p = Process(target=mymodule.main)
        p.start()

        print('主进程结束标志')
        return JsonResponse({'data': '启动爬虫成功！'})

    else:
        print('主进程结束标志')
        return JsonResponse({'data': '无法启动此爬虫，权限不足！'})



def selectspiderbyid(request):

    spiserid = request.GET['title']

    result = Spider.objects.filter(id=spiserid)
    content = result[0].spider_content
    mark = result[0].spider_mark
    context = {
        'content':content,
        'mark':mark,
    }

    return JsonResponse({'data': context})


def getspiderlogbyid(request):

    redisclient = redis.Redis(host='127.0.0.1', port=6379)
    info = redisclient.lpop('university_list')

    if info == None:
        return JsonResponse({'data': 'Null'})
    if info == b'done':
        return JsonResponse({'data': 'done'})

    return JsonResponse({'data': info})















def dataoprate(request):
    pass


def spidersetting(request):
    pass


def spiderhistoty(request):
    pass




















