from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conn = sqlite3.connect('bauru_participa.db')
    return conn

def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Enquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OpcoesEnquete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_enquete INTEGER,
            opcao TEXT NOT NULL,
            FOREIGN KEY(id_enquete) REFERENCES Enquetes(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_enquete INTEGER,
            id_opcao INTEGER,
            FOREIGN KEY(id_enquete) REFERENCES Enquetes(id),
            FOREIGN KEY(id_opcao) REFERENCES OpcoesEnquete(id)
        )
    ''')
    conn.commit()
    conn.close()

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


@app.route('/')
def index():
    return 'Bem-vindo à plataforma Bauru Participa!'

if __name__ == '__main__':
    criar_tabelas()  
    app.run(debug=True)


@app.route('/api/enquetes', methods=['POST'])
def criar_enquete():
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    try:
        adicionar_enquete(titulo, descricao)
        return jsonify({"message": "Enquete criada com sucesso."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/enquetes', methods=['GET'])
def listar_enquetes_api():
    try:
        enquetes = listar_enquetes()
        return jsonify({"enquetes": enquetes}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/enquetes/<int:id_enquete>', methods=['GET'])
def obter_detalhes_enquete_api(id_enquete):
    try:
        enquete = obter_detalhes_enquete(id_enquete)
        if enquete:
            return jsonify({"enquete": enquete}), 200
        else:
            return jsonify({"message": "Enquete não encontrada."}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/enquetes/<int:id_enquete>/votar', methods=['POST'])
def votar_opcao_enquete_api(id_enquete):
    data = request.get_json()
    id_opcao = data.get('id_opcao')
    try:
        votar_opcao_enquete(id_enquete, id_opcao)
        return jsonify({"message": "Voto registrado com sucesso."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/enquetes/<int:id_enquete>/opcoes', methods=['POST'])
def adicionar_opcao_enquete_api(id_enquete):
    data = request.get_json()
    opcao = data.get('opcao')
    try:
        adicionar_opcao_enquete(id_enquete, opcao)
        return jsonify({"message": "Opção de enquete adicionada com sucesso."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/enquetes/<int:id_enquete>/opcoes/<int:id_opcao>', methods=['DELETE'])
def deletar_opcao_enquete_api(id_enquete, id_opcao):
    try:
        deletar_opcao_enquete(id_opcao)
        return jsonify({"message": "Opção de enquete deletada com sucesso."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    criar_tabelas()
    app.run(debug=True)
