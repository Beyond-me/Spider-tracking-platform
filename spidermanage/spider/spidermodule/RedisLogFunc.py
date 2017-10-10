# coding=utf-8
import redis
import os
import time
import json
import csv


# spider_file_name = 'BaiduNwes'
# 创建这个类的时候：
# 1. 会新建log文件
# 2. 检查redis数据库中是否有初始数据，如果没有就新建，有就直接取出
# 3. 创建类需要传入的是爬虫的名字，其余的参数都会根据爬虫的名字来创建
class RedisLog(object):
    def __init__(self, spider_file_name, form):
        super(RedisLog, self).__init__()

        self.SPIDER_FILE_NAME = spider_file_name
        self.form = form
        self.host = '127.0.0.1'

        mytime = str(time.strftime("%Y%m%d_%H%M%S", time.gmtime()))

        # 被调用时的绝对路径是调用程序的路径，这里需要定位到一个已知规定的路径
        # self.BASE_DIR = os.path.abspath('.')   # 测试路径
        # self.FILE_DIR = self.BASE_DIR + '\\' + self.SPIDER_FILE_NAME  # 测试路径

        self.BASE_DIR = os.path.abspath('.') + '/spider/spidermodule/'   # 生产路径
        self.FILE_DIR = self.BASE_DIR + self.SPIDER_FILE_NAME  # 生产路径

        if not os.path.exists(self.FILE_DIR):
            os.mkdir(self.FILE_DIR)

        self.LOG_FILE_NAME = os.path.join(self.BASE_DIR, self.SPIDER_FILE_NAME, self.SPIDER_FILE_NAME + '.log')
        self.DATA_FILE_NAME = os.path.join(self.BASE_DIR, self.SPIDER_FILE_NAME,
                                           self.SPIDER_FILE_NAME + mytime + '.' + self.form)

        # 初始化log和数据文件,创建文件
        with open(self.LOG_FILE_NAME, 'w') as f:
            pass
        with open(self.DATA_FILE_NAME, 'w') as f:
            pass
        self.CSV_FIRST = True

        # redis状态码设置为True
        redisclient = redis.Redis(host=self.host, port=6379, db=1)
        redisclient.set(self.SPIDER_FILE_NAME + ':runing', 'True')

        if redisclient.get(self.SPIDER_FILE_NAME + ':requestCount') == None:
            redisclient.set(self.SPIDER_FILE_NAME + ':requestCount', 0)
            self.request_count = 0
        else:
            request_count = redisclient.get(self.SPIDER_FILE_NAME + ':requestCount')
            self.request_count = int(request_count)

        if redisclient.get(self.SPIDER_FILE_NAME + ':downloadCount') == None:
            redisclient.set(self.SPIDER_FILE_NAME + ':downloadCount', 0)
            self.download_count = 0
        else:
            sdownload_count = redisclient.get(self.SPIDER_FILE_NAME + ':downloadCount')
            self.download_count = int(sdownload_count)

        if redisclient.get(self.SPIDER_FILE_NAME + ':infoCount') == None:
            redisclient.set(self.SPIDER_FILE_NAME + ':infoCount', 0)
            self.info_count = 0
        else:
            info_count = redisclient.get(self.SPIDER_FILE_NAME + ':infoCount')
            self.info_count = int(info_count)

        if redisclient.get(self.SPIDER_FILE_NAME + ':errorCount') == None:
            redisclient.set(self.SPIDER_FILE_NAME + ':errorCount', 0)
            self.error_count = 0
        else:
            error_count = redisclient.get(self.SPIDER_FILE_NAME + ':errorCount')
            self.error_count = int(error_count)

    # mode = R-request | D-download | I-info | E-error
    # 作用：打印信息，写入log，根据mode变更redis数据
    def loginfo(self, info, mode='N', count=1):

        info = 'INFO: ' + info

        if mode == 'R':
            self.request_count += count
        elif mode == 'D':
            self.download_count += count
        elif mode == 'E':
            info = 'ERROR: ' + info
            self.error_count += count
        elif mode == 'I':
            self.info_count += count

        print(info)
        with open(self.LOG_FILE_NAME, 'a') as f:
            logtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            f.write(logtime + ' ' + info + '\n')

    # 检查请求是否完成过（针对整站的爬取）
    # 如果是重复的就抛出UrlExistException异常，不重复就加入指纹库并请求
    def insert_req(self, req):
        redisclient = redis.Redis(host=self.host, port=6379, db=1)
        rname = self.SPIDER_FILE_NAME + ':doneUrl'
        ext = redisclient.sismember(rname, req)
        if ext == True:
            raise UrlExistException()
        else:
            redisclient.sadd(rname, req)

    # 检查请求是否完成过（针对整站的爬取）
    # 如果是重复的就返回True，不重复就加入指纹库并请求
    def url_done_check(self, req):
        redisclient = redis.Redis(host=self.host, port=6379, db=1)
        rname = self.SPIDER_FILE_NAME + ':doneUrl'
        ext = redisclient.sismember(rname, req)
        if ext == True:
            self.loginfo('重复的url请求，跳过 %s' % req)
            return True
        else:
            redisclient.sadd(rname, req)
            self.loginfo('url加入指纹库 %s' % req)
            return False

    # 提交最新数据到redis
    def commit_redis(self):
        redisclient = redis.Redis(host=self.host, port=6379, db=1)
        mset_dic = {
            self.SPIDER_FILE_NAME + ":requestCount": self.request_count,
            self.SPIDER_FILE_NAME + ":downloadCount": self.download_count,
            self.SPIDER_FILE_NAME + ":infoCount": self.info_count,
            self.SPIDER_FILE_NAME + ":errorCount": self.error_count,
        }
        redisclient.mset(mset_dic)

    # 运行状态变为False
    def run_false(self):
        redisclient = redis.Redis(host=self.host, port=6379, db=1)
        redisclient.set(self.SPIDER_FILE_NAME + ':runing', 'False')

    # 运行状态变为True
    def run_true(self):
        redisclient = redis.Redis(host=self.host, port=6379, db=1)
        redisclient.set(self.SPIDER_FILE_NAME + ':runing', 'True')

    # 检查运行状态
    def check_status(self):
        redisclient = redis.Redis(host=self.host, port=6379, db=1)
        info = redisclient.get(self.SPIDER_FILE_NAME + ':runing')
        if info == b'False':
            return False
        else:
            return True

    # 传入一条数据（即接收一个字典），写入csv
    def write_csv(self, item):
        with open(self.DATA_FILE_NAME, 'a') as f:
            writer = csv.writer(f)
            if self.CSV_FIRST == True:
                writer.writerow(item.keys())
                self.loginfo('写入title数据成功')
                self.CSV_FIRST = False
            writer.writerow(item.values())
            self.loginfo('写入一条数据成功', 'I')

    # 传入一条数据（即接收一个字典），写入json
    def write_json(self, item):
        data = json.dumps(item, ensure_ascill=False) + ','
        with open(self.DATA_FILE_NAME, 'a') as f:
            f.write(data)


class UrlExistException(Exception):
    def __init__(self, err='此url已经访问过'):
        Exception.__init__(self, err)