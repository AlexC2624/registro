# Registro

Um projeto para gerenciar e registrar informações importantes de forma simples e eficiente.

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

5. **Comandos extras**
    #### Liste as branch atuais localmente, remotamente e a selecionada:
    ```bash
    git branch -a
    ```
    #### Altere de branch:
    ```bash
    git checkout nome-da-branch
    ```
    #### Atualizar as referências ao remoto
    ```bash
    git pull
    ```
        
## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.