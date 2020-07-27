from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.pledges.misc import get_var_names_from_string_format


class Action(models.Model):
    name = models.CharField(max_length=64, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pledge_text = models.CharField(max_length=512)
    co2_formula = models.CharField(max_length=128, null=True, blank=True)
    water_formula = models.CharField(max_length=128, null=True, blank=True)
    waste_formula = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    class AnswerInputType(models.TextChoices):
        NUMERIC = 'numeric', 'numeric'
        SELECT = 'select', 'select'

    action = models.ForeignKey('Action', on_delete=models.CASCADE)
    question_id = models.SlugField()

    answer_input_type = models.CharField(max_length=32, choices=AnswerInputType.choices)
    answer_input_type_options = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text='Add additional input options used to further constrain allowed input values.',
    )

    class Meta:
        unique_together = ['action', 'question_id']

    def has_numeric_answer(self):
        return self.answer_input_type == self.AnswerInputType.NUMERIC


class SelectAnswerFormulaValue(models.Model):
    """Holds values for formula calculation types"""

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_value = models.CharField(max_length=64)
    formula_value = models.FloatField()


class Pledge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.ForeignKey('Action', on_delete=models.CASCADE)
    message = models.CharField(max_length=512, null=True, blank=True)
    co2_impact = models.FloatField(null=True, blank=True)
    water_impact = models.FloatField(null=True, blank=True)
    waste_impact = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'action']

    def get_pledge_text(self):
        return self.action.pledge_text.format(
            **{answer.question.question_id: answer.answer_value for answer in self.answer_set.all()}
        )

    def get_formula_impact(self, formula_name):
        formula_template = getattr(self.action, formula_name)
        if formula_template is None:
            return None

        formula_questions = get_var_names_from_string_format(formula_template)
        formula_values = {
            answer.question.question_id: answer.formula_value
            for answer in self.answer_set.all()
        } if formula_questions else {}

        # not all required answers provided
        if sorted(formula_values.keys()) != sorted(formula_questions):
            return None

        return eval(formula_template.format(**formula_values))

    def update_impact(self):
        self.co2_impact = self.get_formula_impact('co2_formula')
        self.water_impact = self.get_formula_impact('water_formula')
        self.waste_impact = self.get_formula_impact('waste_formula')

        self.save()


class Answer(models.Model):
    pledge = models.ForeignKey('Pledge', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_value = models.CharField(max_length=64)
    formula_value = models.FloatField(blank=True)

    class Meta:
        unique_together = ['pledge', 'question']

    def get_formula_value(self):
        if self.question.has_numeric_answer():
            return self.answer_value

        return SelectAnswerFormulaValue.objects.get(answer_value=self.answer_value).formula_value

    def clean(self):
        try:
            self.formula_value = self.get_formula_value()
        except SelectAnswerFormulaValue.DoesNotExist:
            raise ValidationError('Wrong answer.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pledge.update_impact()
