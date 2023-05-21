from django.contrib import admin
from .models import Usercreds, BaseModel, Category, Question, Answer

# Register your models here.

admin.site.register(Usercreds)
admin.site.register(Category)


class AnswerAdmin(admin.StackedInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
