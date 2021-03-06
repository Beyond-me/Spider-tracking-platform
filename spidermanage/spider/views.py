#coding=utf-8

from django.shortcuts import render
from models import Spider, DatabaseType, Message
import time
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Process
import subprocess
import os
import sys
import redis
import syncSpider
import spiderDataFile
from django.core import paginator
from django.http import StreamingHttpResponse

# 爬虫模块的源路径
SpiderBaseDir = os.path.abspath('.') + '/spider/spidermodule/'
reload(sys)
sys.setdefaultencoding('utf-8')

# 爬虫监控的首页
@syncSpider.sync
def spiderstatus(request):
    all_spider = Spider.objects.all().order_by('-id')
    # 计算所有的－请求量／下载量／储存量
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

    all_me = Message.objects.all().order_by('-id')[:5]

    # 传递上下文
    context = {
        'urlmark': 'spiderstatus',
        'all_spider':all_spider,
        'requests_total': requests_total,
        'download_total': download_total,
        'info_total': info_total,
        'spider_num': spider_num,
        'run_time': run_time,
        'all_me': all_me,
    }
    return render(request, 'spider/spiderstatus.html', context)


# 查看所有任务
@syncSpider.sync
def checktask(request):

    # 后续加上从爬虫redis数据库更新数据到mysql

    all_spider = Spider.objects.all().order_by('id')
    context = {
        'urlmark':'checktask',
        'all_spider':all_spider,
    }
    return render(request, 'spider/checkspidertask.html', context)


# 执行任务－选择爬虫和设置参数
def runtask(request):
    all_spider = Spider.objects.all().order_by('id')

    first_spider_obj = all_spider[0]
    content = first_spider_obj.spider_content
    mark = first_spider_obj.spider_mark
    func_name = first_spider_obj.spider_runfunction

    redisclient = redis.Redis(host='127.0.0.1', port=6379, db=1)
    info = redisclient.get(func_name + ':runing')

    if info == None:
        first_spider_obj.spider_runing = False
    elif info == b'False':
        first_spider_obj.spider_runing = False
    else:
        first_spider_obj.spider_runing = True

    first_spider_obj.save()

    context = {
        'urlmark':'runtask',
        'all_spider':all_spider,
        'content':content,
        'mark':mark,
        'first_item_runing':first_spider_obj.spider_runing,
    }
    return render(request, 'spider/runspidertask.html', context)


# 启动爬虫进程－使用新进程启动爬虫　来自ajax请求
def startspiderbyid(request):
    # 设置模块查找目录
    sys.path.append(SpiderBaseDir)
    # 保存get请求的值
    spider_id =request.GET['spider_id']
    spider_argv = request.GET['run_argvs']

    # 取出目标爬虫中的模块名称
    result = Spider.objects.filter(id=spider_id)
    spider_obj = result[0]
    func_name = spider_obj.spider_runfunction

    # 如果模块名称没有定义就不会执行新的任务，否则使用新的进程运行爬虫程序
    if func_name != 'no info':
        # 使用新进程开始任务
        mymodule = __import__(func_name)
        if spider_argv != '':
            spider_argv = tuple(spider_argv.split(' '))
            p = Process(target=mymodule.main,args=spider_argv)
            markcontent = '爬虫启动成功, 参数为：' + '<b>' +request.GET['run_argvs'] + '</b>'
        else:
            p = Process(target=mymodule.main)
            markcontent = '爬虫启动成功, 无自定义参数：'
        p.start()

        # 创建通知对象
        me_obj = Message()
        mytime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        me_obj.action_time = mytime
        me_obj.content = markcontent
        me_obj.user = 'admin'
        me_obj.spider = spider_obj
        me_obj.save()

        # 改变数据库中爬虫运行状态
        spider_obj.spider_runing = True
        spider_obj.save()

        print('主进程结束标志1：此视图结束，爬虫程序自己运行，但是运行状态会放在redis和log中，使用视图调用并传递到ajax和mysql')
        return JsonResponse({'data': '启动爬虫成功，请到实时监控界面查看！','doing':1})
    else:
        # 改变数据库中爬虫运行状态
        spider_obj.spider_runing = False
        spider_obj.save()

        # 创建通知对象
        me_obj = Message()
        mytime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        me_obj.action_time = mytime
        me_obj.content = '启动爬虫失败：没有足够的权限'
        me_obj.user = 'admin'
        me_obj.spider = spider_obj
        me_obj.save()

        print('主进程结束标志2：此视图结束，爬虫程序自己运行，但是运行状态会放在redis和log中，使用视图调用并传递到ajax和mysql')
        return JsonResponse({'data': '权限不足，无法操作！','doing':0})


