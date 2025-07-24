
import panel as pn
import pandas as pd
from sqlalchemy import text
from database import engine, con
from logger_config import log


def create_categoria_view():
    log.info("Inicializando a tela de gerenciamento de Categorias.")
    id_categoria = pn.widgets.TextInput(name='ID da Categoria', disabled=True)
    nome_categoria = pn.widgets.TextInput(name='Nome da Categoria')
    descricao_categoria = pn.widgets.TextAreaInput(name='Descrição')
    filtro_nome = pn.widgets.TextInput(name='Filtrar por Nome', placeholder='Digite para buscar...')

    btn_inserir, btn_atualizar, btn_excluir, btn_consultar = [pn.widgets.Button(name=n, button_type=t) for n, t in
                                                              [('Inserir', 'primary'), ('Atualizar', 'warning'),
                                                               ('Excluir', 'danger'), ('Consultar', 'default')]]

    tabela_categorias = pn.widgets.Tabulator(None, layout='fit_data_table', disabled=True, page_size=10,
                                             selectable=True)

    def carregar_dados(event=None):
        log.info("Ação: carregar_dados (Categorias)")
        params = {}
        query = text("SELECT * FROM categoria")
        if filtro_nome.value:
            query = text("SELECT * FROM categoria WHERE nome_categoria ILIKE :nome")
            params['nome'] = f"%{filtro_nome.value}%"
        try:
            df = pd.read_sql_query(query, engine, params=params)
            tabela_categorias.value = df
            if event:
                limpar_campos()
        except Exception:
            log.exception("ERRO ao carregar categorias!")
            pn.state.notifications.error('Erro ao carregar categorias. Verifique o console.')

    def limpar_campos(event=None):
        id_categoria.value, nome_categoria.value, descricao_categoria.value = '', '', ''
        tabela_categorias.selection = []  # Limpa a seleção na tabela

    def inserir_action(event):
        log.info(f"Ação: inserir_action (Categoria) com nome='{nome_categoria.value}'")
        if not nome_categoria.value:
            pn.state.notifications.warning('O nome da categoria é obrigatório.')
            return
        try:
            cursor = con.cursor()
            cursor.execute("INSERT INTO categoria (nome_categoria, descricao_categoria) VALUES (%s, %s)",
                           (nome_categoria.value, descricao_categoria.value))
            con.commit()
            cursor.close()
            pn.state.notifications.success('Categoria inserida com sucesso!')
            carregar_dados()
        except Exception:
            log.exception("ERRO ao inserir categoria!")
            con.rollback()
            pn.state.notifications.error('Erro ao inserir. Verifique o console.')

    def atualizar_action(event):
        log.info(f"Ação: atualizar_action (Categoria) para ID={id_categoria.value}")
        if not id_categoria.value:
            pn.state.notifications.warning('Selecione uma categoria para atualizar.')
            return
        try:
            cursor = con.cursor()
            cursor.execute("UPDATE categoria SET nome_categoria=%s, descricao_categoria=%s WHERE id_categoria=%s",
                           (nome_categoria.value, descricao_categoria.value, int(id_categoria.value)))
            con.commit()
            cursor.close()
            pn.state.notifications.success('Categoria atualizada com sucesso!')
            carregar_dados()
        except Exception:
            log.exception(f"ERRO ao atualizar categoria ID={id_categoria.value}!")
            con.rollback()
            pn.state.notifications.error('Erro ao atualizar. Verifique o console.')

    def excluir_action(event):
        log.info(f"Ação: excluir_action (Categoria) para ID={id_categoria.value}")
        if not id_categoria.value:
            pn.state.notifications.warning('Selecione uma categoria para excluir.')
            return
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM categoria WHERE id_categoria=%s", (int(id_categoria.value),))
            con.commit()
            cursor.close()
            pn.state.notifications.success('Categoria excluída com sucesso!')
            carregar_dados()
        except Exception:
            log.exception(f"ERRO ao excluir categoria ID={id_categoria.value}!")
            con.rollback()
            pn.state.notifications.error('Erro ao excluir. Verifique o console.')

    def selecionar_linha(event):
        if not event.new:  # Se a lista de seleção estiver vazia
            limpar_campos()
            return

        indice_selecionado = event.new[0]  # Pega o índice da primeira linha selecionada
        linha_data = tabela_categorias.value.iloc[indice_selecionado]

        log.info(f"Linha selecionada (Categoria): {linha_data.to_dict()}")
        id_categoria.value = str(linha_data['id_categoria'])
        nome_categoria.value = linha_data['nome_categoria']
        descricao_categoria.value = linha_data['descricao_categoria']

    btn_consultar.on_click(carregar_dados)
    btn_inserir.on_click(inserir_action)
    btn_atualizar.on_click(atualizar_action)
    btn_excluir.on_click(excluir_action)

    tabela_categorias.param.watch(selecionar_linha, 'selection')

    carregar_dados()

    layout = pn.Column(
        pn.Row(filtro_nome, btn_consultar, align='end'),
        tabela_categorias,
        pn.Row(
            pn.Column("### Formulário de Categoria", id_categoria, nome_categoria, descricao_categoria),
            pn.Column("### Ações", pn.Row(btn_inserir, btn_atualizar, btn_excluir))
        )
    )
    return layout