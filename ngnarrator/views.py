from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from narrator import Narrator
from common import Common
from components import LinkNode


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
        'project_entries': Narrator.load_output_entries(project_id)
    }
    return HttpResponse(template.render(context, request))


def entry(request, project_id, entry_id):
    template = loader.get_template('ngnarrator/entry.html')
    context = {
        'entry_node': Narrator.load_output_entries(project_id)[entry_id].node
    }
    return HttpResponse(template.render(context, request))


def create_entry(request, project_id):
    return HttpResponseRedirect(reverse('new_entry', args=(project_id, request.GET['target'])))


def new_entry(request, project_id, entry_name):
    template = loader.get_template('ngnarrator/new_entry.html')
    loaded_project = Common.load_projects()[project_id].name
    new_node = Narrator(loaded_project, name=entry_name)
    new_node._gen(auto=True)
    Common.temp_entry = new_node.output_node_root
    context = {
        'project_id': project_id,
        'entry_node': new_node.output_node_root
    }
    return HttpResponse(template.render(context, request))


def save_entry(request, project_id):
    if isinstance(Common.temp_entry, LinkNode):
        Common.temp_entry.save()
        Common.temp_entry = None
    return HttpResponseRedirect(reverse('project', args=[project_id]))
