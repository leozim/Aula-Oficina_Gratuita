# Protótipo de Aplicação - Aulas e Oficinas Gratuitas

Este projeto é um protótipo de aplicação em Python com interface gráfica para gerenciar o banco de dados `AULA_OFICINA_GRATUITA`. Ele permite realizar operações de CRUD (Criar, Ler, Atualizar, Excluir) em diferentes tabelas do sistema.

## 🛠️ Estrutura do Projeto

O projeto está organizado nos seguintes arquivos:

- **`main.py`**: Ponto de entrada da aplicação. Organiza as diferentes telas em abas.
- **`database.py`**: Centraliza a configuração e a conexão com o banco de dados PostgreSQL.
- **`crud_leonardo_usuario.py`**: Tela para o gerenciamento de **Usuários**.
- **`crud_matheus_aula.py`**: Tela para o gerenciamento de **Aulas e Oficinas**.
- **`crud_cinthia_inscricao.py`**: Tela para o gerenciamento de **Inscrições**.
- **`crud_vitor_categoria.py`**: Tela para o gerenciamento de **Categorias**.
- **`requirements.txt`**: Lista de dependências Python.
- **`.env.example`**: Arquivo de exemplo para as variáveis de ambiente.

## ✅ Pré-requisitos

- Python 3.8 ou superior
- Banco de dados PostgreSQL ativo com o schema do projeto já criado.

## ⚙️ Configuração do Ambiente

1.  **Crie e ative um ambiente virtual:**
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

2.  **Instale as dependências:**
    Crie o arquivo `requirements.txt` (conteúdo abaixo) e execute:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as variáveis de ambiente:**
    - Crie uma cópia do arquivo `.env.example` e renomeie para `.env`.
    - Preencha o arquivo `.env` com as credenciais do seu banco de dados PostgreSQL. O nome do banco de dados deve ser `AULA_OFICINA_GRATUITA`.

## 🚀 Como Executar a Aplicação

Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando no terminal:

```bash
panel serve main.py --autoreload --show