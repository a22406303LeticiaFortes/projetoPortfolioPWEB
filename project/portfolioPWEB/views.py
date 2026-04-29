from django.shortcuts import render, redirect , get_object_or_404
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


def makingof_detalhe_view(request, makingof_id):
    makingof = MakingOf.objects.select_related("projeto").get(id=makingof_id)
    return render(request, "portfolioPWEB/makingof_detalhe.html", {"makingof": makingof})


def areas_view(request):
    areas = AreaDeInteresse.objects.prefetch_related("competencias").all()
    return render(request, "portfolioPWEB/areas.html", {"areas": areas})


def portfolio_home_view(request):
    return render(request, "portfolioPWEB/home.html")


# --- CRUD PROJETOS ---


def novo_projeto_view(request):
    form = ProjetoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("projetos")
    return render(request, "portfolioPWEB/projetoForm.html", {"form": form, "titulo": "Novo Projeto"})


def edita_projeto_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)
    if form.is_valid():
        form.save()
        return redirect("projetos")
    return render(request, "portfolioPWEB/projetoForm.html", {"form": form, "titulo": "Editar Projeto", "projeto": projeto})


def apaga_projeto_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if request.method == "POST":
        projeto.delete()
        return redirect("projetos")
    return render(request, "portfolioPWEB/projetoDelete.html", {"projeto": projeto})


# --- CRUD TECNOLOGIAS ---


def nova_tecnologia_view(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("tecnologias")
    return render(request, "portfolioPWEB/tecnologiaForm.html", {"form": form, "titulo": "Nova Tecnologia"})


def edita_tecnologia_view(request, tecnologia_id):
    tecnologia = get_object_or_404(Tecnologia, id=tecnologia_id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tecnologia)
    if form.is_valid():
        form.save()
        return redirect("tecnologias")
    return render(request, "portfolioPWEB/tecnologiaForm.html", {"form": form, "titulo": "Editar Tecnologia", "tecnologia": tecnologia})


def apaga_tecnologia_view(request, tecnologia_id):
    tecnologia = get_object_or_404(Tecnologia, id=tecnologia_id)
    if request.method == "POST":
        tecnologia.delete()
        return redirect("tecnologias")
    return render(request, "portfolioPWEB/tecnologiaDelete.html", {"tecnologia": tecnologia})


# --- CRUD COMPETÊNCIAS ---


def nova_competencia_view(request):
    form = CompetenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("competencias")
    return render(request, "portfolioPWEB/competenciaForm.html", {"form": form, "titulo": "Nova Competência"})


def edita_competencia_view(request, competencia_id):
    competencia = get_object_or_404(Competencia, id=competencia_id)
    form = CompetenciaForm(request.POST or None, instance=competencia)
    if form.is_valid():
        form.save()
        return redirect("competencias")
    return render(request, "portfolioPWEB/competenciaForm.html", {"form": form, "titulo": "Editar Competência", "competencia": competencia})


def apaga_competencia_view(request, competencia_id):
    competencia = get_object_or_404(Competencia, id=competencia_id)
    if request.method == "POST":
        competencia.delete()
        return redirect("competencias")
    return render(request, "portfolioPWEB/competenciaDelete.html", {"competencia": competencia})


# --- CRUD FORMAÇÕES ---

def nova_formacao_view(request):
    form = FormacaoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("formacoes")
    return render(request, "portfolioPWEB/formacaoForm.html", {"form": form, "titulo": "Nova Formação"})

def edita_formacao_view(request, formacao_id):
    formacao = get_object_or_404(Formacao, id=formacao_id)
    form = FormacaoForm(request.POST or None, request.FILES or None, instance=formacao)
    if form.is_valid():
        form.save()
        return redirect("formacoes")
    return render(request, "portfolioPWEB/formacaoForm.html", {"form": form, "titulo": "Editar Formação", "formacao": formacao})


def apaga_formacao_view(request, formacao_id):
    formacao = get_object_or_404(Formacao, id=formacao_id)
    if request.method == "POST":
        formacao.delete()
        return redirect("formacoes")
    return render(request, "portfolioPWEB/formacaoDelete.html", {"formacao": formacao})