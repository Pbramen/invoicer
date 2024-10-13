from django.shortcuts import render


def index(request):
    template_name= 'invoicer/index.html'
    if not request.htmx:
        print('request.htmx not found... returning complete')
        template_name= 'invoicer/base.html'
    return render(request, template_name, {})
