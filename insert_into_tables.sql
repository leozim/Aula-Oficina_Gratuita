-- ========= SCRIPT DE POVOAMENTO DE TABELAS (INSERTS) =========
-- PROJETO: Aplicativo de Intermediação de Aulas e Oficinas Gratuitas
-- =================================================================

-- 1. POVOAMENTO DE USUARIOS
INSERT INTO USUARIO (pnome, snome, email, senha, foto_perfil_url, numero_celular) VALUES
('Leonardo', 'Mariz', 'leo.mariz@email.com', 'senha123', 'http://example.com/leo.jpg', '11987654321'),
('Matheus', 'Alves', 'matheus.alves@email.com', 'senha123', 'http://example.com/matheus.jpg', '21987654322'),
('Cinthia', 'Nunes', 'cinthia.nunes@email.com', 'senha123', 'http://example.com/cinthia.jpg', '31987654323'),
('Vitor', 'Pinheiro', 'vitor.pinheiro@email.com', 'senha123', 'http://example.com/vitor.jpg', '41987654324'),
('Ana', 'Silva', 'ana.silva@email.com', 'senha123', 'http://example.com/ana.jpg', '51987654325'),
('Bruno', 'Costa', 'bruno.costa@email.com', 'senha123', 'http://example.com/bruno.jpg', '61987654326'),
('Carla', 'Dias', 'carla.dias@email.com', 'senha123', 'http://example.com/carla.jpg', '71987654327'),
('Daniel', 'Ferreira', 'daniel.ferreira@email.com', 'senha123', 'http://example.com/daniel.jpg', '81987654328'),
('Eduarda', 'Lima', 'eduarda.lima@email.com', 'senha123', 'http://example.com/duda.jpg', '91987654329'),
('Fábio', 'Melo', 'fabio.melo@email.com', 'senha123', 'http://example.com/fabio.jpg', '11987654330'),
('Gabriela', 'Nogueira', 'gabriela.nogueira@email.com', 'senha123', 'http://example.com/gabi.jpg', '21987654331'),
('Heitor', 'Oliveira', 'heitor.oliveira@email.com', 'senha123', 'http://example.com/heitor.jpg', '31987654332'),
('Isabela', 'Pereira', 'isabela.pereira@email.com', 'senha123', 'http://example.com/isabela.jpg', '41987654333'),
('João', 'Ribeiro', 'joao.ribeiro@email.com', 'senha123', 'http://example.com/joao.jpg', '51987654334');

-- 2. POVOAMENTO DOS TIPOS DE USUÁRIOS
-- Administradores
INSERT INTO ADMINISTRADOR (id_usuario, nivel_permissao_admin) VALUES
(1, 'Super Admin'),
(4, 'Moderador de Conteúdo');

-- Instrutores
INSERT INTO INSTRUTOR (id_usuario, biografia_resumo, link_portfolio) VALUES
(2, 'Especialista em desenvolvimento de software com 10 anos de experiência em Python e Java.', 'http://linkedin.com/in/matheusalves'),
(3, 'Designer Gráfica e Artista Plástica, apaixonada por ensinar técnicas de aquarela e design digital.', 'http://behance.net/cinthianunes'),
(5, 'Chef de cozinha com foco em culinária regional brasileira.', NULL),
(6, 'Músico profissional, professor de violão e teoria musical.', 'http://youtube.com/brunocostamusic'),
(7, 'Professora de Yoga e meditação, certificada internacionalmente.', NULL);

-- Alunos
INSERT INTO ALUNO (id_usuario, nivel_escolaridade) VALUES
(8, 'Ensino Superior Completo'),
(9, 'Ensino Médio Completo'),
(10, 'Cursando Ensino Superior'),
(11, 'Ensino Superior Completo'),
(12, 'Mestrado'),
(13, 'Ensino Médio Completo'),
(14, 'Doutorado');

-- Áreas de Interesse dos Alunos
INSERT INTO ALUNO_areas_interesse (id_usuario, areas_interesse) VALUES
(8, 'Tecnologia'), (8, 'Música'),
(9, 'Artes'), (9, 'Culinária'),
(10, 'Tecnologia'), (10, 'Programação'),
(11, 'Bem-estar'), (11, 'Culinária'),
(12, 'Artes'), (12, 'Música'),
(13, 'Idiomas'), (13, 'Tecnologia'),
(14, 'Ciência de Dados'), (14, 'Programação');

