from django.contrib.auth.models import User
from apps.pledges.models import (
    SelectAnswerFormulaValue,
    Action,
    Question,
    Pledge,
    Answer,
)

action, _ = Action.objects.get_or_create(
    name='Veg Out',
    pledge_text=(
        'At the moment, I munch on {current_meals} meaty meals each week. For the next two '
        'months, I pledge to go veg for {veggie_meals} extra meals each week.'
    ),
    co2_formula='0.884 * {veggie_meals} * 8.7',
    water_formula='0.75 * {current_meals}',
    waste_formula='0.2 * {current_meals} * {veggie_meals}',
)
veggie_meals, _ = Question.objects.get_or_create(
    action=action,
    question_id='veggie_meals',
    answer_input_type=Question.AnswerInputType.NUMERIC,
)
for i in range(1, 6):
    SelectAnswerFormulaValue.objects.get_or_create(
        question=veggie_meals, answer_value=i, formula_value=2.5
    )
SelectAnswerFormulaValue.objects.get_or_create(
    question=veggie_meals, answer_value=6, formula_value=3
)
current_meals, _ = Question.objects.get_or_create(
    action=action,
    question_id='current_meals',
    answer_input_type=Question.AnswerInputType.NUMERIC,
)

user1 = User.objects.get(username='user1')
pledge, _ = Pledge.objects.get_or_create(user=user1, action=action, message='I will do that!')
Answer.objects.get_or_create(
    pledge=pledge, question=veggie_meals, answer_value=4, formula_value=2.5
)
Answer.objects.get_or_create(
    pledge=pledge, question=current_meals, answer_value=2, formula_value=2
)

user2 = User.objects.get(username='user2')
pledge, _ = Pledge.objects.get_or_create(user=user2, action=action, message='You bet I do that!')
Answer.objects.get_or_create(
    pledge=pledge, question=veggie_meals, answer_value=6, formula_value=6
)
Answer.objects.get_or_create(
    pledge=pledge, question=current_meals, answer_value=5, formula_value=5
)
