from django.db import models

# Create your models here.


class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    creditos = models.IntegerField()
    semestres = models.IntegerField()
    formato = models.CharField(max_length=50)
    website = models.URLField()
    faculdade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Docente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    pagina_pessoal = models.URLField()

    def __str__(self):
        return self.nome


class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    descricao = models.TextField()
    nivel = models.IntegerField()

    def __str__(self):
        return self.nome


class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='tecnologias/')
    website = models.URLField()
    nivel_conhecimento = models.IntegerField()
    nivel_interesse = models.IntegerField()
    competencias = models.ManyToManyField(Competencia, related_name='tecnologias', blank=True)

    def __str__(self):
        return self.nome


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    ano_curricular = models.IntegerField()
    creditos = models.IntegerField()
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='ucs/')
    link_UC = models.URLField()
    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name='ucs'
    )
    docentes = models.ManyToManyField(Docente, related_name='ucs', blank=True)
    competencias = models.ManyToManyField(Competencia, related_name='ucs', blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, related_name='ucs', blank=True)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField()
    tecnologias_resumo = models.TextField()
    ano = models.IntegerField()
    imagem = models.ImageField(upload_to='projetos/')
    video_demo = models.URLField(blank=True, null=True)
    github = models.URLField()
    uc = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name='projetos'
    )
    tecnologias = models.ManyToManyField(Tecnologia, related_name='projetos', blank=True)
    competencias = models.ManyToManyField(Competencia, related_name='projetos', blank=True)

    def __str__(self):
        return self.titulo


class TFC(models.Model):
    titulo = models.CharField(max_length=150)
    autores = models.CharField(max_length=150)
    orientadores = models.CharField(max_length=150)
    ano = models.IntegerField()
    descricao = models.TextField()
    link = models.URLField()
    nivel_interesse = models.IntegerField()
    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name='tfcs'
    )
    tecnologias = models.ManyToManyField(Tecnologia, related_name='tfcs', blank=True)
    competencias = models.ManyToManyField(Competencia, related_name='tfcs', blank=True)

    def __str__(self):
        return self.titulo


class Formacao(models.Model):
    nome = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    logotipo = models.ImageField(upload_to='formacoes/')
    competencias = models.ManyToManyField(Competencia, related_name='formacoes', blank=True)

    def __str__(self):
        return self.nome


class MakingOf(models.Model):
    registos = models.TextField()
    etapas = models.TextField()
    decisoes = models.TextField()
    erros_encontrados = models.TextField()
    correcoes = models.TextField()
    justificacao = models.TextField()
    uso_IA = models.TextField()
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='makingofs'
    )

    def __str__(self):
        return f"MakingOf - {self.projeto.titulo}"


class AreaDeInteresse(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50)
    competencias = models.ManyToManyField(Competencia, related_name='areas_interesse', blank=True)

    def __str__(self):
        return self.nome