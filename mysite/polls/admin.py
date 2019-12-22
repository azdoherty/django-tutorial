from django.contrib import admin
from .models import Question, Choice
# Register your models here.

# admin.site.register(Question)

class ChoiceInline(admin.TabularInline):
    # best way to register is as an inline field
    model = Choice
    extra = 3


# create an admin class then register it with the appropriate model
class QuestionAdmin(admin.ModelAdmin):
    # control order of quetions
    # fields = ['pub_date', 'question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    # use fieldsets to create logical groupings
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)


# You could register choice as separate page, but that is extra work
# admin.site.register(Choice)
