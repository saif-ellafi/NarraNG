from django.urls import path

from . import views
import ngnarrator.shadowrun.views as sr_views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:project_id>/<int:entry_id>/', views.entry, name='entry'),
    path('<int:project_id>/new/', views.new_entry, name='new_entry'),
    path('<int:project_id>/save_entry', views.save_entry, name='save_entry'),

    path('shadowrun/initiative', sr_views.initiative, name='sr_initiative')
]
