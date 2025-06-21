# Registro

Este projeto salva dados em relação ao manejo do gado de corte e tem IA integrada para responder as perguntas referentes aos dados cadastrados. Foi desenvolvido para poder verificar o lucro, gargalos, perdas e pontos de melhoria, para diminuir custos e aumentar o lucro.

## Sumário
- [Tecnologias usadas](#tecnologias)
- [Como usar](#como-usar)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Funcionalidades

- Cadastro de registros
- Edição e exclusão de registros
- Busca e filtragem de informações

## Tecnologias

- socket
- os
- pandas
- json
- shutil
- flask
    - Flask
    - render_template
    - request
    - redirect
    - url_for
    - send_from_directory
- flasgger
    - Swagger
- [UIVerse](https://uiverse.io/) – Biblioteca de componentes visuais (HTML + CSS) para estilização da interface

## Como usar

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/AlexC2624/registro.git
    cd registro
    ```

2. **Crie e ative um ambiente virtual (recomendado):**

    **No Linux/macOS:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    **No Windows (CMD):**
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate
    ```

    > Após ativar, o terminal deverá exibir algo como `(.venv)` no início da linha.

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o projeto:**
    ```bash
    python main.py
    ```

5. **Abra no navegador:**
    ```navegador
    http://127.0.0.1:50002
        
## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

[Início](#registro)
