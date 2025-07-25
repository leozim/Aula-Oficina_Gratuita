-- =================================================================================
/*
CREATE DATABASE "AULA_OFICINA_GRATUITA"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
*/
-- =================================================================================

-- =================================================================================
-- ========= SCRIPT DE CRIAÇÃO DE TABELAS PARA O BANCO DE DADOS POSTGRES =========
-- PROJETO: Aplicativo de Intermediação de Aulas e Oficinas Gratuitas
-- =================================================================================

-- SCRIPT DE LIMPEZA
DROP TABLE IF EXISTS MENSAGEM_PRIVADA, MENSAGEM, NOTIFICACAO, FREQUENCIA, CERTIFICADO, AVALIACAO, INSCRICAO, AULA_OFICINA_material_apoio, AULA_OFICINA_publico_alvo, AULA_OFICINA, CATEGORIA, ALUNO_areas_interesse, ADMINISTRADOR, INSTRUTOR, ALUNO, USUARIO CASCADE;
DROP TYPE IF EXISTS status_aula_enum, status_inscricao_enum;
COMMIT;

-- Definição de tipos ENUM para padronizar valores de status
CREATE TYPE status_aula_enum AS ENUM ('Rascunho', 'Publicada', 'Em Andamento', 'Concluída', 'Cancelada');
CREATE TYPE status_inscricao_enum AS ENUM ('Confirmada', 'Lista de Espera', 'Cancelada');

-- ========= 1. TABELAS DE USUÁRIOS (ESTRUTURA DE HERANÇA) =========

-- Tabela central que armazena dados comuns a todos os usuários (Superclasse)
CREATE TABLE USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    pnome VARCHAR(50) NOT NULL,
    snome VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_cadastro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    foto_perfil_url VARCHAR(255),
    numero_celular VARCHAR(20),
    numero_telefone VARCHAR(20)
);

-- Especialização para Alunos
CREATE TABLE ALUNO (
    id_usuario INTEGER PRIMARY KEY,
    nivel_escolaridade VARCHAR(100),
    CONSTRAINT fk_aluno_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

-- Tabela para o atributo multivalorado "áreas de interesse" do aluno
CREATE TABLE ALUNO_areas_interesse (
    id_usuario INTEGER NOT NULL,
    areas_interesse VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_usuario, areas_interesse),
    CONSTRAINT fk_areas_interesse_aluno FOREIGN KEY (id_usuario) REFERENCES ALUNO(id_usuario) ON DELETE CASCADE
);

