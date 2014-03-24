from django import forms

class EgressoForm(forms.Form):

    cpf =               forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}), label='CPF:')
    email =             forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), label='Email:')
    first_name =        forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), label='Nome:')
    last_name =         forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}), label='Sobrenome:')
    password1 =         forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Senha:')
    password2 =         forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Repita a senha:')
    telefone=           forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), label='Contato:')
    lattes=             forms.URLField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), label='Link do Curriculo Lattes:')
    areaDeAtuacao =     forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), label='Area de Atuacao')
    consultor =         forms.BooleanField(label='Consultor?')
    empreendedor =      forms.BooleanField(label='Empreendedor?')
    enderecoPessoal =   forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), label='Endereco Pessoal:')
    enderecoComercial = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), label='Endereco Comercial:')