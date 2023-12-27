from django.urls import path
from .views import index,carro,sala, login, aprovar_carro,aprovar_sala,reservas,reserva_mes,reservas_json,reservas_get,manutencao,pings,json_ping

urlpatterns = [
    path('', index,name='index'),
    path('carros/<str:result>/<str:carro>',carro,name='carros'),
    path('salas/<str:result>/<str:sala>',sala,name='salas'),
    path('login',login,name='login'),
    path('aprovarCarro',aprovar_carro,name='aprovarCarro'),
    path('aprovarSala',aprovar_sala,name='aprovarSala'),
    path('reservas/<str:item>',reservas,name='reservas'),
    path('reservas-totais/<str:db>',reserva_mes,name='reservaMes'),
    path('tabela/<str:carro>/<str:dat>',reservas_get,name='reservasGET'),
    path('json/<str:item>',reservas_json,name='json'),

    #path('',manutencao,name='manutencao'),
    path('ping', pings, name='ping'),
    path('ping/json', json_ping, name='jsonPing'),
]