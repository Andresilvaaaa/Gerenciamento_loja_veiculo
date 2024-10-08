// document.getElementById('linkHome').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/home';  // Redireciona para Home
// });

// document.getElementById('linkDashboard').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/dashboard';  // Redireciona para Dashboard
// });

// document.getElementById('linkFaturamento').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/faturamento';  // Redireciona para Faturamento
// });

// document.getElementById('linkServices').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/services';  // Redireciona para Serviços
// });

// document.getElementById('linkMinhaConta').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/minha_conta';  // Redireciona para Minha Conta
// });

// document.getElementById('linkCalendar').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/clientepf';  // Redireciona para Calendário
// });

// document.getElementById('linkCalendar').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/clientepj';  // Redireciona para Calendário
// });

// document.getElementById('linkAbout').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/about';  // Redireciona para Sobre
// });

// document.getElementById('linkFeedback').addEventListener('click', function(event) {
//     event.preventDefault();  // Evita comportamento padrão
//     window.location.href = '/feedback';  // Redireciona para Feedback
// });

document.addEventListener('DOMContentLoaded', function() {
    var linkHome = document.getElementById('linkHome');
    if (linkHome) {
        linkHome.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/home';  // Redireciona para Home
        });
    }

    var linkDashboard = document.getElementById('linkDashboard');
    if (linkDashboard) {
        linkDashboard.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/dashboard';  // Redireciona para Dashboard
        });
    }

    var linkFaturamento = document.getElementById('linkFaturamento');
    if (linkFaturamento) {
        linkFaturamento.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/faturamento';  // Redireciona para Faturamento
        });
    }

    var linkServices = document.getElementById('linkServices');
    if (linkServices) {
        linkServices.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/services';  // Redireciona para Serviços
        });
    }

    var linkMinhaConta = document.getElementById('linkMinhaConta');
    if (linkMinhaConta) {
        linkMinhaConta.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/minha_conta';  // Redireciona para Minha Conta
        });
    }

    var linkClientepf = document.getElementById('linkClientepf');
    if (linkClientepf) {
        linkClientepf.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/clientepf';  // Redireciona para Cliente PF
        });
    }

    // var linkClientepj = document.getElementById('linkClientepj');
    // if (linkClientepj) {
    //     linkClientepj.addEventListener('click', function(event) {
    //         event.preventDefault();  // Evita comportamento padrão
    //         window.location.href = '/clientepj';  // Redireciona para Cliente PJ
    //     });
    // }
    var linkEnviardocumentos = document.getElementById('linkEnviardocumentos');
    if (linkEnviardocumentos) {
        linkEnviardocumentos.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/enviar_documentos';  // Redireciona para Cliente PJ
        });
    }

    var linkveiculo = document.getElementById('linkveiculo');
    if (linkveiculo) {
        linkveiculo.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/veiculo';  // Redireciona para veiculo
        });
    }

    var linkFeedback = document.getElementById('linkFeedback');
    if (linkFeedback) {
        linkFeedback.addEventListener('click', function(event) {
            event.preventDefault();  // Evita comportamento padrão
            window.location.href = '/feedback';  // Redireciona para Feedback
        });
    }
});
