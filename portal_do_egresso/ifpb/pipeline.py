from urllib2 import urlopen
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from social.pipeline.partial import *
from models import Aluno
from forms import EgressoForm


@partial
def require_email(strategy, details, response, user=None, is_new=False, *args, **kwargs):
    #dumpclean(response)
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('require_email')

@partial
def associate_by_mail(strategy, details, user=None, is_new=False, *args, **kwargs):
    """
    Associa um usuario ja existente a sua conta da rede social
    """
    try:
        print details
        email = details['email']
        kwargs['user'] = User.objects.get(email=email)
        is_new = False
    except:
        pass
    return kwargs


@partial
def save_facebook_profile_picture(strategy, details, response, user=None, is_new=False, *args, **kwargs):
    """
    Salva a imagem do perfil do facebook
    """
    if is_new and strategy.backend.name == 'facebook':
        print 'Novo usuario chegando!! pegando a foto do facebook agora...'
        url = "http://graph.facebook.com/%s/picture?type=large" % (response['id'])
        picture = urlopen(url)
        aluno = Aluno()
        aluno.user = user
        aluno.save()
        aluno.foto.save('{0}._social.jpg'.format(user.username), ContentFile(picture.read()))
        aluno.save()
        user.save()
        kwargs['aluno'] = aluno
    return kwargs

@partial
def complete_register(strategy, details, response, user=None, is_new=False, *args, **kwargs):
    """Complementa o cadastro do usuario autenticado pelo facebook"""
    if user is not None:
        if user.aluno is not None:
            for (chave, valor) in kwargs.items:
                print '%s: %s' % (chave, valor)
    return kwargs



def dumpclean(obj):
    """
        imprime o dicionario formatado para leitura
    """
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj
