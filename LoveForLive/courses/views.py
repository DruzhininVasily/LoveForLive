from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Courses, Allowance, Lesson, Tasks, LessonProgress, Dossing
from .forms import LessonProgressFormSet
from .services import open_file
from django.http import StreamingHttpResponse
from requests import post


class CoursesView(ListView):
    model = Courses
    template_name = 'courses/courses.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CoursesView, self).get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            allow = Allowance.objects.filter(user=self.request.user).all()
        else:
            allow = None
        ctx['title'] = 'Онлайн курсы'
        ctx['allow'] = allow
        return ctx


class DossingView(DetailView):
    model = Courses
    template_name = 'courses/dossing.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(DossingView, self).get_context_data(**kwargs)
        course = Courses.objects.filter(slug=self.kwargs['slug']).first()
        dossing = Dossing.objects.get(course=course)
        dossing_list = dossing.dossing_list.split(';')
        if dossing_list[-1] == '':
            dossing_list.pop()
        ctx['course'] = course
        ctx['dossing_list'] = dossing_list
        return ctx


class CourseDetailPage(DetailView):
    model = Courses
    template_name = 'courses/course.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(**kwargs)
        course = Courses.objects.filter(slug=self.kwargs['slug']).first()
        allow = Allowance.objects.filter(course=course, user=self.request.user).first()
        lessons = Lesson.objects.filter(course=course).order_by('number')
        progress = []
        for lesson in lessons:
            tasks = Tasks.objects.filter(lesson=lesson).all()
            results = []
            for task in tasks:
                result = LessonProgress.objects.filter(user=self.request.user, task=task)
                result = result[0].status
                results.append(result)
            prog = all(results)
            progress.append(prog)
        ctx['progress'] = progress
        ctx['title'] = course
        ctx['allow'] = allow
        ctx['lessons'] = lessons
        return ctx


class LessonDetailPage(DetailView):
    model = Courses
    template_name = 'courses/lesson-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(**kwargs)
        course = Courses.objects.filter(slug=self.kwargs['slug']).first()
        allow = Allowance.objects.filter(course=course).first().allow
        lesson = Lesson.objects.filter(lesson_slug=self.kwargs['lesson_slug']).first()
        tasks = Tasks.objects.filter(lesson=lesson).all()
        progress = []
        for task in tasks:
            progress.append(LessonProgressFormSet(queryset=LessonProgress.objects.filter(user=self.request.user, task=task)))
        ctx['title'] = lesson
        ctx['lesson'] = lesson
        ctx['tasks'] = tasks
        ctx['course'] = course
        ctx['progress'] = progress
        ctx['allow'] = allow
        return ctx

    def post(self, request, *args, **kwargs):
        formset = LessonProgressFormSet(self.request.POST)
        formset.save()
        return redirect('lesson', self.kwargs['slug'], self.kwargs['lesson_slug'])


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


class InfoView(DetailView):
    model = Courses
    template_name = 'courses/course-info.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(InfoView, self).get_context_data(**kwargs)
        course = Courses.objects.filter(id=self.kwargs['pk']).first()
        ctx['title'] = course.title
        ctx['course'] = course
        return ctx


def payment_view(request, course):
    print(request.user.id)
    print(course)
    return redirect('home')