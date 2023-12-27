#-*-coding:utf-8 -*-
import django.contrib.auth
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
import ping3

from .models import Carro,Sala
from .forms import ReservaSala,ReservaCarro,LoginForms,ReservasForm
from django.core.mail import EmailMessage
from django.contrib import messages
from datetime import date,datetime,timedelta


def index(request):
    carro_list=['FordKa','Onix','HB20']
    sala_list=['Sala Terreo','Sala andar 1','Sala Maior Conad','Sala Menor Conad','Auditório']
    return render(request,'reserva/index.html',{'carro_list':carro_list,'sala_list':sala_list})

def conversor_de_hora(hora):
    if not len(hora) > 1:
        return hora[0]
    else:
        hora_convetida=f'{hora[0][:5]}-{hora[-1][-5:]}'
        return hora_convetida

def conversor_reverso(hora,carro=False,sala=False,auditorio=False):
    try : hora[0]
    except:return ['']
    carro_h_lista=['07:50-08:50', '08:51-09:50','09:51-10:50','10:51-11:50','11:51-12:50','12:51-13:50','13:51-14:50',
             '14:51-15:50','15:51-17:15']
    sala_h_lista=['07:50-08:30','08:31-09:00','09:01-09:30',
             '09:31-10:00','10:01-10:30','10:31-11:00','11:01-11:30',
             '11:31-12:00','12:01-12:30','12:31-13:00',
             '13:01-13:30','13:31-14:00','14:01-14:30',
             '14:31-15:00', '15:01-15:30','15:31-16:00',
             '16:01-16:30','16:31-17:15']
    auditorio_h_lista = ['08:00-12:00','12:01-17:00','17:01-22:50']
    init=0
    end=0
    horas=[]
    if carro==True:
        h_lista=carro_h_lista
    elif sala==True:
        h_lista=sala_h_lista
    elif auditorio==True:
        h_lista=auditorio_h_lista
    for query in hora:
        for h in h_lista:
            if query[0][:5] == h[:5]:
                init=h_lista.index(h)
            if query[0][-5:] == h[-5:]:
                end=h_lista.index(h)
        for i in range(init,end+1):
            horas.append(h_lista[i])

    return horas

