from django.contrib import admin

from apps.pledges import models


class PledgeQuestionInline(admin.TabularInline):
    model = models.PledgeQuestion
    extra = 0
    show_change_link = True


@admin.register(models.Pledge)
class PledgeAdmin(admin.ModelAdmin):
    inlines = [PledgeQuestionInline]
    list_display = ('name', 'created_at', 'pledge_text')


class SelectAnswerFormulaValueInline(admin.TabularInline):
    model = models.SelectAnswerFormulaValue
    extra = 0


@admin.register(models.PledgeQuestion)
class PledgeQuestionAdmin(admin.ModelAdmin):
    inlines = [SelectAnswerFormulaValueInline]
    list_display = ('question_id', 'pledge', 'answer_input_type')


class UserPledgeAnswerInline(admin.TabularInline):
    model = models.UserPledgeAnswer
    extra = 0
    readonly_fields = ('formula_value',)


@admin.register(models.UserPledge)
class UserPledgeAdmin(admin.ModelAdmin):
    inlines = [UserPledgeAnswerInline]
    list_display = ('user', 'pledge', 'message')
