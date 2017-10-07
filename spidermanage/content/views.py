#coding=utf-8

from django.shortcuts import render
from models import *
import project.models as pm
from django.core import paginator

# Create your views here.

def index(request):
    all_articel = Article.objects.all().order_by('-id')[:5]

    all_project = pm.TProject.objects.all().order_by('-id')[:5]

    context = {
        'all_articel':all_articel,
        'all_project':all_project,
    }
    return render(request, 'content/index.html', context)


def articel(request):

    all_articel = Article.objects.all().order_by('-id')

    context = {
        'all_articel': all_articel,
        'tags':'',
    }
    return render(request, 'content/articellist.html', context)


def choosetype(request, typename):

    all_articel = Article.objects.filter(articel_type__typename=typename)

    context = {
        'all_articel': all_articel,
        'typename':typename,
        'tags':'',
    }
    return render(request, 'content/articeltypelixt.html', context)



def articeldetail(request, idnum):

    print(idnum)

    arti = Article.objects.filter(id=idnum)
    arti = arti[0]
    alltag = arti.articel_tag.all()


    print(arti)
    context = {
        'arti':arti,
        'alltag':alltag,
    }
    return render(request, 'content/articeldetail.html', context)



def articelpage(request, index):

    # 获取所有的的数据，list是一个列表，包含有所有数据对应的实例对象
    list = Article.objects.all()
    # 使用Paginator方法返回一个分页的对象
    # 这个对象包括所有数据，分页的情况
    pag = paginator.Paginator(list, 5)
    # 使用此判断语句是为了在用户跳转www.xxx.com/info/时也能访问第一页
    if index == '':
        index = 1
    # 返回指定（index）页的数据，用于呈现在指定页上
    page = pag.page(index)
    # 构造上下文，以便html文件中能调用对应页的数据
    context = {
        'page': page,
        'viewIndex':int(index),
    }
    return render(request, 'content/articellist.html', context)




















