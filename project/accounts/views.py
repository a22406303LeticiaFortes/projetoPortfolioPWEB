
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import secrets

from .forms import RegistoForm, LoginForm, MagicLinkForm


# ── Login por username & password ─────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('portfolio_home')

    form_login     = LoginForm(request.POST or None)
    form_magic     = MagicLinkForm()
    magic_enviado  = False

    if request.method == 'POST':
        if 'login_password' in request.POST:
            # Formulário de login normal
            form_login = LoginForm(request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data['username']
                password = form_login.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    next_url = request.GET.get('next', 'portfolio_home')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Username ou password incorretos.')

        elif 'magic_link' in request.POST:
            # Formulário de magic link
            form_magic = MagicLinkForm(request.POST)
            if form_magic.is_valid():
                email = form_magic.cleaned_data['email']
                try:
                    user = User.objects.get(email=email)
                    # Gera token e guarda na sessão
                    token = secrets.token_urlsafe(32)
                    request.session[f'magic_token_{user.pk}'] = token
                    # Envia email
                    host = request.get_host()
                    if 'localhost' in host or '127.0.0.1' in host:
                        host = 'musical-acorn-jjgj6rggjr6p3px9-8000.app.github.dev'
                    link = f"https://{host}/accounts/magic/{user.pk}/{token}/"
                    send_mail(
                        subject='Portfólio — Acesso por link mágico',
                        message=f'Olá {user.first_name or user.username},\n\nClica no link para entrar:\n{link}\n\nO link expira quando fechares o browser.',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=True,
                    )
                    magic_enviado = True
                    messages.success(request, f'Link enviado para {email}!')
                except User.DoesNotExist:
                    messages.error(request, 'Não existe nenhuma conta com esse email.')

    context = {
        'form_login':    form_login,
        'form_magic':    form_magic,
        'magic_enviado': magic_enviado,
    }
    return render(request, 'accounts/login.html', context)


# ── Magic link — validação ─────────────────────────────────────────────────────
def magic_link_view(request, user_pk, token):
    session_token = request.session.get(f'magic_token_{user_pk}')
    if session_token and session_token == token:
        try:
            user = User.objects.get(pk=user_pk)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            del request.session[f'magic_token_{user_pk}']
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            return redirect('portfolio_home')
        except User.DoesNotExist:
            pass
    messages.error(request, 'Link inválido ou expirado.')
    return redirect('login')


# ── Logout ────────────────────────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('portfolio_home')


# ── Registo ───────────────────────────────────────────────────────────────────
def registo_view(request):
    if request.user.is_authenticated:
        return redirect('portfolio_home')

    form = RegistoForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        # Adiciona ao grupo 'autores' automaticamente (para artigos)
        grupo, _ = Group.objects.get_or_create(name='autores')
        user.groups.add(grupo)
        login(request, user)
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('portfolio_home')

    return render(request, 'accounts/registo.html', {'form': form})