import hashlib
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from social.backends.google import GooglePlusAuth
from forms import EgressoForm
from models import Aluno


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render_to_response('home.html', RequestContext(request))


def home(request):
    """Pagina principal, exibe tela de login"""
    #se o usuario ja estiver logado, redirecione para pagina principal
    if request.user.is_authenticated():
        return redirect('done')
    else:
        if request.method == 'POST':
            print "faz o login do usuario"
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if username != '' and password != '':
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return redirect('done')
                else:
                    error = 'usuario ou senha nao conferem'
                    return render_to_response('home.html', {'error': error}, RequestContext(request))                
            else:
                error = 'Preencha todos os campos.'
                return render_to_response('home.html', {'error': error}, RequestContext(request))                
    return render_to_response('home.html', {
                                    'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
                                },
                            RequestContext(request))

@login_required
def foto(request):
    aluno = request.user.aluno
    print aluno.foto
    return render(request, 'foto.html', {'aluno': aluno})



@login_required
def done(request):
    """Login complete view, displays user data"""
    scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
    user = request.user
    aluno = user.aluno
    return render_to_response('done.html', {
        'aluno' : aluno,
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': scope
    }, RequestContext(request))


def register(request):
    """
    Registra o usuario no sistema, realizando o seu cadastro
    """
    form = EgressoForm()
    if request.method == 'POST':
        form = EgressoForm(request.POST)
        if form.is_valid():
            print 'Form valido'
            #agora precisamos verificar se ja nao existe um usuario com o mesmo email
            email = request.POST.get('email')
            if User.objects.filter(email=email).count() == 0:
                # se o password estiver batendo...
                if request.POST['password1'] == request.POST['password2']:
                    print 'usuario pode ser cadastrado'
                    #precisamos criar um usuario django para autenticacao
                    #para criar um usuario do Django, precisamos de um nome de usuario
                    #iremos atribuir o email como nome usuario para evitar duplicidade
                    user = User.objects.create_user(request.POST['email'], email, request.POST['password1'])
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.is_active = True
                    user.save()
                    #agora precisamos associar esse usuario com um egresso(aluno)
                    aluno = Aluno()
                    aluno.user = user
                    #e agora vamos popular o campos do usuario
                    aluno.lattes =  request.POST.get('lattes', '')
                    aluno.rua_av =  request.POST.get('rua', '')
                    aluno.bairro =  request.POST.get('bairro', '')
                    aluno.cep =     request.POST.get('cep', '')
                    aluno.cidade =  request.POST.get('cidade', '')
                    aluno.estado =  request.POST.get('estado', '')
                    aluno.sexo =    request.POST.get('sexo', '')
                    if request.FILES['foto'] is not None:
                        aluno.foto = request.FILES['foto']
                    aluno.save()
                    return redirect('home')
                else:
                    error = 'As senhas nao conferem'
                    return render(request, 'register.html', {'form' : form, 'error': error})    
            else:
                error = 'ja existe um usuario cadastrado com esse email'
                return render(request, 'register.html', {'form' : form, 'error': error})
        else:
            print 'Form invalido'
        
    return render(request, 'register.html', {'form' : form})

def confirmar_dados(request):
    """
    Complementa o cadastro de um aluno pre cadastrado no portal do egresso
    """
    #redireciona o usuario para o form de complementacao de dados
    if request.method == 'GET':
        q = request.GET.get('q', '')
        if q != '':
            print 'Hash: %s' % (q)
            usuarios = User.objects.all()
            for usuario in usuarios:
                if hashlib.sha224(usuario.email).hexdigest() == q:
                    print 'usuario localizado - nome: %s' % (usuario.first_name)
                    form = EgressoForm(
                        initial={'first_name': usuario.first_name,
                            'last_name': usuario.last_name,
                            'email': usuario.email,
                        })
                    
                    return render(request, 'complement.html', {'form': form})
        else:
            print 'parametro inexistente'
    #atualiza o usuario com seus novos dados
    elif request.method == 'POST':
        print 'POST para atualizacao dos dados'
    return redirect('home')

















