from urllib2 import urlopen
from django.utils.text import slugify
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from social.pipeline.partial import partial


@partial
def require_email(strategy, details, response, user=None, is_new=False, *args, **kwargs):
    #dumpclean(kwargs)
    print response
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('require_email')

#@partial
#def register(strategy, details, user=None, is_new=False, *args, **kwargs):
#    if is_new:

def save_facebook_profile_picture(strategy, details, response, user=None, is_new=False, *args, **kwargs):
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
