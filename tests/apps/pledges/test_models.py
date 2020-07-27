import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.pledges.models import Action, Answer, Pledge, Question, SelectAnswerFormulaValue


def test_action_str(db):
    action = Action.objects.create(name='Test', pledge_text='Test')
    assert str(action) == 'Test'


def test_pledge_answer_clean_numeric_answer_success(db):
    action = Action.objects.create(name='Test', pledge_text='Test')
    user = User.objects.create(username='user1')

    question = Question.objects.create(
        action=action, question_id='test', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge = Pledge.objects.create(user=user, action=question.action, message='I will do that!',)
    a = Answer(pledge=pledge, question=question, answer_value=1,)
    a.clean()

    assert a.formula_value == 1


def test_pledge_answer_clean_selectable_answer_formula_success(db):
    action = Action.objects.create(name='Test', pledge_text='Test')
    user = User.objects.create(username='user1')
    question = Question.objects.create(
        action=action, question_id='test', answer_input_type=Question.AnswerInputType.SELECT,
    )
    SelectAnswerFormulaValue.objects.get_or_create(
        question=question, answer_value='test_answer_value', formula_value=0.5
    )
    pledge = Pledge.objects.create(user=user, action=question.action, message='I will do that!',)
    a = Answer(pledge=pledge, question=question, answer_value='test_answer_value',)
    a.clean()

    assert a.formula_value == 0.5


def test_pledge_answer_clean_selectable_answer_formula_does_not_exist_error(db):
    action = Action.objects.create(name='Test', pledge_text='Test')
    user = User.objects.create(username='user1')
    question = Question.objects.create(
        action=action, question_id='test', answer_input_type=Question.AnswerInputType.SELECT,
    )
    pledge = Pledge.objects.create(user=user, action=question.action, message='I will do that!',)
    with pytest.raises(ValidationError) as excinfo:
        Answer(pledge=pledge, question=question, answer_value='not selectable value',).clean()

        assert 'Wrong answer.' == str(excinfo.value)
