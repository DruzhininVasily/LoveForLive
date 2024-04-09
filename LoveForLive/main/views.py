from django.shortcuts import render, redirect
from .forms import ConsultationForm
from .models import Articles
from .services import open_file
from django.views.generic import ListView, DetailView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse


def home_page_views(request):
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
            msg = EmailMultiAlternatives(subject='Заявка на консультацию', to=['druzhinin-91@bk.ru',])
            msg.attach_alternative(html_body, "text/html")
            msg.send()
            form.save()
            return redirect('home')
    form = ConsultationForm(request.POST)
    return render(request, 'main/home.html', {'title': 'LoveForLive', 'form': form})


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
