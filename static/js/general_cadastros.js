// Lógica para exibir alertas de status em páginas de cadastro genéricas
document.addEventListener('DOMContentLoaded', () => {
    const statusMessageElement = document.getElementById('status-message-general');
    if (statusMessageElement) {
        try {
            const statusText = JSON.parse(statusMessageElement.textContent);
            if (statusText) {
                alert(statusText);
            }
        } catch (e) {
            console.error("Erro ao parsear a mensagem de status:", e);
        }
    }
});
