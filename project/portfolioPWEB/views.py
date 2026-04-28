from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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

from .forms import ProjetoForm, TecnologiaForm, CompetenciaForm, FormacaoForm


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
    projetos = Projeto.objects.select_related("uc").prefetch_related(
        "tecnologias", "competencias", "makingofs"
    ).all()
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


# CRUD PROJETOS

@login_required
def novo_projeto_view(request):
    form = ProjetoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("projetos")

    return render(request, "portfolioPWEB/novo_projeto.html", {"form": form})


@login_required
def edita_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)

    if form.is_valid():
        form.save()
        return redirect("projetos")

    return render(request, "portfolioPWEB/edita_projeto.html", {
        "form": form,
        "projeto": projeto,
    })


@login_required
def apaga_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    projeto.delete()
    return redirect("projetos")


# CRUD TECNOLOGIAS

@login_required
def nova_tecnologia_view(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("tecnologias")

    return render(request, "portfolioPWEB/nova_tecnologia.html", {"form": form})


@login_required
def edita_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tecnologia)

    if form.is_valid():
        form.save()
        return redirect("tecnologias")

    return render(request, "portfolioPWEB/edita_tecnologia.html", {
        "form": form,
        "tecnologia": tecnologia,
    })


@login_required
def apaga_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)
    tecnologia.delete()
    return redirect("tecnologias")


# CRUD COMPETÊNCIAS

@login_required
def nova_competencia_view(request):
    form = CompetenciaForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("competencias")

    return render(request, "portfolioPWEB/nova_competencia.html", {"form": form})


@login_required
def edita_competencia_view(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)
    form = CompetenciaForm(request.POST or None, request.FILES or None, instance=competencia)

    if form.is_valid():
        form.save()
        return redirect("competencias")

    return render(request, "portfolioPWEB/edita_competencia.html", {
        "form": form,
        "competencia": competencia,
    })


@login_required
def apaga_competencia_view(request, competencia_id):
    competencia = Competencia.objects.get(id=competencia_id)
    competencia.delete()
    return redirect("competencias")


# CRUD FORMAÇÕES

@login_required
def nova_formacao_view(request):
    form = FormacaoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("formacoes")

    return render(request, "portfolioPWEB/nova_formacao.html", {"form": form})


@login_required
def edita_formacao_view(request, formacao_id):
    formacao = Formacao.objects.get(id=formacao_id)
    form = FormacaoForm(request.POST or None, request.FILES or None, instance=formacao)

    if form.is_valid():
        form.save()
        return redirect("formacoes")

    return render(request, "portfolioPWEB/edita_formacao.html", {
        "form": form,
        "formacao": formacao,
    })


@login_required
def apaga_formacao_view(request, formacao_id):
    formacao = Formacao.objects.get(id=formacao_id)
    formacao.delete()
    return redirect("formacoes")