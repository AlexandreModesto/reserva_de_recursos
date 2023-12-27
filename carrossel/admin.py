from django.contrib import admin
from .models import Tv_PA, Tv_Imagem
class ListandoImagens(admin.ModelAdmin):
    list_display = ('id','nome_do_PA')
    list_display_links = ("id", "nome_do_PA")
class TvImagems(admin.ModelAdmin):
    list_display = ('id', 'nome_da_imagem')
    list_display_links = ("id", "nome_da_imagem")

admin.site.register(Tv_PA, ListandoImagens)
admin.site.register(Tv_Imagem, TvImagems)