def carro(request,result,carro):
    if not carro == "FordKa" and not carro == "Onix" and not carro == "HB20":
        return redirect('reservas',carro)
    carroForm = ReservaCarro()
    result = result.split('-')
    data = f'{result[0]}/{result[1]}/{result[2]}'
    n_result = f'{result[2]}/{result[1]}/{result[0]}'
    data_f = datetime.strptime(n_result, '%Y/%m/%d').date()

    select=Carro.objects.filter(carro=carro,data=n_result.replace('/','-'),aprovado=True).values_list('hora')
    selecteds=conversor_reverso(select,carro=True)
    len=selecteds.__len__()


    if request.method == 'POST':
        carroForm = ReservaCarro(request.POST)
        if carroForm.is_valid():
            nome=carroForm.cleaned_data['nome']
            nome=nome.replace(' ','-')
            email=carroForm.cleaned_data['email']
            hora = request.POST.getlist('hora')
            rep=carroForm.cleaned_data['repetir']
            motivo=carroForm.cleaned_data['motivo']
            motivo = motivo.replace(' ', '-')

            data_f = datetime.strptime(n_result, '%Y/%m/%d').date()
            if not rep:
                r=Carro(carro=carro,motivo=motivo,solicitante=nome,email_solicitante=email,data=data_f,hora=conversor_de_hora(hora))
                r.save()
            else:
                nuRepetir = request.POST.get('nuRepetir', None)  # numero
                tpRepetir = request.POST.get('tpRepetir', None)  # D/S
                ate = request.POST.get('ate', None)
                ate_l=str(ate).split('/')
                ate_s = f'{ate_l[2]}-{ate_l[1]}-{ate_l[0]}'
                ate_f = datetime.strptime(ate_s, '%Y-%m-%d').date()

                prox_data = data_f
                if tpRepetir == 'D':

                    r = Carro(carro=carro,motivo=motivo, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=conversor_de_hora(hora))
                    r.save()

                    if ate_f.month > data_f.month:
                        calculo=(data_f.day-ate_f.day)+1
                    else:
                        calculo = (ate_f.day - data_f.day) + 1
                    for i in range(0,calculo, int(nuRepetir)):
                        prox_data=prox_data + timedelta(days=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        if prox_data.weekday() < 5:
                            r = Carro(carro=carro,motivo=motivo, solicitante=nome, email_solicitante=email,
                                      data=str(prox_data), hora=conversor_de_hora(hora))
                            r.save()
                        else:pass
                else:
                    r = Carro(carro=carro,motivo=motivo, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=conversor_de_hora(hora))
                    r.save()
                    finalRange = ate_f - data_f
                    for i in range(7, finalRange.days+1,7):
                        prox_data = prox_data + timedelta(weeks=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        if prox_data.weekday() < 5:
                            r = Carro(carro=carro,motivo=motivo, solicitante=nome, email_solicitante=email,
                                      data=str(prox_data), hora=conversor_de_hora(hora))
                            r.save()
                        else:pass

            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Nova Solicitação de Reserva</h1>
                                            <p><strong>{nome.replace('-',' ')} esta solicitando reserva do {carro} pro dia <strong>{data}</strong> horário: <strong>{conversor_de_hora(hora)}</strong></p>
                                            <p>Para aprovar ou não clique <a href='10.110.209.15:90/aprovarSala'>aqui</a></p>""",
                None,
                ['antoniorezende@sicoob.com.br'])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request,'Reserva encaminhada para Aprovação')
            return redirect('index')
        print(carroForm.errors.as_data())
    return render(request,'reserva/carro.html',{'carroForm':carroForm,'carro':carro,'data':data,'selecteds':selecteds,'len':len})

def sala(request,result,sala):
    if sala == "FordKa" and sala == "Onix" and sala == "HB20":
        return redirect('reservas',sala)
    salaForm = ReservaSala()
    result = result.split('-')
    data = f'{result[0]}/{result[1]}/{result[2]}'
    n_result = f'{result[2]}/{result[1]}/{result[0]}'
    select = Sala.objects.filter(sala=sala, data=n_result.replace('/', '-'),aprovado=True).values_list('hora')
    if sala == 'Auditorio':
        selecteds = conversor_reverso(select, auditorio=True)
    else:
        selecteds = conversor_reverso(select, sala=True)
    if request.method == 'POST':
        salaForm = ReservaSala(request.POST)
        if salaForm.is_valid():
            nome=salaForm.cleaned_data['nome']
            nome=nome.replace(' ','-')
            email=salaForm.cleaned_data['email']
            hora = request.POST.getlist('hora')
            rep=salaForm.cleaned_data['repetir']
            motivo=salaForm.cleaned_data['motivo']
            motivo = motivo.replace(' ', '-')
            if sala=='Sala Menor Conad' or sala=='Sala Maior Conad':
                apro='Maria Valdirene'
                mail='valdirene.monteiro@sicoob.com.br'
            elif sala == 'Auditorio':
                apro='Maria José'
                mail='maze.teixera@sicoob.com.br'
            else:
                apro = 'Mayara Alvarenga'
                mail = 'mayara.alvarenga@sicoob.com.br'

            data_f = datetime.strptime(n_result, '%Y/%m/%d').date()
            if not rep:
                r=Sala(sala=sala,motivo=motivo,aprovador=apro,solicitante=nome,email_solicitante=email,data=data_f,hora=conversor_de_hora(hora))
                r.save()
            else:
                nuRepetir = request.POST.get('nuRepetir', None)  # numero
                tpRepetir = request.POST.get('tpRepetir', None)  # D/S
                ate = request.POST.get('ate', None)
                ate_l = str(ate).split('/')
                ate_s = f'{ate_l[2]}-{ate_l[1]}-{ate_l[0]}'
                ate_f = datetime.strptime(ate_s, '%Y-%m-%d').date()

                prox_data = data_f
                if tpRepetir == 'D':
                    r = Sala(sala=sala,motivo=motivo,aprovador=apro, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=conversor_de_hora(hora))
                    r.save()

                    if ate_f.month > data_f.month:
                        calculo=(data_f.day-ate_f.day)+1
                    else:
                        calculo = (ate_f.day - data_f.day) + 1
                    for i in range(0,calculo, int(nuRepetir)):
                        prox_data=prox_data + timedelta(days=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        if prox_data.weekday() < 5:
                            r = Sala(sala=sala,motivo=motivo,aprovador=apro, solicitante=nome, email_solicitante=email,
                                      data=str(prox_data), hora=conversor_de_hora(hora))
                            r.save()
                        else:pass
                else:
                    r = Sala(sala=sala,motivo=motivo,aprovador=apro, solicitante=nome, email_solicitante=email,
                              data=str(prox_data), hora=conversor_de_hora(hora))
                    r.save()
                    finalRange = ate_f - data_f
                    for i in range(7, finalRange.days+1,7):
                        prox_data = prox_data + timedelta(weeks=int(nuRepetir))
                        if prox_data > ate_f:
                            break
                        if prox_data.weekday() < 5:
                            r = Sala(sala=sala,motivo=motivo,aprovador=apro, solicitante=nome, email_solicitante=email,
                                      data=str(prox_data), hora=conversor_de_hora(hora))
                            r.save()
                        else:pass

            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Nova Solicitação de Reserva</h1>
                                            <p><strong>{nome.replace('-',' ')} esta solicitando reserva da(o) {sala} pro dia <strong>{data}</strong> horário: <strong>{conversor_de_hora(hora)}</strong></p>
                                            <p>Para aprovar ou não clique <a href='10.110.209.15:90/aprovarSala'>aqui</a></p>""",
                None,
                [mail])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request,'Reserva encaminhada para Aprovação')
            return redirect('index')
        print(salaForm.errors.as_data())
    return render(request,'reserva/sala.html',{'salaForm':salaForm,'sala':sala,'data':data,'selecteds':selecteds})


