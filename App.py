import sqlite3

def conectar_banco():
    conn = sqlite3.connect('bauru_participa.db')
    return conn

def adicionar_enquete(titulo, descricao):
    if not titulo or not descricao:
        raise ValueError("Título e descrição são obrigatórios.")
    if len(titulo) > 255:
        raise ValueError("Título não pode ter mais de 255 caracteres.")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Enquetes (titulo, descricao) VALUES (?, ?)', (titulo, descricao))
    conn.commit()
    conn.close()

def listar_enquetes():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Enquetes')
    enquetes = cursor.fetchall()
    conn.close()
    return enquetes

def obter_detalhes_enquete(id_enquete):
    if not id_enquete:
        raise ValueError("ID da enquete é obrigatório.")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Enquetes WHERE id = ?', (id_enquete,))
    enquete = cursor.fetchone()
    conn.close()
    return enquete

def votar_opcao_enquete(id_enquete, id_opcao):
    if not id_enquete or not id_opcao:
        raise ValueError("ID da enquete e ID da opção são obrigatórios.")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Votos (id_enquete, id_opcao) VALUES (?, ?)', (id_enquete, id_opcao))
    conn.commit()
    conn.close()

def adicionar_opcao_enquete(id_enquete, opcao):
    if not id_enquete or not opcao:
        raise ValueError("ID da enquete e opção são obrigatórios.")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO OpcoesEnquete (id_enquete, opcao) VALUES (?, ?)', (id_enquete, opcao))
    conn.commit()
    conn.close()

def deletar_enquete(id_enquete):
    if not id_enquete:
        raise ValueError("ID da enquete é obrigatório.")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Enquetes WHERE id = ?', (id_enquete,))
    conn.commit()
    conn.close()

def deletar_opcao_enquete(id_opcao):
    if not id_opcao:
        raise ValueError("ID da opção é obrigatório.")

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM OpcoesEnquete WHERE id = ?', (id_opcao,))
    conn.commit()
    conn.close()

try:
    adicionar_enquete('Enquete 1', 'Esta é a descrição da Enquete 1')
    print("Enquete adicionada com sucesso.")
except ValueError as e:
    print("Erro ao adicionar enquete:", str(e))

try:
    enquetes = listar_enquetes()
    print("Enquetes:", enquetes)
except ValueError as e:
    print("Erro ao listar enquetes:", str(e))

try:
    enquete = obter_detalhes_enquete(1)
    print("Detalhes da enquete:", enquete)
except ValueError as e:
    print("Erro ao obter detalhes da enquete:", str(e))

try:
    votar_opcao_enquete(1, 1)
    print("Voto registrado com sucesso.")
except ValueError as e:
    print("Erro ao votar em uma opção de enquete:", str(e))

try:
    adicionar_opcao_enquete(1, 'Opção A')
    print("Opção de enquete adicionada com sucesso.")
except ValueError as e:
    print("Erro ao adicionar opção de enquete:", str(e))

try:
    deletar_enquete(1)
    print("Enquete deletada com sucesso.")
except ValueError as e:
    print("Erro ao deletar enquete:", str(e))

try:
    deletar_opcao_enquete(1)
    print("Opção de enquete deletada com sucesso.")
except ValueError as e:
    print("Erro ao deletar opção de enquete:", str(e))




