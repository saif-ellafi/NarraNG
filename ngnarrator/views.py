from django.http import HttpResponse
from django.template import loader

from narrator import Narrator
from common import Common


def index(request):
    template = loader.get_template('ngnarrator/index.html')
    context = {
        'projects_list': Common.load_projects(),
    }
    return HttpResponse(template.render(context, request))


def project(request, project_id):
    template = loader.get_template('ngnarrator/project.html')
    context = {
        'project_entries': Narrator.load_entries(project_id)
    }
    return HttpResponse(template.render(context, request))
