# coding=utf-8
'''
    获取下面网站的各个大学的名称，并储存到json文件中.
    http://gkcx.eol.cn/soudaxue/queryschool.html
'''

import requests
import re
import sys
import json
import redis
import time
import os


def main(test1, test2):
    # 设置默认编码
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # 初始化
    SPIDER_FILE_NAME = os.path.basename(__file__).replace('.py', '')
    REDIS_RUN_RECORD = SPIDER_FILE_NAME+':runing'
    BASE_DIR = '/home/python/Desktop/mysite/django-blog-spider/spidermanage/spider/spidermodule/'
    LOG_FILE_NAME = BASE_DIR + SPIDER_FILE_NAME + '.log'
    # 创建log文件
    with open(LOG_FILE_NAME, 'w+') as f:
        pass

    # 下载器
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)"}
    url = 'http://data.api.gkcx.eol.cn/soudaxue/queryschool.html'  # json
    page = 1
    school_list = []
    while True:
        params = {"messtype": "jsonp","callback": "jQuery18305451626836174455_1505063607887","province": "","schooltype": "普通本科","page": str(page),"size": "30","keyWord1": "","schoolprop": "","schoolflag": "","schoolsort": "","schoolid": "","_": "1505063608095",}

        try:
            html = requests.get(url, params=params, headers=headers).text
        except Exception as e:
            html = ''
            info = ' catching....%d' % page
            print(info)
            with open(LOG_FILE_NAME, 'a+') as f:
                f.write(str(time.ctime(time.time())) + ': ' + info + '\n')

        pattern = r'"schoolname": "(.*?)",'
        dic = re.findall(pattern, html)
        if dic == []:
            break
        school_list += dic
        info = ' catching....%d' % page
        print info

        # 写入log
        with open(LOG_FILE_NAME, 'a+') as f:
            f.write(str(time.ctime(time.time()))+ ': ' + info + '\n')

        page += 1


    # 把school_list写入json文件
    with open(BASE_DIR + 'university_list.json', 'w') as f:
        f.write(json.dumps(school_list, ensure_ascii=False).encode('utf-8'))

    # 写入log
    with open(LOG_FILE_NAME, 'a+') as f:
        f.write(str(time.ctime(time.time())) + ': ' + '爬虫运行结束' + '\n')


    # 程序结束，修改redis状态码
    redisclient = redis.Redis(host='127.0.0.1', port=6379, db=1)
    redisclient.getset(REDIS_RUN_RECORD, 'False')

    print 'Finished:',SPIDER_FILE_NAME,test1,test2

if __name__ == "__main__":
    main()