-- 3. POVOAMENTO DE CATEGORIAS
INSERT INTO CATEGORIA (nome_categoria, descricao_categoria) VALUES
('Tecnologia', 'Aulas sobre programação, software, hardware e novas tecnologias.'),
('Artes', 'Oficinas de desenho, pintura, escultura, fotografia e outras formas de expressão artística.'),
('Culinária', 'Aulas práticas de receitas, técnicas de cozinha e gastronomia.'),
('Música', 'Aulas de instrumentos musicais, canto, teoria musical e produção.'),
('Bem-estar', 'Atividades voltadas para a saúde física e mental, como yoga, meditação e fitness.'),
('Idiomas', 'Cursos para aprendizado de línguas estrangeiras.'),
('Negócios', 'Aulas sobre empreendedorismo, finanças pessoais e marketing.'),
('Artesanato', 'Oficinas para aprender a criar peças manuais, como crochê, marcenaria e bijuterias.'),
('Fotografia', 'Cursos sobre técnicas fotográficas, edição de imagem e equipamentos.'),
('Dança', 'Aulas de diversos estilos de dança, para iniciantes e avançados.');

-- 4. POVOAMENTO DE AULAS_OFICINAS
INSERT INTO AULA_OFICINA (id_instrutor, id_categoria, titulo, descricao_detalhada, data_hora_inicio, data_hora_fim, formato, link_aula, logradouro, numero, bairro, cidade, estado, cep, capacidade_maxima, status_aula) VALUES
(2, 1, 'Introdução ao Python', 'Aprenda os conceitos básicos da linguagem Python.', '2025-08-01 19:00:00-03', '2025-08-01 21:00:00-03', 'Online', 'http://meet.google.com/pypy', NULL, NULL, NULL, NULL, NULL, NULL, 50, 'Publicada'),
(3, 2, 'Aquarela para Iniciantes', 'Descubra o mundo da pintura em aquarela.', '2025-08-05 14:00:00-03', '2025-08-05 17:00:00-03', 'Presencial', NULL, 'Rua das Artes', '123', 'Centro', 'Fortaleza', 'CE', '60000-000', 15, 'Publicada'),
(5, 3, 'Culinária Cearense: Baião de Dois', 'Aprenda a fazer um autêntico Baião de Dois.', '2025-07-25 18:00:00-03', '2025-07-25 20:00:00-03', 'Presencial', NULL, 'Av. Beira Mar', '456', 'Meireles', 'Fortaleza', 'CE', '60165-121', 20, 'Em Andamento'),
(6, 4, 'Violão Básico', 'Primeiros acordes e ritmos no violão.', '2025-08-10 10:00:00-03', '2025-08-10 12:00:00-03', 'Online', 'http://zoom.us/violao', NULL, NULL, NULL, NULL, NULL, NULL, 30, 'Publicada'),
(7, 5, 'Meditação Guiada para Aliviar o Estresse', 'Uma sessão para acalmar a mente.', '2025-07-30 07:00:00-03', '2025-07-30 08:00:00-03', 'Online', 'http://meet.google.com/medi', NULL, NULL, NULL, NULL, NULL, NULL, 100, 'Publicada'),
(2, 1, 'Desenvolvimento Web com Flask', 'Crie sua primeira aplicação web com Python e Flask.', '2025-09-01 19:00:00-03', '2025-09-01 21:00:00-03', 'Online', 'http://meet.google.com/flask', NULL, NULL, NULL, NULL, NULL, NULL, 40, 'Publicada'),
(3, 8, 'Oficina de Macramê', 'Aprenda a arte dos nós para criar peças decorativas.', '2025-08-20 15:00:00-03', '2025-08-20 18:00:00-03', 'Presencial', NULL, 'Rua dos Artesãos', '789', 'Aldeota', 'Fortaleza', 'CE', '60150-160', 12, 'Publicada'),
(5, 3, 'Moqueca Baiana', 'Uma viagem de sabores pela culinária da Bahia.', '2025-07-15 19:00:00-03', '2025-07-15 21:00:00-03', 'Presencial', NULL, 'Av. Beira Mar', '456', 'Meireles', 'Fortaleza', 'CE', '60165-121', 20, 'Concluída'),
(6, 4, 'Teoria Musical para Leigos', 'Entenda os fundamentos da música.', '2025-07-10 18:00:00-03', '2025-07-10 19:00:00-03', 'Online', 'http://zoom.us/teoria', NULL, NULL, NULL, NULL, NULL, NULL, 50, 'Concluída'),
(7, 5, 'Yoga para Iniciantes', 'Introdução às posturas e respiração do Yoga.', '2025-07-01 09:00:00-03', '2025-07-01 10:30:00-03', 'Presencial', NULL, 'Parque do Cocó', 's/n', 'Cocó', 'Fortaleza', 'CE', '60175-055', 25, 'Cancelada');

