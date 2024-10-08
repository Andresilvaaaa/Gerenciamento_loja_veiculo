document.getElementById('logout-link').addEventListener('click', async function(event) {
    event.preventDefault();  // Evita o comportamento padrão do link

    try {
        const response = await fetch('/logout', {
            method: 'POST',  // Ou GET se preferir
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'  // Certifica-se de que os cookies estão sendo enviados
        });

        if (response.ok) {
            alert('Logout realizado com sucesso');
            // Redireciona o usuário para a página de login ou página inicial
            window.location.href = '/';
        } else {
            alert('Erro ao realizar logout');
        }
    } catch (error) {
        console.error('Erro ao tentar fazer logout:', error);
    }
});
