from django.urls import path
from . import views

urlpatterns = [
    path('',                           views.artigos_list_view,   name='artigos'),
    path('novo/',                      views.artigo_novo_view,    name='artigo_novo'),
    path('<int:artigo_id>/',           views.artigo_detail_view,  name='artigo_detail'),
    path('<int:artigo_id>/like/',      views.artigo_like_view,    name='artigo_like'),
    path('<int:artigo_id>/edita/',     views.artigo_edita_view,   name='artigo_edita'),
    path('<int:artigo_id>/apaga/',     views.artigo_apaga_view,   name='artigo_apaga'),
]