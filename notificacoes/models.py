from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('chat', 'Nova Mensagem no Chat'),
        ('pergunta', 'Nova Pergunta em Evento'),
        ('resposta', 'Resposta à Pergunta'),
        ('avaliacao', 'Nova Avaliação'),
        ('compromisso', 'Novo Compromisso na Agenda'),
        ('orcamento', 'Solicitação/Atualização de Orçamento'),
        ('comentario_servico', 'Comentário em Serviço'),
        ('outro', 'Outro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    url_redirecionamento = models.CharField(max_length=500, blank=True, null=True)
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    #Campos opcionais para referência a objetos relacionados
    objeto_id = models.PositiveIntegerField(null=True, blank=True)
    objeto_tipo = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        indexes = [
            models.Index(fields=['usuario', 'lida']),
            models.Index(fields=['-data_criacao']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    def marcar_como_lida(self):
        """Marca a notificação como lida"""
        self.lida = True
        self.save(update_fields=['lida'])
    
    @classmethod
    def criar_notificacao(cls, usuario, tipo, titulo, mensagem, url_redirecionamento=None, objeto_id=None, objeto_tipo=None):
        return cls.objects.create(
            usuario=usuario,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            url_redirecionamento=url_redirecionamento,
            objeto_id=objeto_id,
            objeto_tipo=objeto_tipo
        )
    
    @classmethod
    def contar_nao_lidas(cls, usuario):
        """Retorna o número de notificações não lidas do usuário"""
        return cls.objects.filter(usuario=usuario, lida=False).count()
