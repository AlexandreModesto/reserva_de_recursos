from django.db import models

# Create your models here.
class Carro(models.Model):
    carro=models.CharField(max_length=100)
    aprovador=models.CharField(max_length=100, default='Antônio Rezende')
    email=models.EmailField(max_length=254, default='antoniorezende@sicoob.com.br')
    solicitante=models.CharField(max_length=100,null=True,blank=True)
    motivo=models.CharField(max_length=100,null=True,blank=True)
    email_solicitante=models.EmailField(max_length=254,null=True,blank=True)
    data = models.DateField(null=True, blank=True)
    hora = models.CharField(max_length=11,null=True, blank=True)
    aprovado = models.BooleanField(null=True, blank=True)
    created_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract = False

    def __str__(self):
        return self.carro
class Sala(models.Model):
    sala=models.CharField(max_length=100)
    aprovador=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    solicitante = models.CharField(max_length=100, null=True,blank=True)
    motivo = models.CharField(max_length=100, null=True, blank=True)
    email_solicitante = models.EmailField(max_length=254, null=True,blank=True)
    data = models.DateField(null=True, blank=True)
    hora=models.CharField(max_length=11,null=True,blank=True)
    aprovado=models.BooleanField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = False

    def __str__(self):
        return self.sala