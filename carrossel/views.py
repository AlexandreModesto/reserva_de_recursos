from django.shortcuts import render,redirect
from .models import Tv_PA,Tv_Imagem
from django.contrib import messages
import os


def carrossel(request,id_pa):
    first = Tv_PA.objects.get(id=id_pa).images.all()[0]
    imagens=Tv_PA.objects.get(id=id_pa).images.exclude(id=first.id)
    return render(request,'Tv/carrossel.html',{'imagens':imagens,'first':first})

def painel_pas(request):
    postos=Tv_PA.objects.all()
    if request.method == 'POST':
        nome=request.POST.get('nome_posto',None)
        p=Tv_PA(nome_do_PA=nome)
        p.save()

        return redirect('tv:painel_pa_imagem',p.id)

    return render(request,'Tv/painel_pa.html',{'postos':postos})


def painel_pa_imagens(request,id_pa):
    pa_imagens = Tv_PA.objects.get(id=id_pa)
    if request.method == 'POST':
        photo=request.FILES.get("photo")
        nome=str(photo)
        if not photo == None:
            p = Tv_Imagem(nome_da_imagem=nome, imagem=photo)
            p.save()
            Tv_PA.objects.get(id=id_pa).images.add(p)
            messages.success(request,f'Imagem {nome} adicionada')
        else:
            messages.error(request, f'Nenhuma Imagem selecionada')
    return render(request,'Tv/painel_pa_imagens.html',{'pa_imagens':pa_imagens,'id_pa':id_pa})

def remove_imagem(request,id_pa,id_img):
    posto = Tv_PA.objects.get(id=id_pa)
    img = Tv_Imagem.objects.get(id=id_img)

    if os.path.exists('media/' + str(img.imagem)):
        os.remove('media/' + str(img.imagem))
        posto.images.remove(img)
        posto.save()
        img.delete()
        messages.success(request,'Imagem Removida')
    else:
        messages.error(request, 'Imagem Não encontrada')

    return redirect('tv:painel_pa_imagem',id_pa)

def remove_posto(request,id_pa):
    p=Tv_PA.objects.get(id=id_pa)
    for i in p.images.all():
        img = Tv_Imagem.objects.get(id=i.id)
        if os.path.exists('media/' + str(img.imagem)):
            os.remove('media/' + str(img.imagem))
            img.delete()
        if os.path.exists('media/Tv_imagens/carrossel/' + str(img.nome_da_imagem)):
            os.remove('media/Tv_imagens/carrossel/' + str(img.nome_da_imagem))
            img.delete()

    p.delete()
    messages.success(request,'Posto Excluído')
    return redirect('tv:painel_pa')
