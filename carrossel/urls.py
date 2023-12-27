from django.urls import path
from .views import carrossel,painel_pas,painel_pa_imagens,remove_imagem,remove_posto

app_name='tv'

urlpatterns=[
    path('carrossel/<int:id_pa>',carrossel,name='carrossel'),
    path('painel',painel_pas,name='painel_pa'),
    path('painel/<int:id_pa>',painel_pa_imagens,name='painel_pa_imagem'),
    path('painel/remover/imagem/<int:id_pa>/<int:id_img>',remove_imagem,name='remove_imagem'),
    path('painel/remover/posto/<int:id_pa>',remove_posto,name='remove_posto'),
]