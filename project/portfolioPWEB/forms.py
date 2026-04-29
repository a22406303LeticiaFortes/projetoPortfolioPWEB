from django import forms
from .models import Projeto, Tecnologia, Competencia, Formacao


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = "__all__"
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "conceitos_aplicados": forms.Textarea(attrs={"rows": 3}),
            "tecnologias_resumo": forms.Textarea(attrs={"rows": 3}),
        }


class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = "__all__"
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }


class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = "__all__"
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }


class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = "__all__"