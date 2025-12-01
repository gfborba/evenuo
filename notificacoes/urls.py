from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar_notificacoes, name='listar_notificacoes'),
    path('contar/', views.contar_nao_lidas, name='contar_notificacoes'),
    path('<int:notificacao_id>/marcar-lida/', views.marcar_como_lida, name='marcar_notificacao_lida'),
    path('marcar-todas-lidas/', views.marcar_todas_como_lidas, name='marcar_todas_notificacoes_lidas'),
    path('<int:notificacao_id>/visualizar/', views.visualizar_notificacao, name='visualizar_notificacao'),
]

