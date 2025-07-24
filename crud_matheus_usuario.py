
import panel as pn
import pandas as pd
from sqlalchemy import text
from database import engine, con
from logger_config import log


def create_usuario_view():
    log.info("Inicializando a tela de gerenciamento de Usuários.")
    id_usuario = pn.widgets.TextInput(name='ID do Usuário', disabled=True)
    pnome, snome = pn.widgets.TextInput(name='Primeiro Nome'), pn.widgets.TextInput(name='Sobrenome')
    email = pn.widgets.TextInput(name='E-mail')
    senha = pn.widgets.PasswordInput(name='Senha', placeholder='Digite para inserir/atualizar')
    foto_perfil_url = pn.widgets.TextInput(name='URL da Foto do Perfil')
    numero_celular = pn.widgets.TextInput(name='Celular')
    filtro_email = pn.widgets.TextInput(name='Filtrar por E-mail', placeholder='Digite para buscar...')

    btn_inserir, btn_atualizar, btn_excluir, btn_consultar = [pn.widgets.Button(name=n, button_type=t) for n, t in
                                                              [('Inserir', 'primary'), ('Atualizar', 'warning'),
                                                               ('Excluir', 'danger'), ('Consultar', 'default')]]

    tabela_usuarios = pn.widgets.Tabulator(None, layout='fit_data_table', disabled=True, page_size=10, selectable=True)

    def carregar_dados(event=None):
        log.info("Ação: carregar_dados (Usuários)")
        params = {}
        query = text(
            "SELECT id_usuario, pnome, snome, email, data_cadastro, foto_perfil_url, numero_celular FROM usuario")
        if filtro_email.value:
            query = text(
                "SELECT id_usuario, pnome, snome, email, data_cadastro, foto_perfil_url, numero_celular FROM usuario WHERE email ILIKE :email")
            params['email'] = f"%{filtro_email.value}%"
        try:
            df = pd.read_sql_query(query, engine, params=params)
            tabela_usuarios.value = df
            if event:
                limpar_campos()
        except Exception:
            log.exception("ERRO ao carregar usuários!")
            pn.state.notifications.error('Erro ao carregar usuários. Verifique o console.')

    def limpar_campos(event=None):
        id_usuario.value, pnome.value, snome.value, email.value = '', '', '', ''
        senha.value, foto_perfil_url.value, numero_celular.value = '', '', ''
        tabela_usuarios.selection = []

    def inserir_action(event):
        log.info(f"Ação: inserir_action (Usuário) com email='{email.value}'")
        if not email.value or not pnome.value or not snome.value or not senha.value:
            pn.state.notifications.warning('Nome, sobrenome, e-mail e senha são obrigatórios.')
            return
        try:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO usuario (pnome, snome, email, senha, foto_perfil_url, numero_celular) VALUES (%s, %s, %s, %s, %s, %s)",
                (pnome.value, snome.value, email.value, senha.value, foto_perfil_url.value or None,
                 numero_celular.value or None)
            )
            con.commit()
            cursor.close()
            pn.state.notifications.success('Usuário inserido!')
            carregar_dados()
        except Exception:
            log.exception("ERRO ao inserir usuário!")
            con.rollback()
            pn.state.notifications.error('Erro ao inserir. Verifique o console.')

    def atualizar_action(event):
        log.info(f"Ação: atualizar_action (Usuário) para ID={id_usuario.value}")
        if not id_usuario.value:
            pn.state.notifications.warning('Selecione um usuário para atualizar.')
            return

        query_update = "UPDATE usuario SET pnome=%s, snome=%s, email=%s, foto_perfil_url=%s, numero_celular=%s {senha_update} WHERE id_usuario=%s"
        params = [pnome.value, snome.value, email.value, foto_perfil_url.value or None, numero_celular.value or None]

        if senha.value:
            query_update = query_update.format(senha_update=", senha=%s")
            params.append(senha.value)
        else:
            query_update = query_update.format(senha_update="")
        params.append(int(id_usuario.value))
        try:
            cursor = con.cursor()
            cursor.execute(query_update, tuple(params))
            con.commit()
            cursor.close()
            pn.state.notifications.success('Usuário atualizado!')
            carregar_dados()
        except Exception:
            log.exception(f"ERRO ao atualizar usuário ID={id_usuario.value}!")
            con.rollback()
            pn.state.notifications.error('Erro ao atualizar. Verifique o console.')

    def excluir_action(event):
        log.info(f"Ação: excluir_action (Usuário) para ID={id_usuario.value}")
        if not id_usuario.value:
            pn.state.notifications.warning('Selecione um usuário para excluir.')
            return
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM usuario WHERE id_usuario=%s", (int(id_usuario.value),))
            con.commit()
            cursor.close()
            pn.state.notifications.success('Usuário excluído!')
            carregar_dados()
        except Exception:
            log.exception(f"ERRO ao excluir usuário ID={id_usuario.value}!")
            con.rollback()
            pn.state.notifications.error('Erro ao excluir. Verifique o console.')

    def selecionar_linha(event):
        if not event.new:
            limpar_campos()
            return

        indice_selecionado = event.new[0]
        linha_data = tabela_usuarios.value.iloc[indice_selecionado]

        log.info(f"Linha selecionada (Usuário): {linha_data.to_dict()}")
        id_usuario.value = str(linha_data['id_usuario'])
        pnome.value, snome.value, email.value = linha_data['pnome'], linha_data['snome'], linha_data['email']
        foto_perfil_url.value = linha_data['foto_perfil_url'] if pd.notna(linha_data['foto_perfil_url']) else ''
        numero_celular.value = linha_data['numero_celular'] if pd.notna(linha_data['numero_celular']) else ''
        senha.value = ''

    btn_consultar.on_click(carregar_dados)
    btn_inserir.on_click(inserir_action)
    btn_atualizar.on_click(atualizar_action)
    btn_excluir.on_click(excluir_action)

    tabela_usuarios.param.watch(selecionar_linha, 'selection')

    carregar_dados()

    form_layout = pn.Column("### Formulário de Usuário", id_usuario, pn.Row(pnome, snome), email, senha,
                            foto_perfil_url, numero_celular)
    actions_layout = pn.Column("### Ações", pn.Row(btn_inserir, btn_atualizar, btn_excluir))
    layout = pn.Column(
        pn.Row(filtro_email, btn_consultar, align='end'),
        tabela_usuarios,
        pn.Row(form_layout, actions_layout)
    )
    return layout