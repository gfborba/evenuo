// ---------------------------- Sistema de Notificações ----------------------------
(function() {
    'use strict';
    
    const NOTIFICATION_API_BASE = '/notificacoes/';
    let notificationCheckInterval = null;
    
    //Elementos DOM
    const notificationToggle = document.getElementById('notification-toggle');
    const notificationDropdown = document.getElementById('notification-dropdown');
    const notificationList = document.getElementById('notification-list');
    const notificationBadge = document.getElementById('notification-badge');
    const notificationEmpty = document.getElementById('notification-empty');
    const markAllReadBtn = document.getElementById('mark-all-read');
    
    //Verificar se os elementos existem
    if (!notificationToggle || !notificationDropdown) {
        return;
    }
    
    //Toggle do dropdown
    notificationToggle.addEventListener('click', function(e) {
        e.preventDefault();
        notificationDropdown.classList.toggle('show');
        
        if (notificationDropdown.classList.contains('show')) {
            carregarNotificacoes();
        }
    });
    
    //Fechar dropdown ao clicar fora
    document.addEventListener('click', function(e) {
        if (!notificationToggle.contains(e.target) && !notificationDropdown.contains(e.target)) {
            notificationDropdown.classList.remove('show');
        }
    });
    
    //Carregar notificações
    function carregarNotificacoes() {
        fetch(NOTIFICATION_API_BASE + 'listar/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                atualizarBadge(data.total_nao_lidas);
                renderizarNotificacoes(data.notificacoes);
            })
            .catch(error => {
                console.error('Erro ao carregar notificações:', error);
                notificationList.innerHTML = '<div class="notification-error">Erro ao carregar notificações</div>';
            });
    }
    
    //Renderizar notificações
    function renderizarNotificacoes(notificacoes) {
        if (notificacoes.length === 0) {
            notificationList.style.display = 'none';
            notificationEmpty.style.display = 'block';
            markAllReadBtn.style.display = 'none';
            return;
        }
        
        notificationList.style.display = 'block';
        notificationEmpty.style.display = 'none';
        
        const temNaoLidas = notificacoes.some(n => !n.lida);
        markAllReadBtn.style.display = temNaoLidas ? 'block' : 'none';
        
        notificationList.innerHTML = notificacoes.map(notif => {
            const classeLida = notif.lida ? 'lida' : '';
            const icone = obterIconePorTipo(notif.tipo);
            
            return `
                <div class="notification-item ${classeLida}" data-id="${notif.id}">
                    <div class="notification-icon-type">${icone}</div>
                    <div class="notification-content">
                        <div class="notification-title">${escapeHtml(notif.titulo)}</div>
                        <div class="notification-message">${escapeHtml(notif.mensagem)}</div>
                        <div class="notification-time">${notif.tempo_relativo}</div>
                    </div>
                    ${!notif.lida ? '<div class="notification-unread-dot"></div>' : ''}
                </div>
            `;
        }).join('');
        
        //Adicionar event listeners aos itens
        notificationList.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', function() {
                const notifId = this.dataset.id;
                const notif = notificacoes.find(n => n.id == notifId);
                
                if (notif && !notif.lida) {
                    marcarComoLida(notifId);
                }
                
                if (notif && notif.url && notif.url !== '#') {
                    window.location.href = notif.url;
                }
            });
        });
    }
    
    //Marcar notificação como lida
    function marcarComoLida(notificacaoId) {
        fetch(NOTIFICATION_API_BASE + notificacaoId + '/marcar-lida/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            atualizarBadge(data.total_nao_lidas);
            const item = notificationList.querySelector(`[data-id="${notificacaoId}"]`);
            if (item) {
                item.classList.add('lida');
                const dot = item.querySelector('.notification-unread-dot');
                if (dot) dot.remove();
            }
        })
        .catch(error => console.error('Erro ao marcar como lida:', error));
    }
    
    //Marcar todas como lidas
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            
            fetch(NOTIFICATION_API_BASE + 'marcar-todas-lidas/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                atualizarBadge(0);
                carregarNotificacoes();
            })
            .catch(error => console.error('Erro ao marcar todas como lidas:', error));
        });
    }
    
    //Atualizar badge
    function atualizarBadge(count) {
        if (count > 0) {
            notificationBadge.textContent = count > 99 ? '99+' : count;
            notificationBadge.style.display = 'inline-flex';
        } else {
            notificationBadge.style.display = 'none';
        }
    }
    
    //Obter ícone por tipo
    function obterIconePorTipo(tipo) {
        const icones = {
            'chat': '<i class="bi bi-chat-dots"></i>',
            'pergunta': '<i class="bi bi-question-circle"></i>',
            'resposta': '<i class="bi bi-reply"></i>',
            'avaliacao': '<i class="bi bi-star"></i>',
            'compromisso': '<i class="bi bi-calendar-event"></i>',
            'orcamento': '<i class="bi bi-cash-coin"></i>',
            'comentario_servico': '<i class="bi bi-chat-square-text"></i>',
            'outro': '<i class="bi bi-bell"></i>'
        };
        return icones[tipo] || icones['outro'];
    }
    
    //Funções auxiliares
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        //Se não encontrou no cookie, tenta pegar do formulário
        if (!cookieValue) {
            const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfInput) {
                cookieValue = csrfInput.value;
            }
        }
        return cookieValue;
    }
    
    //Verifica notificações periodicamente 
    function iniciarVerificacaoPeriodica() {
        atualizarContador();
        notificationCheckInterval = setInterval(atualizarContador, 30000);
    }
    
    function atualizarContador() {
        fetch(NOTIFICATION_API_BASE + 'contar/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                atualizarBadge(data.total_nao_lidas);
            })
            .catch(error => {
                //Silenciar erros 403 (não autenticado) e 404
                if (error.message && !error.message.includes('403') && !error.message.includes('404')) {
                    console.error('Erro ao atualizar contador:', error);
                }
            });
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', iniciarVerificacaoPeriodica);
    } else {
        iniciarVerificacaoPeriodica();
    }
    
    window.addEventListener('beforeunload', function() {
        if (notificationCheckInterval) {
            clearInterval(notificationCheckInterval);
        }
    });
})();

