from django.shortcuts import HttpResponse

from apps.pledges.models import Pledge

HOMEPAGE_TEMPLATE = """Homepage

number of pledges: {pledge_count}
Impact 1: {co2} of CO2 less in the athmosphere
Impact 2: {water} less water used
Impact 3: {waste} less waste
"""

USER_PLEDGES_TEMPLATE = """User pledges

{username} user has made following pledges: {pledges}"""


def homepage(request):
    pledge_count = Pledge.objects.count()
    return HttpResponse(
        HOMEPAGE_TEMPLATE.format(pledge_count=pledge_count, co2=0, water=0, waste=0)
    )


def user_pledges(request, username):
    pledge_list = list(
        Pledge.objects.filter(user__username=username)
        .select_related('action')
        .values_list('action__name', flat=True)
        .distinct()
    )
    return HttpResponse(
        USER_PLEDGES_TEMPLATE.format(username=username, pledges=', '.join(pledge_list))
    )
