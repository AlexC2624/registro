// animal_form.js

// Script para pré-preencher datas
document.addEventListener('DOMContentLoaded', () => {
    const hoje = new Date();
    const ano = hoje.getFullYear();
    const mes = String(hoje.getMonth() + 1).padStart(2, '0'); // meses de 0 a 11
    const dia = String(hoje.getDate()).padStart(2, '0');
    const dataFormatada = `${ano}-${mes}-${dia}`;

    const dataEntradaInput = document.getElementById("data_entrada");
    if (dataEntradaInput) {
        dataEntradaInput.value = dataFormatada;
    }

    const dataSaidaInput = document.getElementById("data_saida");
    if (dataSaidaInput) {
        dataSaidaInput.value = dataFormatada;
    }
});


// Lógica para formulário de Saída de Animal
// Os dados animal_entrada_opcoes precisam ser passados globalmente (ver HTML modificado)
// Exemplo: const animal_entrada_opcoes = JSON.parse(document.getElementById('animal-data').textContent);

// Seleção dos elementos do DOM
const loteEntrada = document.getElementById("lote_entrada");
const tabelaAnimais = document.getElementById("tabelaAnimais");
const checkboxMestre = document.getElementById("selecionar_todos");
const formAnimais = document.getElementById("form-animais");

if (loteEntrada && tabelaAnimais && checkboxMestre && formAnimais) {
    loteEntrada.addEventListener('change', function () {
        const selecionado = Number(this.value);

        tabelaAnimais.innerHTML = ""; // Limpa a tabela
        if (selecionado) {
            // animal_entrada_opcoes precisa estar disponível aqui
            if (typeof animal_entrada_opcoes !== 'undefined' && animal_entrada_opcoes.length > 0) {
                animal_entrada_opcoes.forEach(function (linha) {
                    if (linha[1] === selecionado) {
                        const tb_tr = document.createElement("tr");

                        // coluna 1 - checkbox
                        const tb_td = document.createElement("td");
                        const tb_input = document.createElement("input");
                        tb_input.type = "checkbox";
                        tb_input.name = "animaisSelecionados[]";
                        tb_input.value = linha[0];
                        tb_td.appendChild(tb_input);
                        tb_input.classList.add("linha-checkbox");

                        // Outras colunas (ID, Raça, Fornecedor, Peso, Valor, Data de Entrada)
                        // Você pode simplificar a criação de TDs se preferir
                        const colunas = [linha[0], linha[2], linha[4], linha[6] + 'kg', 'R$' + linha[7], linha[5]];
                        colunas.forEach(text => {
                            const td = document.createElement("td");
                            td.textContent = text;
                            tb_tr.appendChild(td);
                        });

                        tb_tr.insertBefore(tb_td, tb_tr.firstChild); // Adiciona o checkbox como primeira coluna
                        tabelaAnimais.appendChild(tb_tr);
                    }
                });
            } else {
                console.warn("animal_entrada_opcoes não está definido ou está vazio.");
            }
        }
        // Após carregar os animais, desmarca o checkbox mestre
        desmarcarTodos();
    });

    function marcarTodos() {
        document.querySelectorAll(".linha-checkbox").forEach(cb => cb.checked = true);
        checkboxMestre.checked = true;
    }

    function desmarcarTodos() {
        document.querySelectorAll(".linha-checkbox").forEach(cb => cb.checked = false);
        checkboxMestre.checked = false;
    }

    checkboxMestre.addEventListener("change", () => {
        if (checkboxMestre.checked) {
            marcarTodos();
        } else {
            desmarcarTodos();
        }
    });

    // Adiciona evento de mudança a todos os checkboxes de linha para atualizar o mestre
    // Isso deve ser feito após a tabela ser populada
    tabelaAnimais.addEventListener('change', (event) => {
        if (event.target.classList.contains('linha-checkbox')) {
            atualizarCheckboxMestre();
        }
    });

    function atualizarCheckboxMestre() {
        const todos = document.querySelectorAll(".linha-checkbox");
        const marcados = document.querySelectorAll(".linha-checkbox:checked");
        // O checkbox mestre é marcado se todos os sub-checkboxes estiverem marcados,
        // E somente se houver algum checkbox (para evitar marcar se a lista estiver vazia)
        checkboxMestre.checked = todos.length > 0 && todos.length === marcados.length;
    }

    // Validação de envio do formulário de saída
    formAnimais.addEventListener("submit", function (event) {
        const selecionados = document.querySelectorAll("input[name='animaisSelecionados[]']:checked");

        if (selecionados.length === 0) {
            event.preventDefault();  // Impede o envio
            alert("Selecione pelo menos um animal antes de enviar.");
        }
    });
}


// Lógica para exibição de status/alertas
// Esta parte requer que 'status' seja uma variável global ou que o JS seja carregado após o Jinja2 processar
// e inserir o valor de 'status' no HTML (melhor abordagem).
const statusElement = document.getElementById('status-message');
if (statusElement) {
    const statusText = statusElement.textContent;
    if (statusText === 'voltar') {
        window.history.back();
    } else if (statusText) {
        alert(statusText);
    }
    // Sempre volta após o alerta, a menos que 'status' não exista ou seja vazio.
    // Se o 'status' for apenas para exibir e não voltar, remova a linha abaixo
    if (statusText) { // Apenas volta se houver uma mensagem de status
       window.history.back();
    }
}