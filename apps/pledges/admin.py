from django.contrib import admin

from apps.pledges import models


class QuestionInline(admin.TabularInline):
    model = models.Question
    extra = 0
    show_change_link = True


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'created_at', 'pledge_text')


class SelectAnswerFormulaValueInline(admin.TabularInline):
    model = models.SelectAnswerFormulaValue
    extra = 0


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [SelectAnswerFormulaValueInline]
    list_display = ('question_id', 'action', 'answer_input_type')


class AnswerInline(admin.TabularInline):
    model = models.Answer
    extra = 0
    readonly_fields = ('formula_value',)


@admin.register(models.Pledge)
class PledgeAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('user', 'action', 'message')
