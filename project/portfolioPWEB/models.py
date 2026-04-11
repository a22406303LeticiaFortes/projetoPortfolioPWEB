from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    creditos = models.IntegerField()
    semestres = models.IntegerField()
    formato = models.CharField(max_length=50)
    website = models.URLField()
    faculdade = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Licenciatura"
        verbose_name_plural = "Licenciaturas"

    def __str__(self):
        return self.nome


class Docente(models.Model):
    codigo_docente = models.CharField(max_length=30, unique=True, blank=True, null=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    pagina_pessoal = models.URLField(blank=True)

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

    def __str__(self):
        return self.nome


class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    descricao = models.TextField()
    nivel = models.IntegerField()

    class Meta:
        verbose_name = "Competência"
        verbose_name_plural = "Competências"

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
    competencias = models.ManyToManyField(
        Competencia,
        related_name='tecnologias',
        blank=True
    )

    class Meta:
        verbose_name = "Tecnologia"
        verbose_name_plural = "Tecnologias"

    def __str__(self):
        return self.nome


class UnidadeCurricular(models.Model):
    codigo_uc = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=100)
    ano_curricular = models.IntegerField()
    semestre = models.IntegerField(null=True, blank=True)
    creditos = models.IntegerField()
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True)
    link_uc = models.URLField(blank=True)
    metodologia = models.TextField(blank=True)
    objetivos = models.TextField(blank=True)
    programa = models.TextField(blank=True)
    avaliacao = models.TextField(blank=True)

    licenciaturas = models.ManyToManyField(Licenciatura, related_name='unidades_curriculares', blank=True )
    docentes = models.ManyToManyField(Docente,related_name='ucs',blank=True)
    competencias = models.ManyToManyField(Competencia,related_name='ucs',blank=True)
    tecnologias = models.ManyToManyField(Tecnologia,related_name='ucs',blank=True )

    class Meta:
        verbose_name = "Unidade Curricular"
        verbose_name_plural = "Unidades Curriculares"

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField()
    tecnologias_resumo = models.TextField()
    ano = models.IntegerField()
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_demo = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    uc = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name='projetos'
    )
    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='projetos',
        blank=True
    )
    competencias = models.ManyToManyField(
        Competencia,
        related_name='projetos',
        blank=True
    )

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return self.titulo


class TFC(models.Model):
    titulo = models.CharField(max_length=150)
    autores = models.CharField(max_length=150)
    ano = models.IntegerField()
    descricao = models.TextField()
    link = models.URLField()
    nivel_interesse = models.IntegerField()

    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name='tfcs'
    )
    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='tfcs',
        blank=True
    )
    competencias = models.ManyToManyField(
        Competencia,
        related_name='tfcs',
        blank=True
    )
    orientadores = models.ManyToManyField(
        Docente,
        related_name='tfcs_orientados',
        blank=True
    )

    class Meta:
        verbose_name = "TFC"
        verbose_name_plural = "TFCs"

    def __str__(self):
        return self.titulo


class Formacao(models.Model):
    nome = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    logotipo = models.ImageField(upload_to='formacoes/')
    competencias = models.ManyToManyField(
        Competencia,
        related_name='formacoes',
        blank=True
    )

    class Meta:
        verbose_name = "Formação"
        verbose_name_plural = "Formações"

    def __str__(self):
        return self.nome

class MakingOf(models.Model):
    registo1 = models.FileField(upload_to='makingof/', blank=True, null=True)
    registo2 = models.FileField(upload_to='makingof/', blank=True, null=True)
    etapas = models.CharField(max_length=100)
    decisoes = models.TextField()
    erros_encontrados = models.TextField()
    correcoes = models.TextField()
    justificacao = models.TextField()
    uso_ia = models.TextField()

    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='makingofs'
    )

    class Meta:
        verbose_name = "Making Of"
        verbose_name_plural = "Making Of"

    def __str__(self):
        return f"MakingOf - {self.projeto.titulo}"


class AreaDeInteresse(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50)
    competencias = models.ManyToManyField(
        Competencia,
        related_name='areas_interesse',
        blank=True
    )

    class Meta:
        verbose_name = "Área de Interesse"
        verbose_name_plural = "Áreas de Interesse"

    def __str__(self):
        return self.nome