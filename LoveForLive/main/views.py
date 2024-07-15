from django.shortcuts import render, redirect
from .forms import ConsultationForm
from .models import Articles, Receipts,RequestConsultation
from .services import open_file
from django.views.generic import ListView, DetailView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse
from LoveForLive.settings import TERMINAL_KEY, TERMINAL_PASSWORD
import hashlib
import requests


def home_page_views(request):
    return render(request, 'main/home.html', {'title': 'LoveForLive'})


def consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'age': form.cleaned_data['age'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'country': form.cleaned_data['country']
            }
            html_body = render_to_string("email_templates/request_email.html", data)
            msg = EmailMultiAlternatives(subject='Заявка на консультацию', to=['info_loveforlive@mail.ru',])
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            form.save()
            price = 300000
            order = str(RequestConsultation.objects.all().order_by('-pk')[0].id)
            values = {
                'Amount': str(price),
                'Description': 'Индивидуальная консультация',
                'FailURL': str(request.scheme + '://' + request.get_host() + '/fail_cons_pay'),
                "Language": "ru",
                'NotificationURL': str(
                    request.scheme + '://' + request.get_host() + '/consultation'),
                'OrderId': order,
                'Password': str(TERMINAL_PASSWORD),
                "PayType": "O",
                "Recurrent": "N",
                'SuccessURL': str(request.scheme + '://' + request.get_host() + '/success_cons_pay/'+str(order)),
                'TerminalKey': str(TERMINAL_KEY),
            }
            concatenated_values = ''.join([values[key] for key in (values.keys())])
            hash_object = hashlib.sha256(concatenated_values.encode('utf-8'))
            token = hash_object.hexdigest()
            payment_data = {
                'TerminalKey': str(TERMINAL_KEY),
                'OrderId': order,
                'Amount': str(price),
                "Description": 'Индивидуальная консультация',
                "Language": "ru",
                "PayType": "O",
                "Recurrent": "N",
                'Token': token,
                'DATA': {
                    "Phone": str(data['phone']),
                    'Email': str(data['email']),
                },
                'Receipt': {
                    'Email': str(data['email']),
                    'Phone': str(data['phone']),
                    'Taxation': 'osn',
                    'Items': [{
                        'Name': 'Индивидуальная консультация',
                        'Price': str(price),
                        'Quantity': 1,
                        'Amount': str(price),
                        'Tax': 'none',
                    }, ]
                },
                'SuccessURL': str(request.scheme + '://' + request.get_host() + '/success_cons_pay/'+str(order)),
                'NotificationURL': str(
                    request.scheme + '://' + request.get_host() + '/consultation'),
                'FailURL': str(request.scheme + '://' + request.get_host() + '/fail_cons_pay'),
            }

            url = 'https://securepay.tinkoff.ru/v2/Init'
            response = requests.post(url, json=payment_data)
            print(response.json())
            if response.json()['Success']:
                payment_url = response.json()['PaymentURL']
                RequestConsultation.objects.filter(id=int(order)).update(payment_id=str(response.json()['PaymentId']), pay_sum=price/100)

                # отправляем пользователя на платёжную форму
                return redirect(payment_url)
    form = ConsultationForm(request.POST)
    return render(request, 'main/consultation.html', {'title': 'Консультация', 'form': form})


def check_order(order_id):
    url = "https://securepay.tinkoff.ru/v2/CheckOrder"
    values = {
        'OrderId': str(order_id),
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


def success_cons_pay(request, pk):
    if check_order(pk):
        RequestConsultation.objects.filter(id=int(pk)).update(pay_status=True)
        return render(request, 'main/success_cons_pay.html')
    else:
        return redirect('fail_cons_pay')


def fail_cons_pay(request):
    return render(request, 'main/fail_cons_pay.html')


def contacts_page(request):
    return render(request, 'main/contacts.html', {'title': 'Контакты'})


class ShowAllReceipts(ListView):
    model = Receipts
    template_name = 'main/receipts.html'
    context_object_name = 'receipts'
    ordering = ['-date']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        ctx = super(ShowAllReceipts, self).get_context_data(**kwargs)
        ctx['title'] = 'Рецепты'
        return ctx


class ShowReceiptDetail(DetailView):
    model = Receipts
    template_name = 'main/receipt_detail.html'
    context_object_name = 'receipt'


class ShowAllArticles(ListView):
    model = Articles
    template_name = 'main/articles.html'
    context_object_name = 'articles'
    ordering = ['-date']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        ctx = super(ShowAllArticles, self).get_context_data(**kwargs)
        ctx['title'] = 'Статьи'
        return ctx


class ShowArticleDetail(DetailView):
    model = Articles
    template_name = 'main/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        ctx = super(ShowArticleDetail, self).get_context_data(**kwargs)
        ctx['title'] = Articles.objects.get(pk=self.kwargs['pk'])
        return ctx


def get_streaming(request):
    file, status_code, content_length, content_range = open_file(request)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
