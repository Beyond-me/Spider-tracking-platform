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
from RedisLogFunc import RedisLog


def main(test1=1, test2=2):
    # 设置默认编码
    reload(sys)
    sys.setdefaultencoding('utf-8')
    RL = RedisLog('Get_university_list', 'json')

    try:
        DATA_FILE_NAME  = RL.DATA_FILE_NAME
        LOG_FILE_NAME = RL.LOG_FILE_NAME

        # 下载器
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)"}
        url = 'http://data.api.gkcx.eol.cn/soudaxue/queryschool.html'  # json
        page = 1
        school_list = []
        while True:

            if RL.check_status() == False:
                RL.loginfo('爬虫退出')
                sys.exit()

            params = {"messtype": "jsonp","callback": "jQuery18305451626836174455_1505063607887","province": "","schooltype": "普通本科","page": str(page),"size": "30","keyWord1": "","schoolprop": "","schoolflag": "","schoolsort": "","schoolid": "","_": "1505063608095",}
            try:
                html = requests.get(url, params=params, headers=headers).text
                RL.loginfo('请求页面%d' % page, 'R')
                RL.loginfo('下载页面%d' % page, 'D')
            except Exception as e:
                html = ''
                RL.loginfo('请求page%d失败, %s' % (page, e), 'E')

            pattern = r'"schoolname": "(.*?)",'
            dic = re.findall(pattern, html)
            if dic == []:
                break
            school_list += dic
            RL.loginfo('写入文件 %d 条'%len(dic), 'I', len(dic))
            page += 1


        # 把school_list写入json文件
        with open(DATA_FILE_NAME, 'w') as f:
            f.write(json.dumps(school_list, ensure_ascii=False).encode('utf-8'))

        RL.loginfo('爬虫运行完成，退出')
    except Exception as e:
        RL.loginfo('遇到意料之外的错误，退出')
    finally:
        RL.commit_redis()
        RL.run_false()

if __name__ == "__main__":
    main(1,2)

