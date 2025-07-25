
import panel as pn
import pandas as pd
from sqlalchemy import text
from database import engine, con
from logger_config import log
import datetime


def create_aula_view():
    log.info("Inicializando a tela de gerenciamento de Aulas.")

    # --- Funções para popular Selects ---
    def get_instrutores_options():
        try:
            query = "SELECT i.id_usuario, u.pnome || ' ' || u.snome AS nome_completo FROM instrutor i JOIN usuario u ON i.id_usuario = u.id_usuario ORDER BY nome_completo"
            df = pd.read_sql_query(query, engine)
            return list(zip(df['nome_completo'], df['id_usuario']))
        except:
            log.exception("ERRO ao carregar opções de instrutores!")
            return []

    def get_categorias_options():
        try:
            query = "SELECT id_categoria, nome_categoria FROM categoria ORDER BY nome_categoria"
            df = pd.read_sql_query(query, engine)
            return list(zip(df['nome_categoria'], df['id_categoria']))
        except:
            log.exception("ERRO ao carregar opções de categorias!")
            return []

    # --- Widgets e Botões ---
    id_aula = pn.widgets.TextInput(name='ID da Aula', disabled=True)
    titulo = pn.widgets.TextInput(name='Título da Aula')
    select_instrutor = pn.widgets.Select(name='Instrutor', options=get_instrutores_options())
    select_categoria = pn.widgets.Select(name='Categoria', options=get_categorias_options())
    descricao = pn.widgets.TextAreaInput(name='Descrição', min_height=100)
    formato = pn.widgets.RadioBoxGroup(name='Formato', options=['Online', 'Presencial'], inline=True)
    link_aula = pn.widgets.TextInput(name='Link (se Online)')
    logradouro = pn.widgets.TextInput(name='Logradouro (se Presencial)')
    capacidade_maxima = pn.widgets.IntInput(name='Capacidade Máxima', value=10, start=1)
    status_aula = pn.widgets.Select(name='Status',
                                    options=['Rascunho', 'Publicada', 'Em Andamento', 'Concluída', 'Cancelada'])

    data_inicio = pn.widgets.DatePicker(name='Data de Início')
    data_fim = pn.widgets.DatePicker(name='Data de Fim')
    hora_inicio = pn.widgets.TimePicker(name='Hora de Início', format='%H:%M')
    hora_fim = pn.widgets.TimePicker(name='Hora de Fim', format='%H:%M')

    filtro_titulo = pn.widgets.TextInput(name='Filtrar por Título', placeholder='Busque pelo título...')

    btn_inserir, btn_atualizar, btn_excluir, btn_consultar = [pn.widgets.Button(name=n, button_type=t) for n, t in
                                                              [('Inserir', 'primary'), ('Atualizar', 'warning'),
                                                               ('Excluir', 'danger'), ('Consultar', 'default')]]

    tabela_aulas = pn.widgets.Tabulator(None, layout='fit_data_table', disabled=True, page_size=8, selectable=True)

    # --- Funções de Ação ---
    def carregar_dados(event=None):
        params = {}
        query = text(
            "SELECT id_aula, titulo, id_instrutor, id_categoria, formato, status_aula, capacidade_maxima FROM aula_oficina")
        if filtro_titulo.value:
            query = text(
                "SELECT id_aula, titulo, id_instrutor, id_categoria, formato, status_aula, capacidade_maxima FROM aula_oficina WHERE titulo ILIKE :titulo")
            params['titulo'] = f"%{filtro_titulo.value}%"
        try:
            df = pd.read_sql_query(query, engine, params=params)
            tabela_aulas.value = df
            if event:
                limpar_campos()
        except Exception:
            log.exception("ERRO ao carregar aulas!")
            pn.state.notifications.error('Erro ao carregar aulas. Verifique o console.')

    def limpar_campos(event=None):
        id_aula.value, titulo.value, descricao.value, link_aula.value, logradouro.value = '', '', '', '', ''
        capacidade_maxima.value = 10
        data_inicio.value, data_fim.value, hora_inicio.value, hora_fim.value = None, None, None, None
        tabela_aulas.selection = []

    def inserir_action(event):
        instrutor_id = int(select_instrutor.value[1]) if select_instrutor.value else None
        categoria_id = int(select_categoria.value[1]) if select_categoria.value else None

        if not all([titulo.value, instrutor_id, categoria_id, data_inicio.value, data_fim.value, hora_inicio.value,
                    hora_fim.value]):
            pn.state.notifications.warning('Todos os campos, incluindo datas e horas, são obrigatórios.')
            return

        try:
            cursor = con.cursor()
            query_conflito = """
                SELECT titulo FROM aula_oficina
                WHERE id_instrutor = %s
                  AND data_inicio <= %s
                  AND data_fim >= %s
                  AND hora_inicio < %s
                  AND hora_fim > %s
            """
            cursor.execute(query_conflito,
                           (instrutor_id, data_fim.value, data_inicio.value, hora_fim.value, hora_inicio.value))
            aula_conflitante = cursor.fetchone()

            if aula_conflitante:
                pn.state.notifications.error(
                    f'Choque de horário! O instrutor já está alocado na aula "{aula_conflitante[0]}" neste período.')
                cursor.close()
                return
            cursor.close()
        except Exception:
            log.exception("ERRO ao verificar choque de horários do instrutor!")
            pn.state.notifications.error('Erro ao verificar horários. Verifique o console.')
            return

        try:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO aula_oficina (titulo, id_instrutor, id_categoria, descricao_detalhada, formato, link_aula, logradouro, capacidade_maxima, status_aula, data_inicio, data_fim, hora_inicio, hora_fim) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (titulo.value, instrutor_id, categoria_id, descricao.value, formato.value,
                 link_aula.value if formato.value == 'Online' else None,
                 logradouro.value if formato.value == 'Presencial' else None, capacidade_maxima.value,
                 status_aula.value, data_inicio.value, data_fim.value, hora_inicio.value, hora_fim.value)
                )
            con.commit()
            cursor.close()
            pn.state.notifications.success('Aula inserida!')
            carregar_dados()
        except Exception:
            log.exception("ERRO ao inserir aula!")
            con.rollback()
            pn.state.notifications.error('Erro ao inserir. Verifique o console.')

    def atualizar_action(event):
        if not id_aula.value:
            pn.state.notifications.warning('Selecione uma aula para atualizar.')
            return

        instrutor_id = int(select_instrutor.value[1]) if select_instrutor.value else None
        categoria_id = int(select_categoria.value[1]) if select_categoria.value else None
        capacidade = int(capacidade_maxima.value) if capacidade_maxima.value is not None else 0

        if not all([titulo.value, instrutor_id, categoria_id, data_inicio.value, data_fim.value, hora_inicio.value,
                    hora_fim.value]):
            pn.state.notifications.warning('Todos os campos, incluindo datas e horas, são obrigatórios.')
            return

        try:
            cursor = con.cursor()
            aula_atual_id = int(id_aula.value)
            query_conflito = """
                SELECT titulo FROM aula_oficina
                WHERE id_instrutor = %s
                  AND id_aula != %s
                  AND data_inicio <= %s
                  AND data_fim >= %s
                  AND hora_inicio < %s
                  AND hora_fim > %s
            """
            cursor.execute(query_conflito, (
            instrutor_id, aula_atual_id, data_fim.value, data_inicio.value, hora_fim.value, hora_inicio.value))
            aula_conflitante = cursor.fetchone()

            if aula_conflitante:
                pn.state.notifications.error(
                    f'Choque de horário! O instrutor já está alocado na aula "{aula_conflitante[0]}" neste período.')
                cursor.close()
                return
            cursor.close()
        except Exception:
            log.exception("ERRO ao verificar choque de horários na atualização!")
            pn.state.notifications.error('Erro ao verificar horários. Verifique o console.')
            return

        try:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE aula_oficina SET titulo=%s, id_instrutor=%s, id_categoria=%s, descricao_detalhada=%s, formato=%s, link_aula=%s, logradouro=%s, capacidade_maxima=%s, status_aula=%s, data_inicio=%s, data_fim=%s, hora_inicio=%s, hora_fim=%s WHERE id_aula=%s",
                (titulo.value, instrutor_id, categoria_id, descricao.value, formato.value,
                 link_aula.value if formato.value == 'Online' else None,
                 logradouro.value if formato.value == 'Presencial' else None, capacidade, status_aula.value,
                 data_inicio.value, data_fim.value, hora_inicio.value, hora_fim.value, int(id_aula.value))
                )
            con.commit()
            cursor.close()
            pn.state.notifications.success('Aula atualizada!')
            carregar_dados()
        except Exception:
            log.exception(f"ERRO ao atualizar aula ID={id_aula.value}!")
            con.rollback()
            pn.state.notifications.error('Erro ao atualizar. Verifique o console.')

    def excluir_action(event):
        if not id_aula.value:
            pn.state.notifications.warning('Selecione uma aula para excluir.')
            return
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM aula_oficina WHERE id_aula=%s", (int(id_aula.value),))
            con.commit()
            cursor.close()
            pn.state.notifications.success('Aula excluída!')
            carregar_dados()
        except Exception:
            log.exception(f"ERRO ao excluir aula ID={id_aula.value}!")
            con.rollback()
            pn.state.notifications.error('Erro ao excluir. Verifique o console.')

    def selecionar_linha(event):
        if not event.new:
            limpar_campos()
            return

        indice_selecionado = event.new[0]
        linha_selecionada = tabela_aulas.value.iloc[indice_selecionado]
        selected_id = linha_selecionada['id_aula']

        try:
            df_completo = pd.read_sql_query(f"SELECT * FROM aula_oficina WHERE id_aula = {selected_id}", engine)
            if df_completo.empty: return
            linha_data = df_completo.iloc[0]

            id_aula.value = str(linha_data['id_aula'])
            titulo.value = linha_data['titulo']
            descricao.value, formato.value = linha_data['descricao_detalhada'], linha_data['formato']
            link_aula.value = linha_data['link_aula'] if pd.notna(linha_data['link_aula']) else ''
            logradouro.value = linha_data['logradouro'] if pd.notna(linha_data['logradouro']) else ''
            capacidade_maxima.value = int(linha_data['capacidade_maxima'])
            status_aula.value = linha_data['status_aula']

            data_inicio.value = linha_data['data_inicio']
            data_fim.value = linha_data['data_fim']


            hora_inicio.value = linha_data['hora_inicio']
            hora_fim.value = linha_data['hora_fim']

            select_instrutor.value = next(
                (item for item in select_instrutor.options if item[1] == linha_data['id_instrutor']), None)
            select_categoria.value = next(
                (item for item in select_categoria.options if item[1] == linha_data['id_categoria']), None)
        except Exception:
            log.exception(f"ERRO ao buscar detalhes da aula ID={selected_id}!")

    btn_consultar.on_click(carregar_dados)
    btn_inserir.on_click(inserir_action)
    btn_atualizar.on_click(atualizar_action)
    btn_excluir.on_click(excluir_action)
    tabela_aulas.param.watch(selecionar_linha, 'selection')

    carregar_dados()

    # --- Layout Final ---
    form_col1 = pn.Column(id_aula, titulo, select_instrutor, select_categoria, status_aula, capacidade_maxima)
    form_col2 = pn.Column(pn.Row(data_inicio, data_fim), pn.Row(hora_inicio, hora_fim), formato, link_aula, logradouro)
    form_col3 = pn.Column(descricao)
    layout = pn.Column(
        pn.Row(filtro_titulo, btn_consultar, align='end'),
        tabela_aulas, "### Formulário de Aula", pn.Row(form_col1, form_col2, form_col3),
        "### Ações", pn.Row(btn_inserir, btn_atualizar, btn_excluir)
    )
    return layout
