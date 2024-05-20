from django.contrib import admin
from .models import Quiz, Question, Answer

class AnswerInlineModel(admin.TabularInline):
    model = Answer
    extra = 3  # Number of extra inline forms to display

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "quiz", "created_at"]
    search_fields = ["title"]  # Enable search by title
    list_filter = ["quiz"]  # Add filter by quiz
    inlines = [AnswerInlineModel]

class QuizAdmin(admin.ModelAdmin):
    list_display = ["quiz_id", "title", "author", "created_at", "question_count"]
    search_fields = ["title"]  # Enable search by title
    list_filter = ["author"]  # Add filter by author
    ordering = ["-created_at"]  # Display quizzes ordered by creation date

class AnswerAdmin(admin.ModelAdmin):
    list_display = ["answer_text", "is_right", "question"]
    search_fields = ["answer_text"]  # Enable search by answer text
    list_filter = ["question__quiz"]  # Add filter by quiz

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)