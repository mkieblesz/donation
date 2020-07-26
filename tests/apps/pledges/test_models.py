import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.pledges.models import (
    Pledge,
    PledgeQuestion,
    SelectAnswerFormulaValue,
    UserPledge,
    UserPledgeAnswer
)


@pytest.fixture
def pledge(db):
    yield Pledge.objects.create(name='Test', pledge_text='Test')


@pytest.fixture
def user(db):
    yield User.objects.create(username='user1')


@pytest.fixture
def selectable_pledge_question(pledge):
    yield PledgeQuestion.objects.create(
        pledge=pledge, question_id='test', answer_input_type=PledgeQuestion.AnswerInputType.SELECT,
    )


def test_pledge_str(pledge):
    assert str(pledge) == 'Test'


def test_user_pledge_answer_clean_numeric_answer_success(pledge, user):
    pledge_question = PledgeQuestion.objects.create(
        pledge=pledge, question_id='test', answer_input_type=PledgeQuestion.AnswerInputType.NUMERIC,
    )
    up = UserPledge.objects.create(
        user=user, pledge=pledge_question.pledge, message='I will do that!',
    )
    upa = UserPledgeAnswer(
        user_pledge=up,
        pledge_question=pledge_question,
        answer_value=1,
    )
    upa.clean()

    assert upa.formula_value == 1


def test_user_pledge_answer_clean_selectable_answer_formula_success(pledge, user):
    pledge_question = PledgeQuestion.objects.create(
        pledge=pledge, question_id='test', answer_input_type=PledgeQuestion.AnswerInputType.SELECT,
    )
    SelectAnswerFormulaValue.objects.get_or_create(
        pledge_question=pledge_question, answer_value='test_answer_value', formula_value=0.5
    )
    up = UserPledge.objects.create(
        user=user, pledge=pledge_question.pledge, message='I will do that!',
    )
    upa = UserPledgeAnswer(
        user_pledge=up,
        pledge_question=pledge_question,
        answer_value='test_answer_value',
    )
    upa.clean()

    assert upa.formula_value == 0.5


def test_user_pledge_answer_clean_selectable_answer_formula_does_not_exist_error(pledge, user):
    pledge_question = PledgeQuestion.objects.create(
        pledge=pledge, question_id='test', answer_input_type=PledgeQuestion.AnswerInputType.SELECT,
    )
    up = UserPledge.objects.create(
        user=user, pledge=pledge_question.pledge, message='I will do that!',
    )
    with pytest.raises(ValidationError) as excinfo:
        UserPledgeAnswer(
            user_pledge=up,
            pledge_question=pledge_question,
            answer_value='not selectable value',
        ).clean()

        assert 'Wrong answer.' == str(excinfo.value)
