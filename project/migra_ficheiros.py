import os
from django.conf import settings
from django.core.files import File

from portfolioPWEB.models import Tecnologia, UnidadeCurricular, Projeto, Formacao, MakingOf
from escola.models import Curso
from artigos.models import Artigo


PASTAS_LOCAIS = [
    os.path.join(settings.BASE_DIR, "media"),
    os.path.join(settings.BASE_DIR, "mediafiles"),
]


def encontrar_ficheiro_local(nome_ficheiro):
    for pasta in PASTAS_LOCAIS:
        caminho = os.path.join(pasta, nome_ficheiro)
        if os.path.exists(caminho):
            return caminho
    return None


def migrar_campo(obj, campo_nome, etiqueta):
    ficheiro = getattr(obj, campo_nome)

    if not ficheiro or not ficheiro.name:
        return

    local_path = encontrar_ficheiro_local(ficheiro.name)

    if not local_path:
        print(f"Não encontrado {etiqueta}: {ficheiro.name}")
        return

    with open(local_path, "rb") as f:
        ficheiro.save(
            os.path.basename(local_path),
            File(f),
            save=True
        )

    print(f"Migrado {etiqueta}: {obj}")


for obj in Tecnologia.objects.all():
    migrar_campo(obj, "logo", "Tecnologia.logo")

for obj in UnidadeCurricular.objects.all():
    migrar_campo(obj, "imagem", "UnidadeCurricular.imagem")

for obj in Projeto.objects.all():
    migrar_campo(obj, "imagem", "Projeto.imagem")

for obj in Formacao.objects.all():
    migrar_campo(obj, "logotipo", "Formacao.logotipo")

for obj in MakingOf.objects.all():
    migrar_campo(obj, "registo1", "MakingOf.registo1")
    migrar_campo(obj, "registo2", "MakingOf.registo2")

for obj in Curso.objects.all():
    migrar_campo(obj, "imagem", "Curso.imagem")

for obj in Artigo.objects.all():
    migrar_campo(obj, "fotografia", "Artigo.fotografia")

print("Migração concluída!")