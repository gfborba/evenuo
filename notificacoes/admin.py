from django.contrib import admin
from .models import Notificacao

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'titulo', 'lida', 'data_criacao')
    list_filter = ('tipo', 'lida', 'data_criacao')
    search_fields = ('usuario__username', 'titulo', 'mensagem')
    readonly_fields = ('data_criacao',)
    list_editable = ('lida',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'tipo', 'titulo', 'mensagem')
        }),
        ('Redirecionamento', {
            'fields': ('url_redirecionamento', 'objeto_id', 'objeto_tipo')
        }),
        ('Status', {
            'fields': ('lida', 'data_criacao')
        }),
    )
