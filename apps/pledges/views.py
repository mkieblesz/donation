from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, get_object_or_404

from apps.pledges.models import Pledge

BASE_HTML = '<html><body>{body}</body></html>'


def homepage(request):
    pledge_count = Pledge.objects.count()
    response_body = 'Homepage</br></br>'
    response_body += f'number of pledges: {pledge_count}</br>'

    if pledge_count > 0:
        co2 = 0
        water = 0
        waste = 0
        response_body += f'Impact 1: {co2:.2f} of CO2 less in the athmosphere</br>'
        response_body += f'Impact 2: {water:.2f} less water used</br>'
        response_body += f'Impact 3: {waste:.2f} less waste</br>'

    return HttpResponse(BASE_HTML.format(body=response_body))


def user_pledges(request, username):
    user = get_object_or_404(User, username=username)

    # user pledge query
    pledges = Pledge.objects.filter(user=user).select_related('action')

    response_body = f'{username} pledges</br></br>'
    for counter, pledge in enumerate(pledges):
        response_body += f'{counter + 1}. {pledge.action.name} - {pledge.action.pledge_text}\n'
    else:
        response_body += 'User has made no pledges yet.</br>'

    return HttpResponse(BASE_HTML.format(body=response_body))
