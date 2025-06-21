# 📋 Fluxograma Detalhado - Sistema de Gestão de Gado de Corte

## Início
⬇️  
**O que deseja fazer?**

---

## 🔹 [1] Cadastrar
➡️ Deseja cadastrar algum dado?

- 📌 **Animal**
  - ➡️ Preencher: Nome, Raça, Peso, Data de Entrada, Origem
  - 💾 Salvar em: `animal_comprado.csv`

- 📌 **Insumo**
  - ➡️ Preencher: Nome, Unidade, Fornecedor
  - 💾 Salvar em: `insumo_dados.csv`

- 📌 **Fornecedor**
  - ➡️ Preencher: Nome, Contato, Produto
  - 💾 Salvar em: `fornecedor.csv`

---

## 🔹 [2] Registrar Movimentação de Animais
➡️ Deseja registrar movimentação de animal?

- 📌 **Entrada de Animal (compra ou nascimento)**
  - ➡️ Preencher: Data, Nome, Peso, Preço, Fornecedor
  - 💾 Salvar em: `animal_comprado.csv`

- 📌 **Saída por Venda**
  - ➡️ Preencher: ID do Animal, Data, Peso, Preço, Comprador
  - 💾 Salvar em: `animal_vendido.csv`

- 📌 **Morte ou Descarte**
  - ➡️ Preencher: ID do Animal, Data, Motivo
  - 🔁 Atualizar o estoque (sem registro de venda)

---

## 🔹 [3] Registrar Movimentação de Insumos
➡️ Deseja registrar entrada ou consumo de insumo?

- 📌 **Compra de Insumo**
  - ➡️ Preencher: Insumo, Quantidade, Valor Unitário, Data
  - 💾 Salvar em: `insumo_comprado.csv`

- 📌 **Consumo de Insumo**
  - ➡️ Preencher: Insumo, Quantidade, Data, Observações
  - 💾 Salvar em: `insumo_consumo.csv`

---

## 🔹 [4] Consultar Estoque
➡️ Deseja consultar o estoque atual?

- 📌 **Estoque de Animais**
  - 🔍 Calcular saldo a partir de:
    - Entradas: `animal_comprado.csv`
    - Saídas: `animal_vendido.csv`

- 📌 **Estoque de Insumos**
  - 🔍 Calcular saldo a partir de:
    - Entradas: `insumo_comprado.csv`
    - Consumos: `insumo_consumo.csv`

---

## 🔹 [5] Consultar Financeiro
➡️ Deseja consultar dados financeiros?

- 📌 **Receitas**
  - 🔍 Vendas registradas em: `animal_vendido.csv`

- 📌 **Despesas**
  - 🔍 Compras de insumos e outros custos em: `insumo_comprado.csv` e extras

- 📌 **Lucro ou Prejuízo**
  - 🧮 Receita Total - Despesa Total = Resultado do Período

---

## 🔹 [6] Emitir Relatórios
➡️ Que tipo de relatório deseja gerar?

- 📄 **Relatório de Desempenho dos Animais**
  - Ganho de peso, tempo de permanência, origem e destino

- 📄 **Relatório Financeiro**
  - Resumo de receitas, despesas e lucro por período (mês, ano)

- 📄 **Relatório de Estoque**
  - Quantidade atual de insumos e animais
  - Consumo médio e necessidade de reposição

---

## 🔹 [7] Sair do Sistema
➡️ Deseja encerrar o sistema?
- ✅ Sim → Encerrar
- 🔁 Não → Voltar ao Menu Principal
