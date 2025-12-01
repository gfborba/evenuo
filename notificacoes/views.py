from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Notificacao
import json

@login_required
def listar_notificacoes(request):
    """Retorna as notificações do usuário em formato JSON para AJAX"""
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data_criacao')[:10]
    
    notificacoes_data = []
    for notif in notificacoes:
        notificacoes_data.append({
            'id': notif.id,
            'tipo': notif.tipo,
            'titulo': notif.titulo,
            'mensagem': notif.mensagem,
            'url': notif.url_redirecionamento or '#',
            'lida': notif.lida,
            'data_criacao': notif.data_criacao.strftime('%d/%m/%Y %H:%M'),
            'tempo_relativo': _tempo_relativo(notif.data_criacao),
        })
    
    return JsonResponse({
        'notificacoes': notificacoes_data,
        'total_nao_lidas': Notificacao.contar_nao_lidas(request.user)
    })

@login_required
@require_http_methods(["POST"])
def marcar_como_lida(request, notificacao_id):
    """Marca uma notificação específica como lida"""
    notificacao = get_object_or_404(Notificacao, id=notificacao_id, usuario=request.user)
    notificacao.marcar_como_lida()
    
    return JsonResponse({
        'success': True,
        'total_nao_lidas': Notificacao.contar_nao_lidas(request.user)
    })

@login_required
@require_http_methods(["POST"])
def marcar_todas_como_lidas(request):
    """Marca todas as notificações do usuário como lidas"""
    Notificacao.objects.filter(usuario=request.user, lida=False).update(lida=True)
    
    return JsonResponse({
        'success': True,
        'total_nao_lidas': 0
    })

@login_required
def contar_nao_lidas(request):
    """Retorna o número de notificações não lidas"""
    return JsonResponse({
        'total_nao_lidas': Notificacao.contar_nao_lidas(request.user)
    })

@login_required
def visualizar_notificacao(request, notificacao_id):
    """Visualiza uma notificação e redireciona para a URL apropriada"""
    notificacao = get_object_or_404(Notificacao, id=notificacao_id, usuario=request.user)
    
    #Marca como lida
    notificacao.marcar_como_lida()
    
    #Redireciona para a URL da notificação
    if notificacao.url_redirecionamento:
        return redirect(notificacao.url_redirecionamento)
    
    #Se não houver URL, redireciona para a página inicial
    return redirect('index')

def _tempo_relativo(data_criacao):
    """Retorna uma string com o tempo relativo (ex: 'há 5 minutos')"""
    from django.utils import timezone
    from datetime import timedelta
    
    agora = timezone.now()
    diferenca = agora - data_criacao
    
    if diferenca < timedelta(minutes=1):
        return 'agora'
    elif diferenca < timedelta(hours=1):
        minutos = int(diferenca.total_seconds() / 60)
        return f'há {minutos} minuto{"s" if minutos > 1 else ""}'
    elif diferenca < timedelta(days=1):
        horas = int(diferenca.total_seconds() / 3600)
        return f'há {horas} hora{"s" if horas > 1 else ""}'
    elif diferenca < timedelta(days=7):
        dias = diferenca.days
        return f'há {dias} dia{"s" if dias > 1 else ""}'
    else:
        return data_criacao.strftime('%d/%m/%Y')
