#coding=utf-8
from models import Spider
import redis

def sync(func):
    def redis_to_mysql(request ,*args,**kwargs):
        try:
            all_spider = Spider.objects.all()

            for spider_obj in all_spider:

                func_name = spider_obj.spider_runfunction

                if func_name == 'no info':
                    pass
                else:
                    redisclient = redis.Redis(host='127.0.0.1', port=6379, db=1)
                    li = [func_name + ":requestCount",func_name + ":downloadCount",func_name + ":infoCount",func_name + ":errorCount"]
                    rli = redisclient.mget(li)
                    rs = redisclient.get(func_name + ":runing")
                    spider_obj.spider_request_count = str(rli[0])
                    spider_obj.spider_download_count = str(rli[1])
                    spider_obj.spider_info_count = str(rli[2])
                    spider_obj.spider_error_count = str(rli[3])
                    if rs == None:
                        spider_obj.spider_runing = False
                    elif rs == b'False':
                        spider_obj.spider_runing = False
                    else:
                        spider_obj.spider_runing = True

                    spider_obj.save()

        except Exception as e:
            print '同步数据出错:',e
        finally:
            return func(request ,*args,**kwargs)

    return redis_to_mysql


# 仅仅同步爬虫运行状态
def just_sync_run(func):
    def redis_to_mysql_run(request ,*args,**kwargs):
        try:
            spiserid = request.GET['spider_id']
            result = Spider.objects.filter(id=spiserid)
            spider_obj = result[0]
            func_name = spider_obj.spider_runfunction

            if func_name == 'no info':
                pass
            else:
                redisclient = redis.Redis(host='127.0.0.1', port=6379, db=1)
                rs = redisclient.get(func_name + ":runing")
                if rs == None:
                    spider_obj.spider_runing = False
                elif rs == b'False':
                    spider_obj.spider_runing = False
                else:
                    spider_obj.spider_runing = True
                spider_obj.save()

        except Exception as e:
            print '同步数据出错:',e
        finally:
            return func(request ,*args,**kwargs)

    return redis_to_mysql_run