-- Especialização para Instrutores
CREATE TABLE INSTRUTOR (
    id_usuario INTEGER PRIMARY KEY,
    biografia_resumo TEXT,
    link_portfolio VARCHAR(255),
    CONSTRAINT fk_instrutor_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

-- Especialização para Administradores
CREATE TABLE ADMINISTRADOR (
    id_usuario INTEGER PRIMARY KEY,
    nivel_permissao_admin VARCHAR(50) NOT NULL,
    CONSTRAINT fk_admin_usuario FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

-- ========= 2. TABELAS DE CONTEÚDO (AULAS E CATEGORIAS) =========

-- Armazena as categorias para classificar as aulas
CREATE TABLE CATEGORIA (
    id_categoria SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(100) UNIQUE NOT NULL,
    descricao_categoria TEXT
);

-- ... (outras tabelas)

-- Tabela central com informações das aulas e oficinas (ESTRUTURA ATUALIZADA)
CREATE TABLE AULA_OFICINA (
    id_aula SERIAL PRIMARY KEY,
    id_instrutor INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao_detalhada TEXT,
    pre_requisitos TEXT,
    -- COLUNAS ANTIGAS REMOVIDAS
    -- COLUNAS NOVAS ADICIONADAS
    data_inicio DATE,
    data_fim DATE,
    hora_inicio TIME,
    hora_fim TIME,
    formato VARCHAR(20) NOT NULL CHECK (formato IN ('Online', 'Presencial')),
    link_aula VARCHAR(255),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(10),
    capacidade_maxima INTEGER,
    status_aula status_aula_enum NOT NULL,
    CONSTRAINT fk_aula_instrutor FOREIGN KEY (id_instrutor) REFERENCES INSTRUTOR(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_aula_categoria FOREIGN KEY (id_categoria) REFERENCES CATEGORIA(id_categoria) ON DELETE RESTRICT,
    CONSTRAINT chk_capacidade CHECK (capacidade_maxima > 0),
    CONSTRAINT chk_local_formato CHECK (
        (formato = 'Online' AND link_aula IS NOT NULL AND logradouro IS NULL) OR
        (formato = 'Presencial' AND logradouro IS NOT NULL AND link_aula IS NULL)
    )
);

-- Tabela para o atributo multivalorado "publico_alvo" da aula
CREATE TABLE AULA_OFICINA_publico_alvo (
    id_aula INTEGER NOT NULL,
    publico_alvo VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_aula, publico_alvo),
    CONSTRAINT fk_publico_alvo_aula FOREIGN KEY (id_aula) REFERENCES AULA_OFICINA(id_aula) ON DELETE CASCADE
);

-- Tabela para o atributo multivalorado "material_apoio" da aula
CREATE TABLE AULA_OFICINA_material_apoio (
    id_aula INTEGER NOT NULL,
    material_apoio TEXT NOT NULL,
    PRIMARY KEY (id_aula, material_apoio),
    CONSTRAINT fk_material_apoio_aula FOREIGN KEY (id_aula) REFERENCES AULA_OFICINA(id_aula) ON DELETE CASCADE
);


-- ========= 3. TABELAS TRANSACIONAIS E DE RELACIONAMENTO =========

-- Entidade associativa para a inscrição de um Aluno em uma Aula
CREATE TABLE INSCRICAO (
    id_aluno INTEGER NOT NULL,
    id_aula INTEGER NOT NULL,
    data_inscricao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status_inscricao status_inscricao_enum NOT NULL,
    PRIMARY KEY (id_aluno, id_aula),
    CONSTRAINT fk_inscricao_aluno FOREIGN KEY (id_aluno) REFERENCES ALUNO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_inscricao_aula FOREIGN KEY (id_aula) REFERENCES AULA_OFICINA(id_aula) ON DELETE CASCADE
);

-- Armazena as avaliações feitas pelos alunos sobre as aulas
CREATE TABLE AVALIACAO (
    id_aluno INTEGER NOT NULL,
    id_aula INTEGER NOT NULL,
    nota_avaliacao INTEGER NOT NULL,
    comentario_avaliacao TEXT,
    data_avaliacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_aluno, id_aula),
    CONSTRAINT fk_avaliacao_aluno FOREIGN KEY (id_aluno) REFERENCES ALUNO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_avaliacao_aula FOREIGN KEY (id_aula) REFERENCES AULA_OFICINA(id_aula) ON DELETE CASCADE,
    CONSTRAINT chk_nota CHECK (nota_avaliacao BETWEEN 1 AND 5)
);

-- Armazena os dados dos certificados gerados
CREATE TABLE CERTIFICADO (
    id_aluno INTEGER NOT NULL,
    id_aula INTEGER NOT NULL,
    id_instrutor INTEGER NOT NULL,
    nome_aluno VARCHAR(151) NOT NULL,
    nome_aula_oficina VARCHAR(255) NOT NULL,
    nome_instrutor VARCHAR(151) NOT NULL,
    data_conclusao DATE NOT NULL,
    carga_horaria VARCHAR(50),
    PRIMARY KEY (id_aluno, id_aula),
    CONSTRAINT fk_certificado_aluno FOREIGN KEY (id_aluno) REFERENCES ALUNO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_certificado_aula FOREIGN KEY (id_aula) REFERENCES AULA_OFICINA(id_aula) ON DELETE CASCADE,
    CONSTRAINT fk_certificado_instrutor FOREIGN KEY (id_instrutor) REFERENCES INSTRUTOR(id_usuario) ON DELETE SET NULL
);

-- Registra a presença dos alunos nas aulas
CREATE TABLE FREQUENCIA (
    id_aluno INTEGER NOT NULL,
    id_aula INTEGER NOT NULL,
    presente BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id_aluno, id_aula),
    CONSTRAINT fk_frequencia_aluno FOREIGN KEY (id_aluno) REFERENCES ALUNO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_frequencia_aula FOREIGN KEY (id_aula) REFERENCES AULA_OFICINA(id_aula) ON DELETE CASCADE
);


-- ========= 4. TABELAS DE COMUNICAÇÃO =========

-- Armazena as notificações enviadas aos usuários
CREATE TABLE NOTIFICACAO (
    id_notificacao SERIAL PRIMARY KEY,
    id_destinatario INTEGER NOT NULL,
    id_remetente INTEGER, -- Pode ser nulo para notificações do sistema
    mensagem TEXT NOT NULL,
    tipo_notificacao VARCHAR(50),
    data_envio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status_leitura BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_notificacao_destinatario FOREIGN KEY (id_destinatario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_notificacao_remetente FOREIGN KEY (id_remetente) REFERENCES USUARIO(id_usuario) ON DELETE SET NULL
);

-- Armazena mensagens trocadas no contexto de uma aula (mural)
CREATE TABLE MENSAGEM (
    id_mensagem SERIAL PRIMARY KEY,
    id_aula_oficina INTEGER NOT NULL,
    id_remetente INTEGER NOT NULL,
    conteudo_mensagem TEXT NOT NULL,
    data_hora_envio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mensagem_aula FOREIGN KEY (id_aula_oficina) REFERENCES AULA_OFICINA(id_aula) ON DELETE CASCADE,
    CONSTRAINT fk_mensagem_remetente FOREIGN KEY (id_remetente) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

-- Armazena mensagens privadas trocadas entre dois usuários
CREATE TABLE MENSAGEM_PRIVADA (
    id_mensagem SERIAL PRIMARY KEY,
    id_remetente INTEGER NOT NULL,
    id_destinatario INTEGER NOT NULL,
    conteudo_mensagem TEXT NOT NULL,
    data_hora_envio TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status_leitura BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_msg_privada_remetente FOREIGN KEY (id_remetente) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_msg_privada_destinatario FOREIGN KEY (id_destinatario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

/*
ALTER TABLE AULA_OFICINA
ADD COLUMN data_inicio DATE,
ADD COLUMN data_fim DATE,
ADD COLUMN hora_inicio TIME,
ADD COLUMN hora_fim TIME;

COMMIT;

 */

