document.getElementById('chatInput').addEventListener('focus', function() {
    this.scrollIntoView(false);
  });
 
  document.getElementById('chatBody').scrollTop = document.getElementById('chatBody').scrollHeight;
  
  const chatInput = document.getElementById('chatInput');

  // chatInput.addEventListener('keypress', function(event) {
  //   if (event.key === 'Enter') {
  //     event.preventDefault();
  //     sendMessage();
  //   }
  // });

  function sendMessage() {
    const message = chatInput.value.trim();
    if (message !== '') {
      // Envia a mensagem para o servidor ou faz o que você precisa fazer para enviar a mensagem
      console.log(`Mensagem enviada: ${message}`);
      chatInput.value = '';
    }
  }


  // Função para adicionar uma nova mensagem ao chat
  function addMessage(message, className) {
    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    messageElement.classList.add(className); // Adiciona a classe apropriada

    const chatBody = document.getElementById('chatBody');
    chatBody.appendChild(messageElement);
    // Atualizar o scroll para o final
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  document.getElementById('chatInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage();
    }
  });


  // Chamando a função exemplo de adicionar mensagem do
  const chatbox = document.getElementById('chatbox');


