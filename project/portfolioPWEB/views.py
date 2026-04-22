from django.shortcuts import render
from .models import (
    Licenciatura,
    Docente,
    Competencia,
    Tecnologia,
    UnidadeCurricular,
    Projeto,
    TFC,
    Formacao,
    MakingOf,
    AreaDeInteresse,
)

def licenciaturas_view(request):
    licenciaturas = Licenciatura.objects.all()
    return render(request, "portfolioPWEB/licenciaturas.html", {"licenciaturas": licenciaturas})


def docentes_view(request):
    docentes = Docente.objects.prefetch_related("ucs", "tfcs_orientados").all()
    return render(request, "portfolioPWEB/docentes.html", {"docentes": docentes})


def competencias_view(request):
    competencias = Competencia.objects.all()
    return render(request, "portfolioPWEB/competencias.html", {"competencias": competencias})


def tecnologias_view(request):
    tecnologias = Tecnologia.objects.prefetch_related("competencias", "ucs", "projetos", "tfcs").all()
    return render(request, "portfolioPWEB/tecnologias.html", {"tecnologias": tecnologias})


def ucs_view(request):
    ucs = UnidadeCurricular.objects.prefetch_related(
        "licenciaturas", "docentes", "competencias", "tecnologias", "projetos"
    ).all()
    return render(request, "portfolioPWEB/ucs.html", {"ucs": ucs})


def projetos_view(request):
    projetos = Projeto.objects.select_related("uc").prefetch_related("tecnologias", "competencias", "makingofs").all()
    return render(request, "portfolioPWEB/projetos.html", {"projetos": projetos})


def tfcs_view(request):
    tfcs = TFC.objects.select_related("licenciatura").prefetch_related(
        "tecnologias", "competencias", "orientadores"
    ).all()
    return render(request, "portfolioPWEB/tfcs.html", {"tfcs": tfcs})


def formacoes_view(request):
    formacoes = Formacao.objects.prefetch_related("competencias").all()
    return render(request, "portfolioPWEB/formacoes.html", {"formacoes": formacoes})


def makingofs_view(request):
    makingofs = MakingOf.objects.select_related("projeto").all()
    return render(request, "portfolioPWEB/makingofs.html", {"makingofs": makingofs})


def areas_view(request):
    areas = AreaDeInteresse.objects.prefetch_related("competencias").all()
    return render(request, "portfolioPWEB/areas.html", {"areas": areas})

def portfolio_home_view(request):
    return render(request, "portfolioPWEB/home.html")