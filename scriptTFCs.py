import os
import sys
import json
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DJANGO_DIR = os.path.join(BASE_DIR, "project")

sys.path.append(DJANGO_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from portfolioPWEB.models import TFC, Licenciatura, Docente

ficheiro_json = os.path.join(BASE_DIR, "data", "tfcs_2025.json")

if not os.path.isfile(ficheiro_json):
    print("Erro: ficheiro não encontrado.")
    raise SystemExit

with open(ficheiro_json, "r", encoding="utf-8") as file:
    registos = json.load(file)

lic, _ = Licenciatura.objects.get_or_create(
    nome="Engenharia Informática",
    defaults={
        "descricao": "Licenciatura em Engenharia Informática",
        "creditos": 180,
        "semestres": 6,
        "formato": "Presencial",
        "website": "https://www.ulusofona.pt",
        "faculdade": "Escola de Engenharia"
    }
)

novos = 0

for reg in registos:
    titulo = reg.get("titulo")

    if not titulo:
        continue

    tfc_obj, is_new = TFC.objects.get_or_create(
        titulo=titulo,
        defaults={
            "autores": reg.get("autor", ""),
            "ano": reg.get("ano", 2025),
            "descricao": reg.get("resumo", ""),
            "link": reg.get("link", ""),
            "nivel_interesse": reg.get("rating", 0),
            "licenciatura": lic,
        }
    )

    orientadores = reg.get("orientador", "")
    lista_nomes = [nome.strip() for nome in orientadores.split(";") if nome.strip()]

    lista_docentes = []
    for nome_doc in lista_nomes:
        docente_obj, _ = Docente.objects.get_or_create(
            nome=nome_doc,
            defaults={
                "email": "sem_email@ulusofona.pt",
                "pagina_pessoal": "https://www.ulusofona.pt"
            }
        )
        lista_docentes.append(docente_obj)

    tfc_obj.orientadores.set(lista_docentes)

    if is_new:
        novos += 1
        print(f"[NOVO] {titulo}")
    else:
        print(f"[EXISTENTE] {titulo}")

print(f"\nForam adicionados {novos} novos registos.")