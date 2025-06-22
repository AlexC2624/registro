document.addEventListener('DOMContentLoaded', () => {
    // Lógica para exibir alertas de status
    const statusMessageElement = document.getElementById('status-message-manejo');
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

    // Lógica para pré-preencher datas de início e fim (Modo 'alimentacao')
    const dataInicioInput = document.getElementById("data_inicio");
    const dataFimInput = document.getElementById("data_fim");

    if (dataInicioInput && dataFimInput) {
        const hoje = new Date();
        const ano = hoje.getFullYear();
        const mes = String(hoje.getMonth() + 1).padStart(2, '0');
        const dia = String(hoje.getDate()).padStart(2, '0');
        const dataFormatada = `${ano}-${mes}-${dia}`;

        dataInicioInput.value = dataFormatada;
        dataFimInput.value = dataFormatada;
    }

    // Lógica para pré-preencher a data da pesagem (Modo 'pesagem')
    const dataPesagemInput = document.getElementById("data");
    if (dataPesagemInput && !dataInicioInput) { // Verifica se é o campo 'data' da pesagem, não da alimentação
        const hoje = new Date();
        const ano = hoje.getFullYear();
        const mes = String(hoje.getMonth() + 1).padStart(2, '0');
        const dia = String(hoje.getDate()).padStart(2, '0');
        const dataFormatada = `${ano}-${mes}-${dia}`;
        dataPesagemInput.value = dataFormatada;
    }


    // Lógica para atualizar a label de quantidade com a unidade do insumo e max/placeholder de estoque
    const selInsumo = document.getElementById("insumo");
    const labelQuantidade = document.querySelector("label[for='quantidade']");
    const inputQuantidade = document.getElementById("quantidade");

    // A variável insumo_opcoes_data precisa ser declarada no HTML para ser acessível globalmente.
    // Exemplo: <div id="insumo-options-data" style="display:none;">{{ insumo_opcoes | tojson | safe }}</div>
    // E depois no script inline do HTML: const insumo_opcoes_data = JSON.parse(document.getElementById('insumo-options-data').textContent);

    if (selInsumo && labelQuantidade && inputQuantidade && typeof insumo_opcoes_data !== 'undefined') {
        selInsumo.addEventListener("change", function () {
            let insumoSelecionadoId = Number(this.value); // Convertendo para número
            if (insumo_opcoes_data[insumoSelecionadoId]) {
                labelQuantidade.textContent = `Quantidade (${insumo_opcoes_data[insumoSelecionadoId]['unidade']}):`;
                inputQuantidade.placeholder = `Em estoque: ${insumo_opcoes_data[insumoSelecionadoId]['estoque']}`;
                inputQuantidade.max = insumo_opcoes_data[insumoSelecionadoId]['estoque'];
            } else {
                labelQuantidade.textContent = "Quantidade:";
                inputQuantidade.placeholder = "Ex: 75.0"; // Placeholder padrão se não encontrar insumo
                inputQuantidade.removeAttribute('max'); // Remove o max se não tiver insumo selecionado
            }
        });

        // Dispara o evento 'change' ao carregar a página se já houver um insumo selecionado
        // Isso é útil se o formulário for recarregado com dados pré-preenchidos (e.g., erro de validação)
        if (selInsumo.value) {
            selInsumo.dispatchEvent(new Event('change'));
        }
    }
});
