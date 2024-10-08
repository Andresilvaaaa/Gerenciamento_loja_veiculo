// Função genérica para realizar requisições e tratar erros
function fetchProtectedData(url) {
    fetch(url, {
        method: 'GET',
        credentials: 'include' // Inclui cookies na requisição
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status === 401) {
            // O backend já redireciona em caso de token expirado
            console.warn("Token expirado. Redirecionando para a página de login...");
            window.location.href = "/index.html"; // Redirecionar diretamente
        }
    })
    .then(data => {
        // Manipular dados retornados, se a resposta for válida
        console.log(data);
    })
    .catch(error => {
        console.error("Erro ao buscar dados:", error);
    });
}

// Função para exibir o modal de sessão expirada (caso decida manter)
function showExpiredSessionModal() {
    const modal = document.getElementById('expiredSessionModal');
    if (modal) {
        modal.style.display = 'block';
    } else {
        alert("Sessão expirada. Por favor, faça login novamente.");
        setTimeout(() => {
            window.location.href = "/index.html";
        }, 3000);
    }
}

// Adicionar evento para o botão de redirecionamento, se existir no HTML
document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    if (loginButton) {
        loginButton.addEventListener('click', function() {
            window.location.href = "/index.html";
        });
    }
});
