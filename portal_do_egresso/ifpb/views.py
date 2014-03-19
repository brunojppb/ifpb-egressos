from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from social.backends.google import GooglePlusAuth

from portal_do_egresso.ifpb.forms import EgressoForm


def logout(request):
    """Logs out user"""
    auth_logout(request)
    egressoForm = EgressoForm()
    return render_to_response('home.html', {'egressoForm': egressoForm}, RequestContext(request))


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    egressoForm = EgressoForm()
    return render_to_response('home.html', {
                                    'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
                                    'egressoForm': egressoForm
                                },
                            RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
    return render_to_response('done.html', {
        'user': request.user,
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': scope
    }, RequestContext(request))

def register(request):
    """Cadastro manual do egresso ou complementando os dados apos o uso de uma rede social"""
    if request.method == 'POST':
        #cadastra o usuario
        render_to_response('done.html')
    elif request.user.is_authenticated():
        user = request.user
        print "ENTROU========================================"
        egressoform = EgressoForm(initial={'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            })
    else:
        egressoform = EgressoForm()

    return render(request, 'egresso/create.html', {'egressoForm': egressoform})


def signup_email(request):
    return render_to_response('email_signup.html', {}, RequestContext(request))


def validation_sent(request):
    return render_to_response('validation_sent.html', {
        'email': request.session.get('email_validation_address')
    }, RequestContext(request))


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('email.html', RequestContext(request))