def login(request):
    if request.user.is_authenticated and not request.user.username.endswith('runner'):
        if not request.user.username.endswith('m'):
            return redirect('aprovarCarro')
        elif request.user.username.endswith('m'):
            return redirect('aprovarSala')
        elif request.user.username.endswith('Tv'):
            return redirect('tv:painel_pa')
    login = LoginForms()
    if request.method=='POST':
        loginForm = LoginForms(request.POST)
        if loginForm.is_valid():
            usuario=loginForm.cleaned_data['usuario']
            senha = loginForm.cleaned_data['senha']
            user = authenticate(request,username=usuario,password=senha)
            if user is not None:
                django.contrib.auth.login(request,user)
                messages.success(request,'Usuário Logado')
                if usuario == 'rezendea':
                    return redirect('aprovarCarro')
                elif usuario == 'adminTv':
                    return redirect('tv:painel_pa')
                else:
                    return redirect('aprovarSala')
            else:
                messages.error(request, 'Acesso Negado')
                return redirect('login')
    return render(request,'reserva/login.html',{'login':login})

def aprovar_carro(request):
    if not request.user.username.endswith('a'):
        return redirect('login')
    retorna_soli_none = Carro.objects.filter(aprovado=None,data__gte=datetime.today())
    retorna_soli_true = Carro.objects.filter(aprovado=True,data__gte=datetime.today())

    if request.method =="POST":
        check = request.POST.get('botao')
        id = request.POST.get('id')
        obj = Carro.objects.filter(id=id).values('carro','data','hora','email_solicitante')
        valores=[]
        for campo,valor in obj[0].items():
            valores.append(valor)

        if check == 'aprovar':
            Carro.objects.filter(id=id).update(aprovado=True)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Aprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Aprovada</strong></p>""",
                None,
                [valores[3]])
            msg.content_subtype="html"
            msg.send()
            messages.success(request, 'Aprovado')
        elif check == 'cancelar':
            Carro.objects.filter(id=id).update(aprovado=False)
            parecer=request.POST.get('reproCancelado')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Cancelada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Cancelada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Cancelado')
        else:
            Carro.objects.filter(id=id).update(aprovado=False)
            parecer=request.POST.get('repro')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Reprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>reprovada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Reprovado')
        return redirect('aprovarCarro')
    return render(request,'reserva/aprovarCarro.html',{'db_none':retorna_soli_none,'db_true':retorna_soli_true})

def aprovar_sala(request):
    if not request.user.username.endswith('m'):
        return redirect('login')
    mayara='Mayara Alvarenga'
    vald='Maria Valdirene'
    maze='Maria José'
    if request.user.username.endswith('valdirenem'):
        retorna_soli_none = Sala.objects.filter(aprovador=vald,aprovado=None,data__gte=datetime.today())
        retorna_soli_true = Sala.objects.filter(aprovador=vald,aprovado=True, data__gte=datetime.today())
    elif request.user.username.endswith('teixeiram'):
        retorna_soli_none = Sala.objects.filter(aprovador=maze, aprovado=None, data__gte=datetime.today())
        retorna_soli_true = Sala.objects.filter(aprovador=maze, aprovado=True, data__gte=datetime.today())
    else:
        retorna_soli_none = Sala.objects.filter(aprovador=mayara, aprovado=None, data__gte=datetime.today())
        retorna_soli_true = Sala.objects.filter(aprovador=mayara, aprovado=True, data__gte=datetime.today())

    if request.method =="POST":
        id = request.POST.get('id')
        check = request.POST.get('botao')
        obj = Sala.objects.filter(id=id).values('sala', 'data','hora','email_solicitante')
        valores = []
        for campo, valor in obj[0].items():
            valores.append(valor)
        if check == 'aprovar':
            Sala.objects.filter(id=id).update(aprovado=True)
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Aprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Aprovada</strong></p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Aprovado')
        elif check == 'cancelar':
            Sala.objects.filter(id=id).update(aprovado=False)
            parecer = request.POST.get('reproCancelado')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Cancelada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>Cancelada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Cancelado')
        else:
            Sala.objects.filter(id=id).update(aprovado=False)
            parecer = request.POST.get('repro')
            msg = EmailMessage(
                "Solicitação de Reserva",
                fr"""<h1>Solicitação de Reserva foi Reprovada</h1>
                <p>Sua solicitação de reserva do <strong>{valores[0]}</strong> pro dia <strong>{str(valores[1])[8:10]}/{str(valores[1])[5:7]}/{str(valores[1])[:4]}</strong> horário: <strong>{valores[2]}</strong> foi <strong>reprovada</strong></p>
                <p><strong>Motivo</strong>: {parecer}</p>""",
                None,
                [valores[3]])
            msg.content_subtype = "html"
            msg.send()
            messages.success(request, 'Reprovado')
        return redirect('aprovarSala')
    return render(request,'reserva/aprovarSala.html',{'db_none':retorna_soli_none,'db_true':retorna_soli_true})

def return_number(mes):
    dict = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7,
            'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
    return dict[mes]

def reservas(request,item):
    form=ReservasForm()
    if request.method =='POST':
        result = request.POST.get('result',None)
        result = result.replace('/','-')
        if item[:4] == 'Sala' or item == 'Auditorio':
            return redirect('salas', result, item)
        else:
            return redirect('carros',result,item)
    return render(request,'reserva/reservas.html',{'item':item})

def reservas_get(request,carro,dat):
    try:
        tabela=Carro.objects.filter(data=dat,carro=carro,aprovado=True).values()
        print(tabela[0])
    except:
        tabela = Sala.objects.filter(data=dat, sala=carro,aprovado=True).values()
    table = {'solicitante': '', 'motivo': '', 'hora': '', 'aprovado': ''}
    for item in tabela:
        table['solicitante'] += ' ' + item['solicitante']
        table['motivo'] += ' ' + str(item['motivo'])
        table['hora'] += ' ' + item['hora']
        table['aprovado'] += ' ' + str(item['aprovado'])
    table['solicitante'] = table['solicitante'].split()
    table['motivo'] = table['motivo'].split()
    table['hora'] = table['hora'].split()
    table['aprovado'] = table['aprovado'].split()
    return JsonResponse(table,safe=False)


def reservas_json(request,item):
    consultaSala = Sala.objects.filter(data__gte=datetime.today(),aprovado=True)
    consultaCarro = Carro.objects.filter(data__gte=datetime.today(),aprovado=True)

    #Ford Ka

    if item == 'FordKa':
        indice = 0
        fordka=consultaCarro.filter(carro=item)
        resultadosFordKa = {}
        mes_anterior=''

        for i in range(0,len(fordka.dates('data','month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux=fordka.order_by('data').values()

            while True:
                aux_date=aux[indice]['data']
                mes=datetime.strptime(str(aux_date),'%Y-%m-%d').date().month


                if not mes == mes_anterior :
                    mes_anterior=mes
                    break
                else:
                    indice+=1

            for item in fordka.filter(data__month=mes):
                data = datetime.strptime(str(item.data),'%Y-%m-%d').date()
                dias.append(data.day)
                data_f= str(data).split('-')
                data_s=f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados={
                "mes":mes-1,
                "dia":dias,
                "datas":datas,
                "motivo":motivo,
                "solicitante":solicitante
            }
            resultadosFordKa[i]=dados

        return JsonResponse(resultadosFordKa)

    #Onix

    elif item == 'Onix':
        indice = 0
        onix = consultaCarro.filter(carro=item)
        resultadosOnix = {}
        mes_anterior = ''

        for i in range(0, len(onix.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = onix.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in onix.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosOnix[i] = dados

        return JsonResponse(resultadosOnix)

    #HB20

    elif item == 'HB20':
        indice = 0
        HB20 = consultaCarro.filter(carro=item)
        resultadosHB20 = {}
        mes_anterior = ''

        for i in range(0, len(HB20.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = HB20.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in HB20.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosHB20[i] = dados

        return JsonResponse(resultadosHB20)

    #Sala andar 1

    elif item == 'Sala andar 1':
        indice = 0
        sala1 = consultaSala.filter(sala=item)
        resultadosSala1 = {}
        mes_anterior = ''

        for i in range(0, len(sala1.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = sala1.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in sala1.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSala1[i] = dados

        return JsonResponse(resultadosSala1)

    #Sala Terreo

    elif item == 'Sala Terreo':
        indice = 0
        salaT = consultaSala.filter(sala=item)
        resultadosSalaT = {}
        mes_anterior = ''

        for i in range(0, len(salaT.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaT.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaT.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaT[i] = dados

        return JsonResponse(resultadosSalaT)

    #Sala Conad Maior

    elif item == 'Sala Maior Conad':
        indice = 0
        salaConadM = consultaSala.filter(sala=item)
        resultadosSalaConadM = {}
        mes_anterior = ''

        for i in range(0, len(salaConadM.dates('data', 'month'))):

            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaConadM.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaConadM.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()

                dias.append(data.day)
                data_f = str(data).split('-')

                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaConadM[i] = dados

        return JsonResponse(resultadosSalaConadM)

    #Sala Conad Menor

    elif item == 'Sala Menor Conad':
        indice = 0
        salaConadm = consultaSala.filter(sala=item)
        resultadosSalaConadm = {}
        mes_anterior = ''

        for i in range(0, len(salaConadm.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaConadm.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month
                ano = datetime.strptime(str(aux_date), '%Y-%m-%d').date().year
                if not mes == mes_anterior:
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaConadm.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "ano":ano,
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaConadm[i] = dados

        return JsonResponse(resultadosSalaConadm)

    #Auditorio

    else:
        indice = 0
        salaAuditorio = consultaSala.filter(sala=item)
        resultadosSalaAuditorio = {}
        mes_anterior = ''

        for i in range(0, len(salaAuditorio.dates('data', 'month'))):
            dias = []
            datas = []
            motivo = []
            solicitante = []
            aux = salaAuditorio.order_by('data').values()
            while True:
                aux_date = aux[indice]['data']
                mes = datetime.strptime(str(aux_date), '%Y-%m-%d').date().month

                if not mes == mes_anterior:
                    mes_anterior = mes
                    break
                else:
                    indice += 1

            for item in salaAuditorio.filter(data__month=mes):
                data = datetime.strptime(str(item.data), '%Y-%m-%d').date()
                dias.append(data.day)
                data_f = str(data).split('-')
                data_s = f'{data_f[2]}/{data_f[1]}/{data_f[0]}'
                datas.append(data_s)

                motivo.append(item.motivo)
                solicitante.append(item.solicitante)

            dados = {
                "mes": mes - 1,
                "dia": dias,
                "datas": datas,
                "motivo": motivo,
                "solicitante": solicitante
            }
            resultadosSalaAuditorio[i] = dados

        return JsonResponse(resultadosSalaAuditorio)

def reserva_mes(request,db):
    if not db == 'Sala':
        retorno = Carro.objects.filter(created_at__month__gte=date.today().month)
        retorno_todos = Carro.objects.filter(created_at__month__lte=date.today().month)
        retorno_todos =retorno_todos.filter(created_at__month__gte=date.today().month-2)
        return render(request, 'reserva/reservasCarro.html', {'model': retorno,'model_todos':retorno_todos})
    else:
        retorno = Sala.objects.filter(created_at__month__gte=date.today().month)
        retorno_todos = Sala.objects.filter(created_at__month__lte=date.today().month)
        retorno_todos = retorno_todos.filter(created_at__month__gte=date.today().month - 2)
        return render(request, 'reserva/reservasSala.html', {'model': retorno,'model_todos':retorno_todos})

def manutencao(request):
    return render(request,'reserva/manutencao.html')

def pings(request):
    # car = Carro.objects.filter(id=156).values_list()
    # for i in car[0]:
    #     print(i)
    return render(request,'reserva/pinging.html')

def json_ping(request):
    ping3.EXCEPTIONS=True
    json_ip={'local':['Firewall Sede','Pindamonhangaba','Botucatu','Araraquara','Guaratingueta','Campinas','Sisbr','Site Cooperemb','#COOP','Centro','Portal Cooperemb'],'ping':[],'status':[],'ip':[]}
    lista_ip=['189.127.6.65', '10.111.210.1', '10.112.211.1','10.113.212.1','10.114.213.1','10.116.215.1','172.16.2.188','172.67.135.223','13.107.213.33','10.115.214.1','www.cooperemb.com']
    for ip in lista_ip:
        try:
            ping = ping3.ping(ip)
        except:
            json_ip['ping'].append('Tempo excedido')
            json_ip['status'].append('alto')
            json_ip['ip'].append(ip)
        else:
            ping_string = str(ping)[2:6]
            if int(ping_string) < 70:
                json_ip['ping'].append(f'{int(ping_string)}ms')
                json_ip['status'].append('baixo')
                json_ip['ip'].append(ip)
            elif int(ping_string)  < 600 > 70:
                json_ip['ping'].append(f'{int(ping_string)}ms')
                json_ip['status'].append('medio')
                json_ip['ip'].append(ip)
            else:
                json_ip['ping'].append(f'{int(ping_string)}ms')
                json_ip['status'].append('alto')
                json_ip['ip'].append(ip)
    return JsonResponse(json_ip)


