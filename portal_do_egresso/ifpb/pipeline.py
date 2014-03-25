from urllib2 import urlopen
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from social.pipeline.partial import partial


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
    try:
        print details
        email = details['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs


def save_facebook_profile_picture(strategy, details, response, user=None, is_new=False, *args, **kwargs):
    """
    Salva a imagem do perfil do facebook
    """
    if is_new and strategy.backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        picture = urlopen(url)
        user.picture.save(slugify(user.username + " social") + '.jpg', ContentFile(picture.read()))
        user.save()




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
