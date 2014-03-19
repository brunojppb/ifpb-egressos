from django.db import models
from django.contrib.auth.models import User

#MODIFICA A ESTRUTURA ORIGINAL DO DJANGO
"""
Para usarmos a funcionalidade de autenticacao do Django
precisamos adicionar atributos a Classe User do Django
Onde essa classe sera o nosso EGRESSO
"""
User.add_to_class('telefone', models.CharField(max_length=50, blank=True))
User.add_to_class('lattes', models.URLField(max_length=300, blank=True))
User.add_to_class('areaDeAtuacao', models.CharField(max_length=100, blank=True))
User.add_to_class('empreendedor', models.BooleanField())
User.add_to_class('consultor', models.BooleanField())
User.add_to_class('picture', models.ImageField(upload_to='profile_pictures'))

#UTILIZA COMPOSICAO
"""
Podemos tambem criar um relacionamento entro o User do Django e o Egresso
para que possamos usar o sistema de autenticacao do Django
"""

"""
Choices
"""
NIVEL_CHOICE = (
    ('superior', 'Superior'),
    ('tecnico', 'Tecnico'),
    ('medio', 'Medio')
)

SEXO_CHOICE = (
    ('M', 'Masculino'),
    ('F', 'Feminino')
)

CLASSIFICACAO_CHOICE = (
    ('microempresa', 'Micro Empresa'),
    ('pequenoporte', 'Pequeno Porte'),
    ('media', 'Media Empresa'),
    ('artesao', 'Artesao'),
    ('rural', 'Pordutor Rural'),
    ('individual', 'Empreendedor Rural')
)
"""
Modelos que se relacionarao com o usuario do sistema
"""
#class Egresso(models.Model):
#    user = models.ForeignKey(User, unique=True)
#    telefone = models.CharField(max_length=100, blank=True)
#    lattes = models.URLField(max_length=200, blank=True)
#    AreaDeAtuacao = models.CharField(max_length=100)
#    empreendedor = models.BooleanField()
#    consultor = models.BooleanField()

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    nivel = models.CharField(max_length=100, choices=NIVEL_CHOICE)
    egressos = models.ManyToManyField(User, through='EgressoCurso')

    def __unicode__(self):
        return u"%s" % (self.nome)

class EgressoCurso(models.Model):
    dataConclusao = models.DateField()
    egresso = models.ForeignKey(User)
    curso = models.ForeignKey(Curso)

class Empresa(models.Model):
    nome = models.CharField(max_length=200, blank=False)
    areaDeAtuacao = models.CharField(max_length=200, blank=False)
    dataCriacao = models.DateField()
    classificacao = models.CharField(max_length=100, choices=CLASSIFICACAO_CHOICE)
    site = models.URLField(max_length=200, blank=True)
    telefone = models.CharField(max_length=50, blank=True)
    dono = models.ForeignKey(User)