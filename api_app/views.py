from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers, viewsets
from django.http import JsonResponse,HttpResponse
from django.core.validators import validate_email
from .serializers import *
import json
from math import sqrt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.decorators.csrf import csrf_exempt
from geopy.distance import distance

#Acesso ao usuario via Token
#request.user will be a Django User instance.
#request.auth will be a rest_framework.authtoken.models.Token instance.

# ViewSets define the view behavior.
# @permission_classes((IsAuthenticatedOrReadOnly,))
# class ProdutoList(viewsets.ModelViewSet):
#     queryset = Produto.objects.all()
#     serializer_class = ProdutoSerializer
#     def get_queryset(self):
#         return self.queryset.filter(em_estoque=True)

class JogadorList(viewsets.ModelViewSet):
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer

class Objeto_erList(viewsets.ModelViewSet):
    queryset = Objeto_er.objects.all()
    serializer_class = Objeto_erSerializer

class Objeto_er_mapList(viewsets.ModelViewSet):
    queryset = Objeto_er_map.objects.all()
    serializer_class = Objeto_er_mapSerializer

class CapturaList(viewsets.ModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer

def criar_automaticamente(latitude,longitude):
    novo1 = Objeto_er_map()
    novo1.objeto_er = Objeto_er.objects.all().first()
    novo1.latitude = latitude - 0.0002
    novo1.longitude = longitude - 0.0002
    novo1.save()
    novo2 = Objeto_er_map()
    novo2.objeto_er = Objeto_er.objects.all().last()
    novo2.latitude = latitude + 0.0002
    novo2.longitude = longitude + 0.0002
    novo2.save()
    

@api_view(['GET'])
def personagens_proximos(request):
    try:
        latitude = float(request.headers["Latitude"].replace(",","."))
        longitude = float(request.headers["Longitude"].replace(",","."))
        
        try:
            animacao = request.headers["Animacao"]
        except:
            animacao = "default"
        
        try:
            avatar = request.headers["Avatar"]
        except:
            avatar = "default"
        
        print(latitude,longitude)
        localizacao_player = (latitude,longitude)
    except:
        erro = "Enviar a localizacao latitude e longitude via cabeçalho"
        return JsonResponse(erro,status=400,safe=False)
    personagens = []
    jogadores = []

    Jogador.objects.all().update(online=False)

    try:
        jogador = Token.objects.get(key=request.auth).user.jogador
    except:
        jogador = Jogador(user=Token.objects.get(key=request.auth).user)
    
    jogador.latitude = latitude
    jogador.longitude = longitude
    jogador.avatar = avatar
    jogador.animacao = animacao
    jogador.online = True
    jogador.save()

    for obj_er_map in Objeto_er_map.objects.all():
        try:
            localizacao_personagem = (obj_er_map.latitude,obj_er_map.longitude)
            distancia = 1000 * distance(localizacao_player, localizacao_personagem).km
            if distancia <= 500: # Mostrar personagens com 500 metros ou menos do jogador
                j = Objeto_er_mapSerializer(obj_er_map)
                personagens.append(j.data)
        except:
            pass
    for jogador in Jogador.objects.all().exclude(pk=jogador.pk):
        try:
            localizacao_jogador = (jogador.latitude,jogador.longitude)
            distancia = 1000 * distance(localizacao_player, localizacao_jogador).km
            if distancia <= 500: # Mostrar personagens com 500 metros ou menos do jogador
                j = JogadorSerializer(jogador)
                jogadores.append(j.data)
        except:
            pass

    if len(personagens) == 0 : criar_automaticamente(latitude,longitude)
    resultado = {
        "personagens":personagens,
        "jogadores":jogadores
    }
    print(resultado)
    return JsonResponse(resultado,safe=False)