# 停止采集按钮
def stopspiderbyid(request):
    spider_id = request.GET['spider_id']
    result = Spider.objects.filter(id=spider_id)
    spider_obj = result[0]
    func_name = spider_obj.spider_runfunction

    redisclient = redis.Redis(host='127.0.0.1', port=6379, db=1)
    redisclient.getset(func_name + ':runing', 'False')

    spider_obj.spider_runing = False
    spider_obj.save()

    # 创建通知对象
    me_obj = Message()
    mytime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    me_obj.action_time = mytime
    me_obj.content = '手动停止爬虫'
    me_obj.user = 'admin'
    me_obj.spider = spider_obj
    me_obj.save()

    print('修改redis和mysql状态，爬虫退出')
    return JsonResponse({'data': '停止采集成功！'})


# 执行任务-选择-下拉框变化时候动态显示不同选项的值，下拉框操作一次才会请求一次
def selectspiderbyid(request):
    # 保存get请求的值，主要是根据id获取数据库中爬虫模型的信息
    spiserid = request.GET['spider_id']
    result = Spider.objects.filter(id=spiserid)
    # 获取爬虫说明和内容
    spider_obj = result[0]
    content = spider_obj.spider_content
    mark = spider_obj.spider_mark
    func_name = spider_obj.spider_runfunction

    # 读取redis记录的状态，然后传递给数据库
    redisclient = redis.Redis(host='127.0.0.1', port=6379, db=1)
    info = redisclient.get(func_name + ':runing')

    print func_name,info

    if info == None:
        spider_obj.spider_runing = False
    elif info == b'False':
        spider_obj.spider_runing = False
    else:
        spider_obj.spider_runing = True
    spider_obj.save()

    # 拼接爬虫log文件名称,读取对应log文件数据，文件不存在就返回空值
    logfilename = SpiderBaseDir + func_name + '/' + func_name + '.log'
    try:
        with open(logfilename, 'r') as f:
            log_content = f.read()
    except Exception as e:
        print(e,logfilename)
        log_content = ''
    # 生成标签内容
    tags = ''
    for each in log_content.split('\n'):
        li_tag = '<li>' + each + '</li>'
        tags += li_tag

    # 把需要动态显示的内容传递给前端
    context = {
        'content':content,
        'mark':mark,
        'tags':tags,
        'runing':spider_obj.spider_runing,
    }

    # print 'spider_obj.spider_runing',func_name,spider_obj.spider_runing
    return JsonResponse({'data': context})


# 执行任务界面　循环检查这个任务是否完成
def checkrunstatus(request):

    spiserid = request.GET['spider_id']
    result = Spider.objects.filter(id=spiserid)

    spider_obj = result[0]
    flag = spider_obj.spider_runing

    if flag == True:
        return JsonResponse({'data':True})
    else:
        return JsonResponse({'data':False})


