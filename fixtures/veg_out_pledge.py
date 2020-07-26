from django.contrib.auth.models import User
from apps.pledges.models import (
    SelectAnswerFormulaValue,
    Pledge,
    PledgeQuestion,
    UserPledge,
    UserPledgeAnswer,
)

pledge, _ = Pledge.objects.get_or_create(
    name='Veg Out',
    pledge_text=(
        'At the moment, I munch on {current_meals} meaty meals each week. For the next two '
        'months, I pledge to go veg for {veggie_meals} extra meals each week.'
    ),
    co2_formula='0.884 * {veggie_meals} * 8.7',
    water_formula='0.75 * {current_meals}',
    waste_formula='0.2 * {current_meals} * {veggie_meals}',
)
veggie_meals, _ = PledgeQuestion.objects.get_or_create(
    pledge=pledge,
    question_id='veggie_meals',
    answer_input_type=PledgeQuestion.AnswerInputType.NUMERIC,
)
for i in range(1, 6):
    SelectAnswerFormulaValue.objects.get_or_create(
        pledge_question=veggie_meals, answer_value=i, formula_value=2.5
    )
SelectAnswerFormulaValue.objects.get_or_create(
    pledge_question=veggie_meals, answer_value=6, formula_value=3
)
current_meals, _ = PledgeQuestion.objects.get_or_create(
    pledge=pledge,
    question_id='current_meals',
    answer_input_type=PledgeQuestion.AnswerInputType.NUMERIC,
)

user1 = User.objects.get(username='user1')
up, _ = UserPledge.objects.get_or_create(user=user1, pledge=pledge, message='I will do that!')
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up, pledge_question=veggie_meals, answer_value=4, formula_value=2.5
)
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up, pledge_question=current_meals, answer_value=2, formula_value=2
)

user2 = User.objects.get(username='user2')
up, _ = UserPledge.objects.get_or_create(user=user2, pledge=pledge, message='You bet I do that!')
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up, pledge_question=veggie_meals, answer_value=6, formula_value=6
)
UserPledgeAnswer.objects.get_or_create(
    user_pledge=up, pledge_question=current_meals, answer_value=5, formula_value=5
)
