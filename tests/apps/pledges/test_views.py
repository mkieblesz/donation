from django.contrib.auth.models import User
from django.urls import reverse

from apps.pledges.models import Action, Answer, Pledge, Question


def test_homepage_success(db, client):
    assert client.get(reverse('homepage')).status_code == 200
    assert 'Homepage' in client.get(reverse('homepage')).content.decode('utf-8')


def test_homepage_content_pledge_count(db, client):
    user = User.objects.create(username='user1')
    action = Action.objects.create(name='Action 1', pledge_text='Test', co2_formula='10',)
    question = Question.objects.create(
        action=action, question_id='test', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    Pledge.objects.create(user=user, action=question.action)
    assert 'number of pledges: 1</br>' in client.get(reverse('homepage')).content.decode('utf-8')


def test_homepage_content_pledge_aggregate_stats(db, client):
    user = User.objects.create(username='user1')

    action1 = Action.objects.create(name='Action 1', pledge_text='Test', co2_formula='10',)
    question1 = Question.objects.create(
        action=action1, question_id='question', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge1 = Pledge.objects.create(user=user, action=question1.action)
    Answer.objects.create(pledge=pledge1, question=question1, answer_value=2, formula_value=2.0)

    action2 = Action.objects.create(name='Action 2', pledge_text='Test', co2_formula='20',)
    question2 = Question.objects.create(
        action=action2, question_id='question', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge2 = Pledge.objects.create(user=user, action=question2.action)
    Answer.objects.create(pledge=pledge2, question=question2, answer_value=6, formula_value=6.0)

    response_content = client.get(reverse('homepage')).content.decode('utf-8')
    assert 'Impact 1: 30.00 of CO2 less in the athmosphere' in response_content


def test_homepage_content_pledge_all_stats_present(db, client):
    user = User.objects.create(username='user1')
    action = Action.objects.create(
        name='Action', pledge_text='Test', co2_formula='0', water_formula='0', waste_formula='0',
    )
    question = Question.objects.create(
        action=action, question_id='question', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge = Pledge.objects.create(user=user, action=question.action)
    Answer.objects.create(pledge=pledge, question=question, answer_value=1, formula_value=1.0)

    response_content = client.get(reverse('homepage')).content.decode('utf-8')
    assert 'Impact 1: 0.00 of CO2 less in the athmosphere' in response_content
    assert 'Impact 2: 0.00 less water used' in response_content
    assert 'Impact 3: 0.00 less waste' in response_content


def test_user_pledges_success(db, client):
    user = User.objects.create(username='user1')

    response = client.get(reverse('user_pledges', kwargs={'username': user.username}))
    assert response.status_code == 200
    assert 'user1 pledges</br></br>' in response.content.decode('utf-8')


def test_user_pledges_2_pledges_made(db, client):
    user = User.objects.create(username='user1')
    action1 = Action.objects.create(
        name='Action 1', pledge_text='I pledge to mown the lawn {number_per_week} times a week.'
    )
    question1 = Question.objects.create(
        action=action1,
        question_id='number_per_week',
        answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge1 = Pledge.objects.create(user=user, action=question1.action)
    Answer.objects.create(pledge=pledge1, question=question1, answer_value=2, formula_value=2.0)
    action2 = Action.objects.create(
        name='Action 2', pledge_text='I pledge to eat breakfast {number_per_week} times a week.'
    )
    question2 = Question.objects.create(
        action=action2,
        question_id='number_per_week',
        answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge2 = Pledge.objects.create(user=user, action=question2.action)
    Answer.objects.create(pledge=pledge2, question=question2, answer_value=7, formula_value=7.0)

    response = client.get(reverse('user_pledges', kwargs={'username': user.username}))
    response_content = response.content.decode('utf-8')
    assert '1. Action 1 - I pledge to mown the lawn 2 times a week.' in response_content
    assert '2. Action 2 - I pledge to eat breakfast 7 times a week.' in response_content


def test_user_pledges_no_pledges_made(db, client):
    user = User.objects.create(username='user1')

    response = client.get(reverse('user_pledges', kwargs={'username': user.username}))
    assert 'User has made no pledges yet.' in response.content.decode('utf-8')
