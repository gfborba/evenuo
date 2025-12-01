"""
Utilitários para criar notificações no sistema
"""
from django.contrib.auth.models import User
from .models import Notificacao


def criar_notificacao_chat(usuario_destino, usuario_remetente, url_redirecionamento=None):
    """Cria uma notificação quando uma nova mensagem é enviada no chat"""
    if not url_redirecionamento:
        url_redirecionamento = f'/chat/{usuario_remetente.username}/'
    
    return Notificacao.criar_notificacao(
        usuario=usuario_destino,
        tipo='chat',
        titulo='Nova mensagem',
        mensagem=f'{usuario_remetente.get_full_name() or usuario_remetente.username} enviou uma mensagem',
        url_redirecionamento=url_redirecionamento,
        objeto_id=usuario_remetente.id,
        objeto_tipo='user'
    )


def criar_notificacao_pergunta(organizador, fornecedor, evento, pergunta_id):
    """Cria uma notificação quando uma nova pergunta é feita em um evento"""
    return Notificacao.criar_notificacao(
        usuario=organizador.user,
        tipo='pergunta',
        titulo='Nova pergunta em evento',
        mensagem=f'{fornecedor.user.get_full_name() or fornecedor.user.username} fez uma pergunta sobre o evento "{evento.nomeEvento}"',
        url_redirecionamento=f'/evento/{evento.id}/',
        objeto_id=pergunta_id,
        objeto_tipo='pergunta'
    )


def criar_notificacao_resposta(fornecedor, organizador, evento, pergunta_id):
    """Cria uma notificação quando uma pergunta é respondida"""
    return Notificacao.criar_notificacao(
        usuario=fornecedor.user,
        tipo='resposta',
        titulo='Pergunta respondida',
        mensagem=f'{organizador.user.get_full_name() or organizador.user.username} respondeu sua pergunta sobre o evento "{evento.nomeEvento}"',
        url_redirecionamento=f'/evento/{evento.id}/',
        objeto_id=pergunta_id,
        objeto_tipo='pergunta'
    )


def criar_notificacao_avaliacao(fornecedor, organizador):
    """Cria uma notificação quando um fornecedor recebe uma avaliação"""
    return Notificacao.criar_notificacao(
        usuario=fornecedor.user,
        tipo='avaliacao',
        titulo='Nova avaliação',
        mensagem=f'{organizador.user.get_full_name() or organizador.user.username} avaliou seus serviços',
        url_redirecionamento=f'/fornecedor/{fornecedor.id}/',
        objeto_id=fornecedor.id,
        objeto_tipo='fornecedor'
    )


def criar_notificacao_compromisso(usuario, titulo, url_redirecionamento=None):
    """Cria uma notificação quando um compromisso é adicionado na agenda"""
    if not url_redirecionamento:
        url_redirecionamento = '/agenda/'
    
    return Notificacao.criar_notificacao(
        usuario=usuario,
        tipo='compromisso',
        titulo='Novo compromisso',
        mensagem=f'Um novo compromisso foi adicionado: {titulo}',
        url_redirecionamento=url_redirecionamento,
        objeto_tipo='compromisso'
    )


def criar_notificacao_orcamento(usuario_destino, usuario_remetente, tipo_acao, servico_nome, url_redirecionamento=None):
    """
    Cria uma notificação relacionada a orçamentos
    
    tipo_acao pode ser: 'solicitacao', 'resposta', 'aceito', 'recusado', 'mensagem'
    """
    if not url_redirecionamento:
        url_redirecionamento = '/servicos/minhas-solicitacoes-organizador/'
    
    mensagens = {
        'solicitacao': f'{usuario_remetente.get_full_name() or usuario_remetente.username} solicitou um orçamento para "{servico_nome}"',
        'resposta': f'{usuario_remetente.get_full_name() or usuario_remetente.username} enviou um orçamento para "{servico_nome}"',
        'aceito': f'{usuario_remetente.get_full_name() or usuario_remetente.username} aceitou seu orçamento para "{servico_nome}"',
        'recusado': f'{usuario_remetente.get_full_name() or usuario_remetente.username} recusou seu orçamento para "{servico_nome}"',
        'mensagem': f'{usuario_remetente.get_full_name() or usuario_remetente.username} enviou uma mensagem sobre o orçamento de "{servico_nome}"',
    }
    
    titulos = {
        'solicitacao': 'Nova solicitação de orçamento',
        'resposta': 'Orçamento enviado',
        'aceito': 'Orçamento aceito',
        'recusado': 'Orçamento recusado',
        'mensagem': 'Nova mensagem no orçamento',
    }
    
    return Notificacao.criar_notificacao(
        usuario=usuario_destino,
        tipo='orcamento',
        titulo=titulos.get(tipo_acao, 'Atualização de orçamento'),
        mensagem=mensagens.get(tipo_acao, f'Atualização no orçamento de "{servico_nome}"'),
        url_redirecionamento=url_redirecionamento,
        objeto_tipo='orcamento'
    )


def criar_notificacao_personalizada(usuario, tipo, titulo, mensagem, url_redirecionamento=None, objeto_id=None, objeto_tipo=None):
    """Cria uma notificação personalizada"""
    return Notificacao.criar_notificacao(
        usuario=usuario,
        tipo=tipo,
        titulo=titulo,
        mensagem=mensagem,
        url_redirecionamento=url_redirecionamento,
        objeto_id=objeto_id,
        objeto_tipo=objeto_tipo
    )

