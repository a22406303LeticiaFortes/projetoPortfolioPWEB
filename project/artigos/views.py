from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artigo, Like, Comentario
from .forms import ArtigoForm, ComentarioForm


# ── Lista de artigos (público) ─────────────────────────────────────────────────
def artigos_list_view(request):
    artigos = Artigo.objects.select_related('autor').all()
    return render(request, 'artigos/artigos.html', {'artigos': artigos})


# ── Detalhe de artigo (público) + comentários + like ──────────────────────────
def artigo_detail_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)
    comentarios = artigo.comentarios.select_related('autor').all()
    form_comentario = ComentarioForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            c = form_comentario.save(commit=False)
            c.artigo = artigo
            c.autor  = request.user
            c.save()
            return redirect('artigo_detail', artigo_id=artigo.pk)

    context = {
        'artigo':          artigo,
        'comentarios':     comentarios,
        'form_comentario': form_comentario,
    }
    return render(request, 'artigos/artigo_detail.html', context)


# ── Like (qualquer pessoa) ─────────────────────────────────────────────────────
def artigo_like_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)
    ip = request.META.get('REMOTE_ADDR')

    if request.user.is_authenticated:
        like, criado = Like.objects.get_or_create(artigo=artigo, utilizador=request.user)
        if not criado:
            like.delete()  # toggle: remove se já existia
    else:
        like, criado = Like.objects.get_or_create(artigo=artigo, ip=ip)
        if not criado:
            like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'artigos'))


# ── Criar artigo (só autores) ──────────────────────────────────────────────────
@login_required(login_url='login')
def artigo_novo_view(request):
    if not request.user.groups.filter(name='autores').exists():
        messages.error(request, 'Não tens permissão para criar artigos.')
        return redirect('artigos')

    form = ArtigoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        messages.success(request, 'Artigo publicado!')
        return redirect('artigo_detail', artigo_id=artigo.pk)

    return render(request, 'artigos/artigo_form.html', {'form': form, 'titulo': 'Novo Artigo'})


# ── Editar artigo (só o próprio autor) ────────────────────────────────────────
@login_required(login_url='login')
def artigo_edita_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)

    if artigo.autor != request.user:
        messages.error(request, 'Só podes editar os teus próprios artigos.')
        return redirect('artigo_detail', artigo_id=artigo.pk)

    form = ArtigoForm(request.POST or None, request.FILES or None, instance=artigo)
    if form.is_valid():
        form.save()
        messages.success(request, 'Artigo atualizado!')
        return redirect('artigo_detail', artigo_id=artigo.pk)

    return render(request, 'artigos/artigo_form.html', {'form': form, 'titulo': 'Editar Artigo'})


# ── Apagar artigo (só o próprio autor) ────────────────────────────────────────
@login_required(login_url='login')
def artigo_apaga_view(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)

    if artigo.autor != request.user:
        messages.error(request, 'Só podes apagar os teus próprios artigos.')
        return redirect('artigo_detail', artigo_id=artigo.pk)

    if request.method == 'POST':
        artigo.delete()
        messages.success(request, 'Artigo apagado.')
        return redirect('artigos')

    return render(request, 'artigos/artigo_delete.html', {'artigo': artigo})