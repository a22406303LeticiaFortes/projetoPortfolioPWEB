from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Licenciatura, UnidadeCurricular, Docente, Projeto,
    Tecnologia, TFC, Competencia, Formacao, MakingOf, AreaDeInteresse
)


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'faculdade', 'creditos', 'semestres')
    search_fields = ('nome', 'faculdade')


from django.contrib import admin
from django.utils.html import format_html

@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('imagem_preview', 'codigo_uc', 'nome', 'get_licenciaturas', 'ano_curricular', 'semestre', 'creditos')
    list_filter = ('ano_curricular', 'semestre')
    search_fields = ('codigo_uc', 'nome', 'descricao', 'objetivos', 'programa', 'metodologia', 'avaliacao')
    filter_horizontal = ('licenciaturas', 'docentes', 'competencias', 'tecnologias')

    fieldsets = (
        ('Informação Geral', {'fields': ('codigo_uc', 'nome', 'ano_curricular', 'semestre', 'creditos', 'licenciaturas')}),
        ('Conteúdo da UC', {'fields': ('descricao', 'objetivos', 'programa', 'metodologia', 'avaliacao')}),
        ('Media e Ligação', {'fields': ('imagem', 'link_uc')}),
        ('Relações', {'fields': ('docentes', 'competencias', 'tecnologias')}),
    )

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.imagem.url)
        return "-"

    imagem_preview.short_description = 'Imagem'

    def get_licenciaturas(self, obj):
        return ", ".join([l.nome for l in obj.licenciaturas.all()])
    get_licenciaturas.short_description = 'Licenciaturas'

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'pagina_pessoal')
    search_fields = ('nome', 'email')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('preview_imagem','titulo', 'ano', 'uc')
    list_filter = ('ano', 'uc')
    search_fields = ('titulo', 'descricao', 'conceitos_aplicados')
    filter_horizontal = ('tecnologias', 'competencias')

    fieldsets = (
        ('Informação Geral', {'fields': ('titulo', 'descricao', 'conceitos_aplicados', 'ano', 'uc')}),
        ('Media e Links', {'fields': ('imagem', 'preview_imagem', 'video_demo', 'github')}),
        ('Relações', {'fields': ('tecnologias', 'competencias')}),
    )

    readonly_fields = ('preview_imagem',)

    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="max-height: 120px; max-width: 200px;" />', obj.imagem.url)
        return "Sem imagem"

    preview_imagem.short_description = 'Imagem'



@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'nome', 'tipo', 'nivel_conhecimento', 'nivel_interesse')
    list_filter = ('tipo',)
    search_fields = ('nome', 'tipo', 'descricao')
    filter_horizontal = ('competencias',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height: 35px; width: auto; border-radius: 4px;" />',
                obj.logo.url
            )
        return "-"

    logo_preview.short_description = "Logo"


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano', 'nivel_interesse', 'licenciatura')
    list_filter = ('ano', 'licenciatura')
    search_fields = ('titulo', 'autores', 'descricao')
    filter_horizontal = ('tecnologias', 'competencias', 'orientadores')


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nivel')
    list_filter = ('tipo', 'nivel')
    search_fields = ('nome', 'descricao')


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'tipo', 'data_inicio', 'data_fim')
    list_filter = ('tipo', 'instituicao')
    search_fields = ('nome', 'instituicao')
    filter_horizontal = ('competencias',)


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'etapas')
    search_fields = ('projeto__titulo', 'decisoes', 'justificacao')

    fields = ('projeto', 'etapas', 'registo1', 'registo2','decisoes', 'erros_encontrados', 'correcoes', 'justificacao', 'uso_ia')


@admin.register(AreaDeInteresse)
class AreaDeInteresseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')
    filter_horizontal = ('competencias',)