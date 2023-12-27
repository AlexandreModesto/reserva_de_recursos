import os.path

from django.db import models

class Tv_PA(models.Model):
    nome_do_PA=models.CharField(max_length=100,blank=False,null=False)
    images=models.ManyToManyField(to='Tv_Imagem',null=True)

    def imagens_ativas(self):
        return f'Imagens ativas: {len(self.images.all())}'
    def __str__(self):
        return f'{self.nome_do_PA}, {self.imagens_ativas()}'

class Tv_Imagem (models.Model):
    nome_da_imagem=models.CharField(max_length=100,default='Imagem')
    imagem=models.ImageField(upload_to='Tv_imagens/carrossel/')
    adicionado_em=models.DateField(auto_now_add=True)

    def find_image(self):
        if os.path.exists('media/'+str(self.imagem)):
            return True
        else:return False
    def __str__(self):
        return self.nome_da_imagem
    
    
    
