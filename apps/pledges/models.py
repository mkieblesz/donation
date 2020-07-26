from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Pledge(models.Model):
    name = models.CharField(max_length=64, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pledge_text = models.CharField(max_length=512)
    co2_formula = models.CharField(max_length=128, null=True, blank=True)
    water_formula = models.CharField(max_length=128, null=True, blank=True)
    waste_formula = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class PledgeQuestion(models.Model):
    class AnswerInputType(models.TextChoices):
        NUMERIC = 'numeric', 'numeric'
        SELECT = 'select', 'select'

    question_id = models.SlugField(primary_key=True)
    pledge = models.ForeignKey('Pledge', on_delete=models.CASCADE)

    answer_input_type = models.CharField(max_length=32, choices=AnswerInputType.choices)
    answer_input_type_options = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text='Add additional input options used to further constrain allowed input values.',
    )

    def has_numeric_answer(self):
        return self.answer_input_type == self.AnswerInputType.NUMERIC


class SelectAnswerFormulaValue(models.Model):
    """Holds values for formula calculation types"""

    pledge_question = models.ForeignKey('PledgeQuestion', on_delete=models.CASCADE)
    answer_value = models.CharField(max_length=64)
    formula_value = models.FloatField()


class UserPledge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pledge = models.ForeignKey('Pledge', on_delete=models.CASCADE)
    message = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        unique_together = ['user', 'pledge']


class UserPledgeAnswer(models.Model):
    user_pledge = models.ForeignKey('UserPledge', on_delete=models.CASCADE)
    pledge_question = models.ForeignKey('PledgeQuestion', on_delete=models.CASCADE)
    answer_value = models.CharField(max_length=64)
    formula_value = models.FloatField(blank=True)

    class Meta:
        unique_together = ['user_pledge', 'pledge_question']

    def get_formula_value(self):
        if self.pledge_question.has_numeric_answer():
            return self.answer_value

        return SelectAnswerFormulaValue.objects.get(answer_value=self.answer_value).formula_value

    def clean(self):
        try:
            self.formula_value = self.get_formula_value()
        except SelectAnswerFormulaValue.DoesNotExist:
            raise ValidationError('Wrong answer.')