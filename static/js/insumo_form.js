document.addEventListener('DOMContentLoaded', () => {
    // Lógica para exibir alertas de status
    const statusMessageElement = document.getElementById('status-message-insumo');
    if (statusMessageElement) {
        try {
            const statusText = JSON.parse(statusMessageElement.textContent);
            if (statusText) {
                alert(statusText);
            }
            // A linha abaixo causa o window.history.back() se houver status.
            // Se você quer que o alerta apareça e a página não volte, remova-a.
            window.history.back();
        } catch (e) {
            console.error("Erro ao parsear a mensagem de status:", e);
        }
    }

    // Lógica para pré-preencher a data da compra
    const dataCompraInput = document.getElementById("data");
    if (dataCompraInput) {
        const hoje = new Date();
        const ano = hoje.getFullYear();
        const mes = String(hoje.getMonth() + 1).padStart(2, '0');
        const dia = String(hoje.getDate()).padStart(2, '0');
        const dataFormatada = `${ano}-${mes}-${dia}`;
        dataCompraInput.value = dataFormatada;
    }

    // Lógica para atualizar a label de quantidade com a unidade do insumo
    const selInsumo = document.getElementById("insumo");
    const labelQuantidade = document.querySelector("label[for='quantidade']");

    // Verifica se os elementos existem (para evitar erros em modos 'novo' ou 'consumo')
    if (selInsumo && labelQuantidade && typeof insumo_opcoes_data !== 'undefined') {
        selInsumo.addEventListener("change", function () {
            let insumoSelecionadoId = Number(this.value); // Convertendo para número
            if (insumo_opcoes_data[insumoSelecionadoId]) {
                labelQuantidade.textContent = `Quantidade (${insumo_opcoes_data[insumoSelecionadoId]['unidade']}):`;
            } else {
                labelQuantidade.textContent = "Quantidade:";
            }
        });

        // Trigger the change event on load if an option is pre-selected (e.g., after a form submission error)
        if (selInsumo.value) {
            selInsumo.dispatchEvent(new Event('change'));
        }
    }
});

// A variável insumo_opcoes_data é declarada no HTML para ser acessível globalmente.
// Exemplo: <div id="insumo-options-data" style="display:none;">{{ insumo_opcoes | tojson | safe }}</div>
// E depois no script inline do HTML: const insumo_opcoes_data = JSON.parse(document.getElementById('insumo-options-data').textContent);
