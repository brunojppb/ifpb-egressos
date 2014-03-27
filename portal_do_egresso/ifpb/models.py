from django.db import models
from django.contrib.auth.models import User

"""
Choices
"""

CLASSIFICACAO_CHOICE = (
    ('micro', 'Micro Empresa'),
    ('pequena', 'Pequeno Porte'),
    ('media', 'Media Empresa'),
    ('artesao', 'Artesao'),
    ('rural', 'Pordutor Rural'),
    ('individual', 'Empreendedor Individual')
)

def content_file_name(instance, filename):
    """Funcao auxiliar para gerenciar os path das imagens dos usuarios"""
    return '/'.join(['content', instance.user.username, filename])

"""
Modelos que se relacionarao com o usuario do sistema
"""
class Aluno(models.Model):
    user =              models.OneToOneField(User, unique=True, related_name='aluno')
    abreviacao =        models.CharField(max_length=20, blank=True)
    lattes =            models.URLField(max_length=100, blank=True)
    rua_av =            models.CharField(max_length=120, blank=True)
    bairro =            models.CharField(max_length=40, blank=True)
    cep =               models.CharField(max_length=10, blank=True)
    cidade =            models.CharField(max_length=80, blank=True)
    estado =            models.CharField(max_length=2, blank=True)
    sexo =              models.CharField(max_length=2, blank=True)
    foto =              models.ImageField(upload_to=content_file_name, blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

class Telefone(models.Model):
    aluno =             models.ForeignKey(Aluno)
    ddd =               models.CharField(max_length=2, blank=False)
    numero =            models.CharField(max_length=9, blank=False)

    def __unicode__(self):
        return '(%s) %s' %(self.ddd, self.numero)

class Autonomo(models.Model):
    aluno =             models.ForeignKey(Aluno)
    titulo =            models.CharField(max_length=30, blank=False)
    descricao =         models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return '%s' %(self.titulo)

class Area(models.Model):
    descricao =         models.CharField(max_length=80, blank=False)
    abreviacao =        models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return '%s' %(self.descricao)

class FuturoEmpreendedor(models.Model):
    aluno =             models.ForeignKey(Aluno)
    area =              models.ForeignKey(Area)

    def __unicode__(self):
        return '%s' %(self.aluno)

class Consultor(models.Model):
    aluno =             models.ForeignKey(Aluno)
    area =              models.ForeignKey(Area)
    descricao =         models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return '%s' % (self.descricao)

class Instituicao(models.Model):
    descricao =         models.CharField(max_length=80, blank=False)
    abreviacao =        models.CharField(max_length=20)
    inicio =            models.DateTimeField()
    fim =               models.DateTimeField()
    validado =          models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' %(self.descricao)

class Nivel(models.Model):
    descricao =         models.CharField(max_length=20)

    def __unicode__(self):
        return '%s' %(self.descricao)

class Modalidade(models.Model):
    nivel =             models.ForeignKey(Nivel)
    descricao =         models.CharField(max_length=80, blank=False)
    abreviacao =        models.CharField(max_length=80, blank=True)

    def __unicode__(self):
        return '%s' %(self.descricao)

class Curso(models.Model):
    instituicao =       models.ForeignKey(Instituicao)
    modalidade =        models.ForeignKey(Modalidade)
    area =              models.ForeignKey(Area)
    descricao =         models.CharField(max_length=80, blank=False)
    abreviacao =        models.CharField(max_length=80, blank=True)
    validado =          models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' %(self.descricao)

class Matricula(models.Model):
    aluno =             models.ForeignKey(Aluno)
    curso =             models.ForeignKey(Curso)
    matricula =         models.CharField(max_length=20, blank=False, unique=True)
    ano_inicio =        models.IntegerField(max_length=4)
    ano_fim =           models.IntegerField(max_length=4)
    semestre_inicio =   models.IntegerField(max_length=4)
    semestre_fim =      models.IntegerField(max_length=4)
    diploma =           models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' %(self.matricula)

class Tcc(models.Model):
    matricula =         models.ForeignKey(Matricula)
    titulo =            models.CharField(max_length=20, blank=False)

    def __unicode__(self):
        return '%s' %(self.titulo)

class EstagioSupervisionado(models.Model):
    matricula =         models.ForeignKey(Matricula)
    lugar =             models.CharField(max_length=80, blank=False)
    funcao =            models.CharField(max_length=80, blank=False)

    def __unicode__(self):
        return '%s' %(self.funcao)

class Classificacao(models.Model):
    descricao =         models.CharField(max_length=80, blank=False, choices=CLASSIFICACAO_CHOICE)

    def __unicode__(self):
        return '%s' %(self.descricao)

class Empresa(models.Model):
    classificacao =     models.ForeignKey(Classificacao)
    nome =              models.CharField(max_length=80, blank=True)
    descricao =         models.CharField(max_length=80, blank=False)
    abrevicao =         models.CharField(max_length=80, blank=True)
    cnpj =              models.BigIntegerField()
    site =              models.URLField(max_length=200)
    email =             models.EmailField()
    rua_av =            models.CharField(max_length=120)
    bairro =            models.CharField(max_length=40)
    cep =               models.CharField(max_length=10)
    cidade =            models.CharField(max_length=80)
    estado =            models.CharField(max_length=2)
    telefone =          models.CharField(max_length=14)

    def __unicode__(self):
        return '%s' %(self.nome)

class Vinculo(models.Model):
    empresa =           models.ForeignKey(Empresa)
    aluno =             models.ForeignKey(Aluno)
    funcao =            models.CharField(max_length=80, blank=False)
    inicio =            models.DateTimeField()
    fim =               models.DateTimeField()
    proprietario =      models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' %(self.funcao)

class Tipo(models.Model):
    descricao =         models.CharField(max_length=80, blank=False)

    def __unicode__(self):
        return '%s' %(self.descricao)

class Oferta(models.Model):
    empresa =           models.ForeignKey(Empresa)
    tipo =              models.ForeignKey(Tipo)
    titulo =            models.CharField(max_length=80, blank=False)
    descricao =         models.CharField(max_length=80, blank=False)

    def __unicode__(self):
        return '%s' %(self.titulo)