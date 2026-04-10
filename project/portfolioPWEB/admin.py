from django.contrib import admin

from .models import (
    Licenciatura, UnidadeCurricular, Docente, Projeto,
    Tecnologia, TFC, Competencia, Formacao, MakingOf, AreaDeInteresse
)


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'faculdade', 'creditos', 'semestres')
    search_fields = ('nome', 'faculdade')


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano_curricular', 'creditos', 'licenciatura')
    list_filter = ('ano_curricular', 'licenciatura')
    search_fields = ('nome',)


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'email')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano', 'uc')
    list_filter = ('ano', 'uc')
    search_fields = ('titulo', 'descricao')


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel_conhecimento', 'nivel_interesse')
    list_filter = ('tipo',)
    search_fields = ('nome', 'tipo')


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano', 'nivel_interesse', 'licenciatura')
    list_filter = ('ano', 'licenciatura')
    search_fields = ('titulo', 'autores')


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel')
    list_filter = ('tipo', 'nivel')
    search_fields = ('nome',)


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'tipo', 'data_inicio', 'data_fim')
    list_filter = ('tipo', 'instituicao')
    search_fields = ('nome', 'instituicao')


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ('projeto',)
    search_fields = ('projeto__titulo',)


@admin.register(AreaDeInteresse)
class AreaDeInteresseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome',)
