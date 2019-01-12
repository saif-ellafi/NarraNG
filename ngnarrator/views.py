from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from narrator import Narrator
from common import Common
from components import LinkNode

from collections import OrderedDict as OrdD
import os


def index(request):
    template = loader.get_template('ngnarrator/index.html')
    projects = Common.load_projects()
    sourced_projects = {}
    for p in projects:
        source = os.path.split(p.source)[0].replace(Common.PROJECTS_FOLDER, '')
        if source in sourced_projects:
            sourced_projects[source].append(p)
        else:
            sourced_projects[source] = [p]
    context = {
        'projects_list': OrdD(sorted(sourced_projects.items(), key=lambda t: t[0])),
    }
    return HttpResponse(template.render(context, request))


def project(request, project_id):
    template = loader.get_template('ngnarrator/project.html')
    context = {
        'project': Common.load_projects()[project_id],
        'project_entries': Narrator.load_output_entries(project_id)
    }
    return HttpResponse(template.render(context, request))


def entry(request, project_id, entry_id):
    template = loader.get_template('ngnarrator/entry.html')
    context = {
        'entry_node': Narrator.load_output_entries(project_id)[entry_id].node
    }
    return HttpResponse(template.render(context, request))


def new_entry(request, project_id):
    template = loader.get_template('ngnarrator/new_entry.html')
    loaded_project = Common.load_projects()[project_id]
    new_node = Narrator(loaded_project.source)
    new_node._gen(auto=True)
    Common.temp_entry = new_node.output_node_root
    Common.temp_entry.name = None
    context = {
        'project': loaded_project,
        'entry_node': Common.temp_entry
    }
    return HttpResponse(template.render(context, request))


def save_entry(request, project_id):
    content = request.GET['target']
    if isinstance(Common.temp_entry, LinkNode):
        Common.temp_entry.name = content
        Common.temp_entry.save()
        Common.temp_entry = None
    return HttpResponseRedirect(reverse('project', args=[project_id]))
