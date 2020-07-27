import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.pledges.models import Action, Answer, Pledge, Question, SelectAnswerFormulaValue


def test_action_str(db):
    action = Action.objects.create(name='Test', pledge_text='Test')
    assert str(action) == 'Test'


def test_pledge_get_pledge_text(db):
    action = Action.objects.create(name='Test', pledge_text='I plead {number} meals per week.')
    user = User.objects.create(username='user1')
    question = Question.objects.create(
        action=action, question_id='number', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge = Pledge.objects.create(user=user, action=question.action)
    Answer.objects.create(pledge=pledge, question=question, answer_value=2, formula_value=2.0)

    assert pledge.get_pledge_text() == 'I plead 2 meals per week.'


def test_pledge_answer_clean_numeric_answer_success(db):
    action = Action.objects.create(name='Test', pledge_text='Test')
    user = User.objects.create(username='user1')

    question = Question.objects.create(
        action=action, question_id='test', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge = Pledge.objects.create(user=user, action=question.action)
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
    pledge = Pledge.objects.create(user=user, action=question.action)
    a = Answer(pledge=pledge, question=question, answer_value='test_answer_value',)
    a.clean()

    assert a.formula_value == 0.5


def test_pledge_get_formula_impact_empty_formula(db):
    action = Action.objects.create(name='Test', pledge_text='Test', co2_formula=None)
    user = User.objects.create(username='user1')
    pledge = Pledge.objects.create(user=user, action=action)

    assert pledge.get_formula_impact('co2_formula') is None


def test_pledge_get_formula_impact_not_all_answers_provided(db):
    action = Action.objects.create(name='Test', pledge_text='Test', co2_formula='{question}')
    user = User.objects.create(username='user1')
    pledge = Pledge.objects.create(user=user, action=action)
    question = Question.objects.create(
        action=action, question_id='question', answer_input_type=Question.AnswerInputType.NUMERIC,
    )

    assert pledge.get_formula_impact('co2_formula') is None

    Answer.objects.create(pledge=pledge, question=question, answer_value=1, formula_value=1.0)

    assert pledge.get_formula_impact('co2_formula') == 1.0


def test_pledge_update_impact_after_answer_save(db):
    action = Action.objects.create(
        name='Test',
        pledge_text='Test',
        co2_formula='{question}',
        water_formula='{question} * 2',
        waste_formula='{question} * 3',
    )
    user = User.objects.create(username='user1')

    question = Question.objects.create(
        action=action, question_id='question', answer_input_type=Question.AnswerInputType.NUMERIC,
    )
    pledge = Pledge.objects.create(user=user, action=question.action)

    assert pledge.co2_impact is None
    assert pledge.water_impact is None
    assert pledge.waste_impact is None

    Answer.objects.create(pledge=pledge, question=question, answer_value=1, formula_value=1.0)

    pledge.refresh_from_db()
    assert pledge.co2_impact == 1.0
    assert pledge.water_impact == 2.0
    assert pledge.waste_impact == 3.0


def test_pledge_answer_clean_selectable_answer_formula_does_not_exist_error(db):
    action = Action.objects.create(name='Test', pledge_text='Test')
    user = User.objects.create(username='user1')
    question = Question.objects.create(
        action=action, question_id='test', answer_input_type=Question.AnswerInputType.SELECT,
    )
    pledge = Pledge.objects.create(user=user, action=question.action)
    with pytest.raises(ValidationError) as excinfo:
        Answer(pledge=pledge, question=question, answer_value='not selectable value',).clean()

        assert 'Wrong answer.' == str(excinfo.value)
