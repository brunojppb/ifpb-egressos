import hashlib
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template import Context
from django.template.loader import get_template
from portal_do_egresso.ifpb.models import Aluno
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def convidar_cadastrados(request):
	alunos = Aluno.objects.all()
	for aluno in alunos:
		if aluno.user is None:
			email = aluno.user.email
			#criando um hash do email do aluno
			hash = hashlib.sha224(email).hexdigest()
			link = 'http://localhost:8000/complement/?q=%s' % (hash)
			temp_html = get_template('email/convite.html')
			temp_txt = get_template('email/convite.txt')
			context = Context({'nome': aluno.user.first_name, 'link': link})
			txt = temp_txt.render(context)
			html = temp_html.render(context)
			print html
			msg = EmailMultiAlternatives('Portal do Egresso - IFPB', txt, 'portaldoegressoifpb@gmail.com', [email])
			msg.attach_alternative(html, "text/html")
			msg.send()

	return redirect('done')
