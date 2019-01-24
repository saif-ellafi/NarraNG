from django.http import HttpResponse
from django.template import loader


def initiative(request):
    template = loader.get_template('ngnarrator/shadowrun/initiative.html')
    context = {}
    return HttpResponse(template.render(context, request))
