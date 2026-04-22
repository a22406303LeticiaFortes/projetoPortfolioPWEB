from django.urls import path
from . import views

urlpatterns = [
    path("", views.portfolio_home_view, name="portfolio_home"),
    path("licenciaturas/", views.licenciaturas_view, name="licenciaturas"),
    path("docentes/", views.docentes_view, name="docentes"),
    path("competencias/", views.competencias_view, name="competencias"),
    path("tecnologias/", views.tecnologias_view, name="tecnologias"),
    path("ucs/", views.ucs_view, name="ucs"),
    path("projetos/", views.projetos_view, name="projetos"),
    path("tfcs/", views.tfcs_view, name="tfcs"),
    path("formacoes/", views.formacoes_view, name="formacoes"),
    path("makingofs/", views.makingofs_view, name="makingofs"),
    path("areas/", views.areas_view, name="areas"),
]