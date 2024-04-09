from django.contrib import admin
from .models import Courses, Lesson, Tasks, Allowance, LessonProgress


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'lesson_slug', 'title', 'number')
    list_filter = ('course',)


class TasksAdmin(admin.ModelAdmin):
    list_display = ('lesson',)
    list_filter = ('lesson',)


class AllowanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'allow')
    list_filter = ('user', 'course', 'allow')


class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'task')
    list_filter = ('user', 'task')


admin.site.register(Courses, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Allowance, AllowanceAdmin)
admin.site.register(LessonProgress, ProgressAdmin)