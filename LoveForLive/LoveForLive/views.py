from django.shortcuts import render


def get_politic(request):
    return render(request, 'politic.html')

