# coding=utf-8
import csv
import re
import sys
import time

import requests

from RedisLogFunc import RedisLog


def request(page, word, RL):
    url = 'http://news.baidu.com/ns'
    params = {
        "word": word,
        "pn": str(page),
        "rn": "10",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    }
    try:
        if RL.check_status() == False:
            sys.exit()
        time.sleep(1)

        response = requests.get(url, headers=headers, params=params)
        RL.loginfo('请求%s成功' % params, 'R')
        RL.loginfo('下载%s成功' % params, 'D')
        if RL.check_status() == False:
            sys.exit()
        time.sleep(1)
    except Exception as e:
        RL.loginfo('请求失败,url:%s,e:%s' % (params, e), 'E')
        response = ''

    nowtime = time.time()
    return response, nowtime


def parse(response, nowtime, RL):
    global first_csv
    html = response.text

    pattern = r'>.*?</a></h3>.*?data-click="{'
    result = re.compile(pattern, re.DOTALL).findall(html)
    RL.loginfo('正在解析,找到%d条可用数据' % len(result))

    pattern_title = r'>(.*?)</a></h3>'
    pattern_href = r'<h3 class="c-title"><a href="(.*?)"'
    pattern_author = r'<p class="c-author">(.*?)</p>'

    for r in result:
        item = {}
        title = re.findall(pattern_title, r)
        href = re.findall(pattern_href, r)
        author = re.findall(pattern_author, r)

        try:
            item['title'] = title[0].replace('<em>', '').replace('</em>', '')
        except Exception as e:
            item['title'] = 'NULL'
            RL.loginfo('抽取title失败，将置为空')

        try:
            item['href'] = href[0]
        except Exception as e:
            item['href'] = 'NULL'
            RL.loginfo('抽取href失败，将置为空')

        try:
            auth_time = author[0].split('&nbsp;&nbsp;')

            item['author'] = auth_time[0]
            check_time = auth_time[1]

            if '分钟' in check_time:
                num = check_time.replace('分钟前', '')
                realtime = nowtime - int(num) * 60
                item['time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(realtime))
            elif '小时' in check_time:
                num = check_time.replace('小时前', '')
                realtime = nowtime - int(num) * 3600
                item['time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(realtime))
            else:
                item['time'] = check_time + time.strftime('%Y-%m-%d %H:%M', time.localtime(nowtime))
        except Exception as e:
            item['author'] = 'NULL'
            item['time'] = 'NULL'
            RL.loginfo('抽取author,time失败，将置为空')

        RL.write_csv(item)


def main(word='word', count=25):

    reload(sys)
    sys.setdefaultencoding('utf-8')
    RL = RedisLog('BaiduNwes', 'csv')
    count = int(count)

    try:
        num = (count // 10 + 1) * 10
        RL.loginfo('即将采集 %d 条关键字为 %s 的新闻' % (count, word))

        for page in range(0, num, 10):
            response, nowtime = request(page, word, RL)
            if response == '':
                pass
            else:
                parse(response, nowtime, RL)
        RL.loginfo('采集完成，即将退出')
    except Exception as e:
        RL.loginfo('发生意料之外的错误%s' % e, mode='E')
    finally:
        RL.commit_redis()
        RL.run_false()


if __name__ == '__main__':
    main()