from django.contrib import admin

# Register your models here.

from .models import Question, Choice


# admin.site.register(Question)
# admin.site.register(Choice)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5
class QuestionAdmin(admin.ModelAdmin):

    # fields = ['pub_date','question_text']
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date Information', {'fields':['pub_date']}),
    ]
    list_display =  ('question_text','pub_date','published_date')
    list_filter = ['pub_date']

    inlines = [ChoiceInline]

admin.site.register(Question,QuestionAdmin)


