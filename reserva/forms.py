#-*-coding:utf-8 -*-
from django import forms
import  datetime

class ReservaCarro(forms.Form):
    carroChoices=(('Ford Ka','Ford Ka'),('Onix','Onix'),('HB20','HB20'),)
    carro=forms.ChoiceField(choices=carroChoices,label='Qual carro?',required=False)
    nome = forms.CharField(label='Digite seu nome', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome sobrenome', }))
    email = forms.EmailField(label='Digite seu email', max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@email.com'}))
    motivo=forms.CharField(label='Qual o motivo?', max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Viagem para BOT'}))
    repetir=forms.BooleanField(required=False,label='Repetir',)


class ReservaSala(forms.Form):
    salaChoices=(('Sala Terreo','Sala no Terreo'),('Sala andar 1','Sala do 1°andar'),('Sala Conad Maior','Sala Maior do Conad'),('Sala Conad Menor','Sala Menor do Conad'),('Auditório','Auditório'))
    salas=forms.ChoiceField(choices=salaChoices,label='Qual sala?',required=False)
    nome = forms.CharField(label='Digite seu nome', max_length=100,
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome sobrenome',}))
    email = forms.EmailField(label='Digite seu email', max_length=100,
                             widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email@email.com'}))
    motivo = forms.CharField(label='Qual o motivo?', max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reunião da Diretoria'}))
    repetir = forms.BooleanField(required=False, label='Repetir', )


class LoginForms(forms.Form):
    usuario=forms.CharField(label='Usuario', max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'similar a VPN',}))
    senha=forms.CharField(label='Senha', max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'senha',}))

def return_month(date,now=False,one=False,two=False):
    hoje=datetime.datetime.now()
    dict={1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}
    if not now == False:
        return dict[hoje.month]
    elif not one == False:
        try:
            return dict[hoje.month+1]
        except:
            return dict[hoje.month]
    else:
        try:
            return dict[hoje.month+2]
        except:
            dict[hoje.month]=1
            return dict[hoje.month]
class ReservasForm(forms.Form):
    date=datetime.datetime.now()
    meses=((return_month(date,now=True),(return_month(date,now=True))),(return_month(date,one=True),return_month(date,one=True)),(return_month(date=date,two=True),return_month(date=date,two=True)))
    mes=forms.ChoiceField(choices=meses,label='Qual Mês? ')