-- 5. POVOAMENTO DE INSCRIÇÕES
INSERT INTO INSCRICAO (id_aluno, id_aula, status_inscricao) VALUES
(8, 1, 'Confirmada'), (10, 1, 'Confirmada'),
(9, 2, 'Confirmada'), (12, 2, 'Lista de Espera'),
(11, 3, 'Confirmada'), (8, 3, 'Confirmada'),
(13, 4, 'Confirmada'), (10, 4, 'Cancelada'),
(9, 5, 'Confirmada'), (11, 5, 'Confirmada'),
(8, 8, 'Confirmada'), (9, 8, 'Confirmada'),
(10, 9, 'Confirmada'), (13, 9, 'Confirmada');

-- 6. POVOAMENTO DE AVALIAÇÕES (para aulas concluídas)
INSERT INTO AVALIACAO (id_aluno, id_aula, nota_avaliacao, comentario_avaliacao) VALUES
(8, 8, 5, 'Aula maravilhosa! A chef Ana é muito didática.'),
(9, 8, 5, 'Adorei a receita, ficou uma delícia!'),
(10, 9, 4, 'O professor explicou bem, mas o conteúdo era denso.'),
(13, 9, 5, 'Excelente! Abriu minha mente para a música.'),
(11, 8, 4, 'Gostei, mas o espaço era um pouco pequeno.'),
(8, 9, 5, 'Muito bom para quem não sabe nada de música.'),
(9, 9, 4, 'Ótima iniciativa!'),
(10, 8, 5, 'Perfeito! Recomendo a todos.'),
(13, 8, 5, 'Aula deliciosa em todos os sentidos.'),
(11, 9, 3, 'Achei um pouco rápido demais.');

-- 7. POVOAMENTO DE CERTIFICADOS (para aulas concluídas)
INSERT INTO CERTIFICADO (id_aluno, id_aula, id_instrutor, nome_aluno, nome_aula_oficina, nome_instrutor, data_conclusao, carga_horaria) VALUES
(8, 8, 5, 'Daniel Ferreira', 'Moqueca Baiana', 'Ana Silva', '2025-07-15', '2 horas'),
(9, 8, 5, 'Eduarda Lima', 'Moqueca Baiana', 'Ana Silva', '2025-07-15', '2 horas'),
(10, 9, 6, 'Fábio Melo', 'Teoria Musical para Leigos', 'Bruno Costa', '2025-07-10', '1 hora'),
(13, 9, 6, 'Isabela Pereira', 'Teoria Musical para Leigos', 'Bruno Costa', '2025-07-10', '1 hora'),
(11, 8, 5, 'Gabriela Nogueira', 'Moqueca Baiana', 'Ana Silva', '2025-07-15', '2 horas');

-- 8. POVOAMENTO DE FREQUENCIA
INSERT INTO FREQUENCIA (id_aluno, id_aula, presente) VALUES
(8, 8, TRUE), (9, 8, TRUE), (11, 8, TRUE),
(10, 9, TRUE), (13, 9, TRUE),
(8, 1, TRUE), (10, 1, TRUE),
(9, 2, FALSE), -- Aluno faltou
(11, 3, TRUE), (8, 3, TRUE);

