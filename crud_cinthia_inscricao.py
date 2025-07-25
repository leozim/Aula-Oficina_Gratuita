# crud_cinthia_inscricao.py
import panel as pn
import pandas as pd
from sqlalchemy import text
from database import engine, con
from logger_config import log
import datetime


def create_inscricao_view():
    log.info("Inicializando a tela de gerenciamento de Inscrições.")

    # --- Funções para popular Selects ---
    def get_alunos_options():
        try:
            query = "SELECT a.id_usuario, u.pnome || ' ' || u.snome AS nome_completo FROM aluno a JOIN usuario u ON a.id_usuario = u.id_usuario ORDER BY nome_completo"
            df = pd.read_sql_query(query, engine)
            options = list(zip(df['nome_completo'], df['id_usuario']))
            options.insert(0, ('Todos', None))
            return options
        except:
            log.exception("ERRO ao carregar opções de alunos!")
            return [('Todos', None)]

    def get_aulas_options():
        try:
            query = "SELECT id_aula, titulo FROM aula_oficina WHERE status_aula IN ('Publicada', 'Em Andamento') ORDER BY titulo"
            df = pd.read_sql_query(query, engine)
            return list(zip(df['titulo'], df['id_aula']))
        except:
            log.exception("ERRO ao carregar opções de aulas!")
            return []

    # --- Widgets e Botões ---
    select_aluno = pn.widgets.Select(name='Aluno', options=get_alunos_options())
    select_aula = pn.widgets.Select(name='Aula', options=get_aulas_options())
    status_inscricao = pn.widgets.Select(name='Status', options=['Confirmada', 'Lista de Espera', 'Cancelada'])
    id_aluno_pk, id_aula_pk = pn.widgets.TextInput(name='ID Aluno (Chave)', disabled=True), pn.widgets.TextInput(
        name='ID Aula (Chave)', disabled=True)
    filtro_aluno = pn.widgets.Select(name='Filtrar por Aluno', options=get_alunos_options())

    btn_inserir, btn_atualizar, btn_excluir, btn_consultar = [pn.widgets.Button(name=n, button_type=t) for n, t in
                                                              [('Inscrever', 'primary'),
                                                               ('Atualizar Inscrição', 'warning'),
                                                               ('Cancelar Inscrição', 'danger'),
                                                               ('Consultar', 'default')]]

    tabela_inscricoes = pn.widgets.Tabulator(None, layout='fit_data_table', disabled=True, page_size=10,
                                             selectable=True)

    # --- Funções de Ação ---
    def carregar_dados(event=None):
        params = {}
        base_query = "SELECT i.id_aluno, u.pnome || ' ' || u.snome AS aluno, i.id_aula, a.titulo AS aula, i.data_inscricao, i.status_inscricao FROM inscricao i JOIN aluno al ON i.id_aluno = al.id_usuario JOIN usuario u ON al.id_usuario = u.id_usuario JOIN aula_oficina a ON i.id_aula = a.id_aula"

        selected_filter = filtro_aluno.value
        if selected_filter and selected_filter[1] is not None:
            aluno_id = selected_filter[1]
            query = text(f"{base_query} WHERE i.id_aluno = :aluno_id")
            params['aluno_id'] = aluno_id
        else:
            query = text(base_query)

        try:
            df = pd.read_sql_query(query, engine, params=params)
            tabela_inscricoes.value = df
            if event:
                limpar_campos()
        except Exception:
            log.exception("ERRO ao carregar inscrições!")
            pn.state.notifications.error('Erro ao carregar inscrições. Verifique o console.')

    def limpar_campos(event=None):
        id_aluno_pk.value, id_aula_pk.value = '', ''
        tabela_inscricoes.selection = []

    def inserir_action(event):
        aluno_id = int(select_aluno.value[1]) if select_aluno.value else None
        aula_id = int(select_aula.value[1]) if select_aula.value else None
        log.info(f"Ação: inserir_action (Inscrição) para aluno_id={aluno_id}, aula_id={aula_id}")

        if not aluno_id or not aula_id:
            pn.state.notifications.warning('Aluno e Aula são obrigatórios.')
            return

        ### VALIDAÇÃO DE CHOQUE DE HORÁRIOS (LÓGICA ATUALIZADA) ###
        try:
            cursor = con.cursor()
            # 1. Pega o horário da nova aula que o aluno quer se inscrever.
            cursor.execute("SELECT data_inicio, data_fim, hora_inicio, hora_fim FROM aula_oficina WHERE id_aula = %s",
                           (aula_id,))
            nova_aula_horario = cursor.fetchone()
            if not nova_aula_horario or not all(nova_aula_horario):
                log.warning(
                    f"A aula ID={aula_id} não tem horário completo definido. Inscrição permitida sem verificação.")
            else:
                nova_data_inicio, nova_data_fim, nova_hora_inicio, nova_hora_fim = nova_aula_horario

                # 2. Verifica se existe alguma outra aula CONFIRMADA para este aluno que conflite com o novo horário.
                query_conflito = """
                    SELECT a.titulo
                    FROM inscricao i
                    JOIN aula_oficina a ON i.id_aula = a.id_aula
                    WHERE i.id_aluno = %s
                      AND i.status_inscricao = 'Confirmada'
                      AND a.data_inicio <= %s
                      AND a.data_fim >= %s
                      AND a.hora_inicio < %s
                      AND a.hora_fim > %s
                """
                cursor.execute(query_conflito,
                               (aluno_id, nova_data_fim, nova_data_inicio, nova_hora_fim, nova_hora_inicio))
                aula_conflitante = cursor.fetchone()

                # 3. Se encontrou alguma aula conflitante, avisa o usuário e interrompe.
                if aula_conflitante:
                    pn.state.notifications.error(
                        f'Choque de horário! O aluno já está inscrito na aula "{aula_conflitante[0]}" neste período.')
                    cursor.close()
                    return

            cursor.close()
        except Exception:
            log.exception("ERRO ao verificar choque de horários!")
            pn.state.notifications.error('Erro ao verificar horários. Verifique o console.')
            return

        # Se passou por todas as validações, prossegue com a inserção.
        try:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO inscricao (id_aluno, id_aula, data_inscricao, status_inscricao) VALUES (%s, %s, %s, %s)",
                (aluno_id, aula_id, datetime.datetime.now(), status_inscricao.value)
                )
            con.commit()
            cursor.close()
            pn.state.notifications.success('Inscrição realizada!')
            carregar_dados()
        except Exception:
            log.exception("ERRO ao inscrever aluno!")
            con.rollback()
            pn.state.notifications.error('Erro ao inscrever. Verifique o console.')

    def atualizar_action(event):
        if not id_aluno_pk.value or not id_aula_pk.value:
            pn.state.notifications.warning('Selecione uma inscrição para atualizar.')
            return
        try:
            cursor = con.cursor()
            cursor.execute("UPDATE inscricao SET status_inscricao=%s WHERE id_aluno=%s AND id_aula=%s",
                           (status_inscricao.value, int(id_aluno_pk.value), int(id_aula_pk.value))
                           )
            con.commit()
            cursor.close()
            pn.state.notifications.success('Inscrição atualizada!')
            carregar_dados()
        except Exception:
            log.exception("ERRO ao atualizar inscrição!")
            con.rollback()
            pn.state.notifications.error('Erro ao atualizar. Verifique o console.')

    def excluir_action(event):
        if not id_aluno_pk.value or not id_aula_pk.value:
            pn.state.notifications.warning('Selecione uma inscrição para cancelar.')
            return
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM inscricao WHERE id_aluno=%s AND id_aula=%s",
                           (int(id_aluno_pk.value), int(id_aula_pk.value))
                           )
            con.commit()
            cursor.close()
            pn.state.notifications.success('Inscrição cancelada!')
            carregar_dados()
        except Exception:
            log.exception("ERRO ao cancelar inscrição!")
            con.rollback()
            pn.state.notifications.error('Erro ao cancelar. Verifique o console.')

    def selecionar_linha(event):
        if not event.new:
            limpar_campos()
            return

        indice_selecionado = event.new[0]
        linha_data = tabela_inscricoes.value.iloc[indice_selecionado]

        id_aluno_pk.value, id_aula_pk.value = str(linha_data['id_aluno']), str(linha_data['id_aula'])
        status_inscricao.value = linha_data['status_inscricao']

        select_aluno.value = next((item for item in select_aluno.options if item[1] == linha_data['id_aluno']), None)
        select_aula.value = next((item for item in select_aula.options if item[1] == linha_data['id_aula']), None)

    btn_consultar.on_click(carregar_dados)
    btn_inserir.on_click(inserir_action)
    btn_atualizar.on_click(atualizar_action)
    btn_excluir.on_click(excluir_action)
    tabela_inscricoes.param.watch(selecionar_linha, 'selection')

    carregar_dados()

    form_layout = pn.Column("### Nova Inscrição / Edição", select_aluno, select_aula, status_inscricao,
                            pn.Row(id_aluno_pk, id_aula_pk))
    actions_layout = pn.Column("### Ações", pn.Row(btn_inserir, btn_atualizar, btn_excluir))
    layout = pn.Column(
        pn.Row(filtro_aluno, btn_consultar, align='end'),
        tabela_inscricoes,
        pn.Row(form_layout, actions_layout)
    )
    return layout
