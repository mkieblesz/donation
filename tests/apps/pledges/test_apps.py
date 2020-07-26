from django.apps import apps
from apps.pledges.apps import PledgesConfig


def test_pledges_app():
    assert PledgesConfig.name == 'pledges'
    assert apps.get_app_config('pledges').name == 'pledges'