# 请求log-循环请求log信息，前端接收到'done'的时候，会结束循环
def getspiderlogbyid(request):
    # 根据ID获取爬虫任务名称
    spider_id = request.GET['spider_id']
    result = Spider.objects.filter(id=spider_id)
    spider_obj = result[0]
    func_name = spider_obj.spider_runfunction

    # 先判断爬虫的对应模块是否是默认值no info，否则就返回'done'给前端，前端就会停止循环发送请求
    tags = ''
    if func_name == 'no info':
        return JsonResponse({'data': 'done', 'content': tags})
    else:
        # 拼接log文件名称，并且试图读取其中的信息，如果没有这个文件就会返回空值
        logfilename = SpiderBaseDir + func_name + '/' + func_name +'.log'
        try:
            with open(logfilename, 'r') as f:
                content = f.read()
                print '读取log文件成功'
        except Exception as e:
            print '读取log文件失败',e,logfilename
            content = ''
        # 生成html标签内容
        tags = ''
        for each in content.split('\n'):
            li_tag = '<li>' + each + '</li>'
            tags += li_tag

        # 根据名称，在redis查找任务信息中的runing，如果是False前端就会结束循环
        redisclient = redis.Redis(host='127.0.0.1', port=6379, db=1)
        info = redisclient.get(func_name+':runing')

        # 根据redis的状态判断是否要作为最后一次发送数据
        if info == b'False':
            # 改变数据库中爬虫运行状态
            try:
                spider_obj.spider_runing = False
                spider_obj.save()
            except Exception as e:
                print '改变mysql中爬虫状态失败',e
            print 'log信息传输结束'

            # 创建通知对象
            me_obj = Message()
            mytime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            me_obj.action_time = mytime
            me_obj.content = '爬虫运行结束并退出'
            me_obj.user = 'admin'
            me_obj.spider = spider_obj
            me_obj.save()

            return JsonResponse({'data': 'done', 'content': tags})
        else:
            return JsonResponse({'data': 'continue', 'content': tags})


# 根据id访问爬虫监控页面-页面会自动启动ajax请求，不断更新log
def intospider(request, spider_id):
    # 获取爬虫数据对象
    result = Spider.objects.filter(id=spider_id)
    spider_obj = result[0]

    # 传递上下文
    context = {
        'spider_obj': spider_obj,
        'urlmark': 'intospider',
    }
    return render(request, 'spider/intospider.html', context)


# get请求提交给爬虫监控页面-页面会自动启动ajax请求，不断更新log
def intospider_form(request):
    # 获取get参数和爬虫数据对象
    spider_id = request.GET['spiderchoose']
    spider_argv = request.GET['spiderargv']
    result = Spider.objects.filter(id=spider_id)
    spider_obj = result[0]

    # 传递上下文
    context = {
        'spider_obj': spider_obj,
        'urlmark': 'intospider',
    }
    return render(request, 'spider/intospider.html', context)





def dataoprate(request):

    items = spiderDataFile.filemanage()

    context = {
        'urlmark': 'dataoprate',
        'items': items,
    }

    return render(request, 'spider/dataoprate.html',context)

def dataopinfo(request):

    file_name = request.GET['FN']
    dir_name = request.GET['DIR']

    spider_obj = Spider.objects.filter(spider_runfunction=dir_name)[0]

    me_obj = Message()
    mytime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    me_obj.action_time = mytime
    me_obj.content = '下载文件：%s'%file_name
    me_obj.user = 'admin'
    me_obj.spider = spider_obj
    me_obj.save()

    return JsonResponse({'data':'1'})


def spidersetting(request):

    context = {
        'urlmark': 'spidersetting',
    }
    return render(request, 'building.html',context)


def spiderhistoty(request, index):
    all_me = Message.objects.all().order_by('-id')
    pag = paginator.Paginator(all_me, 10)
    if index == '':
        index = 1
    page = pag.page(index)
    context = {
        'page': page,
        'viewIndex': int(index),
        'urlmark': 'spiderhistoty',
    }

    return render(request, 'spider/infohistory.html', context)



def data_file_download(request, dir_name, file_name):
    # do something...
    the_file_name = os.path.join(SpiderBaseDir + dir_name, file_name)

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

    return response











