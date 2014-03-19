from django.contrib.auth.models import User
from django import forms

class EgressoForm(forms.Form):
    """
    Formulario de cadastro do egresso, onde podera se cadastrar
    manualmente ou complementar seu cadastro vinculando sua conta do facebook
    """
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=50,
                                label='Nome de Usuario',
                                error_messages={'invalid': 'Insira apenas letras e numeros'},
                                widget=forms.TextInput(attrs={'class':'form-control'})
                                )
    first_name = forms.CharField(max_length=100, label='Nome', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, label='Sobrenome', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control'}))
    telefone = forms.CharField(max_length=20, label='Telefone', widget=forms.TextInput(attrs={'class':'form-control'}))
    lattes = forms.URLField(max_length=200, label='Link do Curriculo Lattes', widget=forms.TextInput(attrs={'class':'form-control'}))
    areaDeAtuacao = forms.CharField(max_length=100, label='Area de Atuacao', widget=forms.TextInput(attrs={'class':'form-control'}))
    empreendedor = forms.BooleanField(label='eh Empreendedor?')
    consultor = forms.BooleanField(label='eh Consultor?')
    senha1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Senha')
    senha2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Repita a senha')

    def clean_username(self):
        """
        Valida o nome de usuario para eviar duplicidade no banco
        """
        existente = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existente.exists():
            raise forms.ValidationError("Um mesmo nome de usuario ja existe")
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Valida o email para eviar duplicidade no banco
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("esse email ja foi usado")
        return self.cleaned_data['email']

    def clean(self):
        """
        Valida o formulario em se e tabem as senhas
        """
        if 'senha1' in self.cleaned_data and 'senha2' in self.cleaned_data:
            if self.cleaned_data['senha1'] != self.cleaned_data['senha2']:
                raise forms.ValidationError("As senhas nao conferem.")
            return self.cleaned_data
        raise forms.ValidationError("Preencha as senhas.")
