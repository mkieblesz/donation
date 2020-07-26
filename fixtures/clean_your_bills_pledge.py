from django.contrib.auth.models import User
from apps.pledges.models import (
    SelectAnswerFormulaValue,
    Pledge,
    PledgeQuestion,
    UserPledge,
    UserPledgeAnswer,
)

pledge, _ = Pledge.objects.get_or_create(
    name='Clean your bills',
    pledge_text=(
        'Within the next two months, I pledge to switch from my current energy supplier – '
        'which is {energy_supplier} – to a green energy supplier. {number_of_people} people '
        'live in our home. My house is mainly heated by {heating_source}.'
    ),
    co2_formula='49 * {energy_supplier} * {number_of_people} * {heating_source}',
)
energy_supplier, _ = PledgeQuestion.objects.get_or_create(
    pledge=pledge,
    question_id='energy_supplier',
    answer_input_type=PledgeQuestion.AnswerInputType.SELECT,
)
bog_standard, _ = SelectAnswerFormulaValue.objects.get_or_create(
    pledge_question=energy_supplier, answer_value='bog standard', formula_value=0.5
)
a_great_green_tarif, _ = SelectAnswerFormulaValue.objects.get_or_create(
    pledge_question=energy_supplier, answer_value='a great green tarif', formula_value=0
)
heating_source, _ = PledgeQuestion.objects.get_or_create(
    pledge=pledge,
    question_id='heating_source',
    answer_input_type=PledgeQuestion.AnswerInputType.SELECT,
)
gas_or_oil, _ = SelectAnswerFormulaValue.objects.get_or_create(
    pledge_question=heating_source, answer_value='gas or oil', formula_value=5
)
electricity, _ = SelectAnswerFormulaValue.objects.get_or_create(
    pledge_question=heating_source, answer_value='electricity', formula_value=3
)
number_of_people, _ = PledgeQuestion.objects.get_or_create(
    pledge=pledge,
    question_id='number_of_people',
    answer_input_type=PledgeQuestion.AnswerInputType.NUMERIC,
)


user1 = User.objects.get(username='user1')
up, _ = UserPledge.objects.get_or_create(
    user=user1, pledge=pledge, message='For sure I will do that!'
)
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up,
    pledge_question=energy_supplier,
    answer_value=bog_standard.answer_value,
    formula_value=bog_standard.formula_value,
)
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up,
    pledge_question=heating_source,
    answer_value=electricity.answer_value,
    formula_value=electricity.formula_value,
)
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up, pledge_question=number_of_people, answer_value=4, formula_value=4
)

user2 = User.objects.get(username='user2')
up, _ = UserPledge.objects.get_or_create(user=user2, pledge=pledge, message='You bet I do that!')
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up,
    pledge_question=energy_supplier,
    answer_value=a_great_green_tarif.answer_value,
    formula_value=a_great_green_tarif.formula_value,
)
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up,
    pledge_question=heating_source,
    answer_value=gas_or_oil.answer_value,
    formula_value=gas_or_oil.formula_value,
)
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up, pledge_question=number_of_people, answer_value=1, formula_value=1
)
