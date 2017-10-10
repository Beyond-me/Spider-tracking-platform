killall -9 uwsgi;
nginx -s stop;
uwsgi --ini /root/django-blog-spider/spidermanage/spidermanage/uwsgi.ini;
nginx;
ps -ef|grep uwsgi;
echo "-----------------------------------"
ps -ef|grep nginx;
