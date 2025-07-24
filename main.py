
# A importação do logger deve ser a PRIMEIRA para garantir que ele seja configurado.
from logger_config import log

import panel as pn
from crud_vitor_categoria import create_categoria_view
from crud_matheus_usuario import create_usuario_view
from crud_leonardo_aula import create_aula_view
from crud_cinthia_inscricao import create_inscricao_view

log.info("Aplicação iniciada. Configurando extensões do Panel...")
pn.extension('tabulator', notifications=True)

log.info("Criando as visualizações de cada tela...")
view_aulas = create_aula_view()
view_inscricoes = create_inscricao_view()
view_usuarios = create_usuario_view()
view_categorias = create_categoria_view()
log.info("Visualizações criadas com sucesso.")

# Organiza as telas em abas
app_tabs = pn.Tabs(
    ('Gerenciar Aulas', view_aulas),
    ('Gerenciar Inscrições', view_inscricoes),
    ('Gerenciar Usuários', view_usuarios),
    ('Gerenciar Categorias', view_categorias),
    dynamic=True
)

# Cria um template para a aplicação
template = pn.template.FastListTemplate(
    site="Plataforma de Aulas",
    title="Painel de Gerenciamento",
    main=[app_tabs],
    header_background="#007bff",
    accent_base_color="#007bff",
    sidebar_width=200,
)

template.main.append(
    pn.pane.Markdown("--- \n *Protótipo desenvolvido para a disciplina de Fundamentos de Banco de Dados.*")
)

log.info("Template da aplicação pronto para servir.")
template.servable()