from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Courses, Allowance, Lesson, Tasks, LessonProgress, Dossing, Order, Promo
from .forms import LessonProgressFormSet
from .services import open_file
from django.http import StreamingHttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from LoveForLive.settings import TERMINAL_KEY, TERMINAL_PASSWORD
from profiles.models import Profile
import requests
import hashlib


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
    course = Courses.objects.get(id=course)
    order = Order()
    order.user = request.user
    order.course = course
    order.save()
    profile = Profile.objects.get(user=request.user)
    try:
        promo = Promo.objects.get(promo_code=request.POST["Promo"])
        sale = float(promo.weight)
    except Exception:
        sale = 0
    price = int((int(course.price) * 100) - (int(course.price * 100) * sale))
    Order.objects.filter(id=order.id).update(pay_sum=price/100)
    values = {
        'Amount': str(price),
        'Description': 'Обучающий курс ' + str(course.title),
        'FailURL': str(request.scheme + '://' + request.get_host() + '/courses/fail_pay/'+str(order.id)),
        "Language": "ru",
        'NotificationURL': str(request.scheme + '://' + request.get_host() + '/courses/course-info/' + str(course.id)),
        'OrderId': str(order.id),
        'Password': str(TERMINAL_PASSWORD),
        "PayType": "O",
        "Recurrent": "N",
        'SuccessURL': str(request.scheme + '://' + request.get_host() + '/courses/success_pay/'+str(order.id)),
        'TerminalKey': str(TERMINAL_KEY),
    }

    concatenated_values = ''.join([values[key] for key in (values.keys())])
    hash_object = hashlib.sha256(concatenated_values.encode('utf-8'))
    token = hash_object.hexdigest()
    payment_data = {
        'TerminalKey': str(TERMINAL_KEY),
        'OrderId': str(order.id),
        'Amount': str(price),
        "Description": 'Обучающий курс ' + str(course.title),
        "Language": "ru",
        "PayType": "O",
        "Recurrent": "N",
        'Token': token,
        'DATA': {
            "Phone": str(profile.phone),
            'Email': request.user.email,
        },
        'Receipt': {
            'Email': str(request.user.email),
            'Phone': str(profile.phone),
            'Taxation': 'osn',
            'Items': [{
                'Name': 'Обучающий курс ' + str(course.title),
                'Price': str(price),
                'Quantity': 1,
                'Amount': str(price),
                'Tax': 'none',
            }, ]
        },
        'SuccessURL': str(request.scheme+'://'+request.get_host()+'/courses/success_pay/'+str(order.id)),
        'NotificationURL': str(request.scheme+'://'+request.get_host()+'/courses/course-info/'+str(course.id)),
        'FailURL': str(request.scheme+'://'+request.get_host()+'/courses/fail_pay/'+str(order.id)),
    }

    url = 'https://securepay.tinkoff.ru/v2/Init'
    response = requests.post(url, json=payment_data)
    if response.json()['Success']:
        payment_url = response.json()['PaymentURL']
        Order.objects.filter(id=order.id).update(payment_id=str(response.json()['PaymentId']))

        # отправляем пользователя на платёжную форму
        return redirect(payment_url)


def fail_pay(request, pk):
    order = Order.objects.get(id=pk)
    if not order.pay_status:
        Order.objects.filter(id=pk).delete()
    return render(request, 'courses/fail_payment.html')


def check_order(order):
    url = "https://securepay.tinkoff.ru/v2/CheckOrder"
    values = {
        'OrderId': str(order.id),
        'Password': str(TERMINAL_PASSWORD),
        'TerminalKey': str(TERMINAL_KEY),
    }
    concatenated_values = ''.join([values[key] for key in (values.keys())])
    hash_object = hashlib.sha256(concatenated_values.encode('utf-8'))
    token = hash_object.hexdigest()
    values["Token"] = token
    response = requests.post(url, json=values)
    if response.status_code == requests.codes.ok:
        response_data = response.json()
        if response_data["Success"]:
            if response_data['Payments'][0]["Success"]:
                return True
    return False


def success_pay(request, pk):
    order = Order.objects.get(id=pk)
    if check_order(order):
        Order.objects.filter(id=pk).update(pay_status=True)
        Allowance.objects.filter(user=order.user, course=order.course).update(allow=True)
        link = order.course.slug
        data = {
            'name': order.user.username,
            'course': order.course.title,
            'date': order.date,
            'price': order.pay_sum,
            'payment_id': order.payment_id
        }
        html_body = render_to_string("email_templates/payment_email.html", data)
        msg = EmailMultiAlternatives(subject='Покупка', to=['info_loveforlive@mail.ru', ])
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        return render(request, 'courses/success_payment.html', {'link': link, 'status': True})
    else:
        return render(request, 'courses/success_payment.html', {'status': False})