-- 9. POVOAMENTO DE NOTIFICAÇÕES
INSERT INTO NOTIFICACAO (id_destinatario, id_remetente, mensagem, tipo_notificacao, status_leitura) VALUES
(8, NULL, 'Sua inscrição na aula "Introdução ao Python" foi confirmada.', 'Nova_Inscricao', FALSE),
(12, NULL, 'Você está na lista de espera para a aula "Aquarela para Iniciantes".', 'Lista_Espera', TRUE),
(14, NULL, 'A aula "Yoga para Iniciantes", na qual você estava interessado, foi cancelada.', 'Aula_Cancelada', FALSE),
(8, 2, 'Olá! Não se esqueça de instalar o Python 3.12 antes da nossa aula amanhã.', 'Lembrete_Aula', FALSE),
(3, 1, 'Sua aula "Aquarela para Iniciantes" recebeu uma nova avaliação.', 'Nova_Avaliacao', FALSE),
(1, 4, 'O usuário joao.ribeiro@email.com foi reportado por spam.', 'Moderacao', TRUE),
(9, NULL, 'Uma nova aula de "Culinária" foi publicada! Confira: "Bolo de Chocolate"', 'Nova_Aula_Interesse', FALSE),
(10, NULL, 'Lembrete: A aula "Introdução ao Python" começa em 1 hora.', 'Lembrete_Aula', FALSE),
(13, 6, 'Bem-vindo à aula de Violão Básico!', 'Boas_Vindas', TRUE),
(5, NULL, 'Parabéns! Sua aula "Moqueca Baiana" foi concluída com sucesso.', 'Aula_Concluida', TRUE);

-- 10. POVOAMENTO DE MENSAGENS (Mural da Aula)
INSERT INTO MENSAGEM (id_aula_oficina, id_remetente, conteudo_mensagem) VALUES
(1, 2, 'Bem-vindos à nossa aula de Python! Por favor, usem este espaço para dúvidas.'),
(1, 8, 'Professor, qual a diferença entre lista e tupla?'),
(1, 2, 'Ótima pergunta, Daniel! Veremos isso em detalhes no segundo bloco da aula.'),
(2, 3, 'Pessoal, todo o material para a oficina de aquarela já está disponível no local. Não precisam trazer nada!'),
(2, 9, 'Obrigada pela informação, Cinthia! Ansiosa pela aula!'),
(3, 5, 'Alunos, preparem-se para a melhor moqueca da vida de vocês!'),
(3, 11, 'Mal posso esperar, chef!'),
(4, 6, 'Olá, turma! Deixei um link com um afinador online aqui para vocês.'),
(4, 13, 'Muito útil, professor! Obrigado!'),
(1, 10, 'Qual IDE vamos usar? VSCode?');

-- 11. POVOAMENTO DE MENSAGENS PRIVADAS
INSERT INTO MENSAGEM_PRIVADA (id_remetente, id_destinatario, conteudo_mensagem, status_leitura) VALUES
(8, 10, 'Oi Fábio, você entendeu a parte sobre herança na aula de Python?', FALSE),
(10, 8, 'Oi Daniel! Entendi sim, posso te ajudar se quiser.', TRUE),
(9, 12, 'Oi Heitor, você conseguiu vaga na aula de aquarela? Eu fiquei na lista de espera :(', FALSE),
(12, 9, 'Poxa, Eduarda, que pena! Não consegui também. Vamos torcer pra abrir outra turma.', TRUE),
(1, 2, 'Matheus, parabéns pela aula de Python, foi um sucesso!', TRUE),
(2, 1, 'Obrigado, Leonardo! Fico feliz com o feedback.', TRUE),
(4, 1, 'Leo, notei um comentário inadequado na avaliação da aula 9. Pode verificar?', FALSE),
(1, 4, 'Claro, Vitor. Vou verificar agora mesmo. Obrigado por avisar.', TRUE),
(13, 14, 'João, você que é da área, acha que vale a pena fazer o curso de Flask depois do de Python?', FALSE),
(14, 13, 'Com certeza, Isabela! É um ótimo próximo passo.', FALSE);