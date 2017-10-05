from django.shortcuts import render
from models import *



def project(request):

    all_project = TProject.objects.all().order_by('-id')

    context = {
        'all_project':all_project,
    }

    return render(request,'project/projectlist.html', context)


def ptype(request, typename):

    typelist = TProject.objects.filter(project_type__typename=typename)
    context = {
        'typelist':typelist,
        'typename':typename,
    }

    return render(request, 'project/projecttypelist.html', context)



def projectdetail(request, pname):

    thisproject = TProject.objects.filter(project_url=pname)

    context = {
        'proje':thisproject[0],
    }

    return render(request, 'project/projectdetail.html', context)
