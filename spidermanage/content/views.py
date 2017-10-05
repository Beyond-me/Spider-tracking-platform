#coding=utf-8

from django.shortcuts import render
from models import *
import project.models as pm

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

    print(arti)
    context = {
        'arti':arti[0],
    }
    return render(request, 'content/articeldetail.html', context)
























