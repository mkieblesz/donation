from django.shortcuts import HttpResponse


def homepage(request):
    return HttpResponse('Homepage')


def pledges(request, username):
    return HttpResponse('User pledges')
