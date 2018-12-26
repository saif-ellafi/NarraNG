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
        'project_id': project_id,
        'project_name': Common.load_projects()[project_id].name,
        'project_entries': Narrator.load_entries(project_id)
    }
    return HttpResponse(template.render(context, request))


def entry(request, project_id, entry_id):
    template = loader.get_template('ngnarrator/entry.html')
    context = {
        'entry_node': Narrator.load_entries(project_id)[entry_id].node
    }
    return HttpResponse(template.render(context, request))


def new_entry(request, project_id, entry_name):
    template = loader.get_template('ngnarrator/entry.html')
    loaded_project = Common.load_projects()[project_id].name
    new_node = Narrator(loaded_project, name=entry_name)
    new_node._gen(auto=True)
    context = {
        'entry_node': new_node.output_node_root
    }
    return HttpResponse(template.render(context, request))
