// document.addEventListener("DOMContentLoaded", function() {
//   // Mapeamento das rotas do site
//   const routes = {
//       home: "/",
//       cadastro: "/cadastrando",
//       sobre: "/quem_somos",
//       contato: "/contato",
//       pagina_logada: '/pagina_logada',
//       dashboard:  '/dashboard'
//   };

//   // Função para navegar para uma página
//   function navigateTo(page) {
//       if (routes[page]) {
//           window.location.href = routes[page];
//       } else {
//           console.error("Página não encontrada: " + page);
//       }
//   }

//   // Adiciona eventos de clique nos links de navegação
//   document.querySelectorAll("nav a").forEach(function(link) {
//       link.addEventListener("click", function(event) {
//           event.preventDefault();
//           const page = this.getAttribute("data-page");
//           navigateTo(page);
//       });
//   });

  // ===================================================== CHAT ICON =====================================================

  function toggleChat() {
      const chatWindow = document.getElementById('chatWindow');
      if (chatWindow) {
          chatWindow.style.display = chatWindow.style.display === 'none' || chatWindow.style.display === '' ? 'flex' : 'none';
      } else {
          console.error("Janela de chat não encontrada");
      }
  }

  const chatInput = document.getElementById('chatInput');
  if (chatInput) {
      chatInput.addEventListener('keypress', function(event) {
          if (event.key === 'Enter') {
              event.preventDefault();
              sendMessageDirect();
          }
      });
  } else {
      console.error("Campo de entrada do chat não encontrado");
  }

  function sendMessageDirect() {
      const chatInput = document.getElementById('chatInput');
      const chatBody = document.getElementById('chatBody');

      if (chatInput && chatBody) {
          const message = chatInput.value.trim();

          if (message) {
              const messageElement = document.createElement('p');
              messageElement.textContent = message;
              chatBody.appendChild(messageElement);
              chatInput.value = '';
              chatBody.scrollTop = chatBody.scrollHeight; // Scroll para a última mensagem
          }
      } else {
          console.error("Campo de entrada ou corpo do chat não encontrados");
      }
  }
//});  // <-- Fechamento correto do bloco DOMContentLoaded


// ===================================================== LOGOUT =====================================================

// // Função para gerenciar o logout
// function logout() {
//     // Remove o token JWT armazenado no localStorage
//     localStorage.removeItem('token');

//     // Opcional: fazer uma requisição para o backend se você quiser invalidar o JWT
//     fetch('/logout', { method: 'POST' })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data.msg); // Opcional: logar a mensagem de sucesso
//             window.location.href = '/'; // Redireciona para a página de login
//         })
//         .catch(error => {
//             console.error('Erro ao fazer logout:', error);
//             window.location.href = '/'; // Redireciona mesmo que ocorra erro
//         });
// }

// // Espera que o DOM esteja completamente carregado
// document.addEventListener('DOMContentLoaded', function() {
//     // Adiciona o evento de clique ao link de logout
//     const logoutLink = document.getElementById('logout-link');
//     if (logoutLink) {
//         logoutLink.addEventListener('click', function(event) {
//             event.preventDefault(); // Previne o comportamento padrão do link
//             logout(); // Chama a função de logout
//         });
//     }
// });

function logout() {
    // Envia uma requisição de logout para o backend
    fetch('/logout', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.msg);
            localStorage.removeItem('token'); // Limpa o token
            window.location.href = '/'; // Redireciona para a página de login
        })
        .catch(error => console.error('Erro ao fazer logout:', error));
}
