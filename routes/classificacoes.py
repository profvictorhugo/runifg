from flask import Blueprint,  jsonify
from db import mysql
import MySQLdb.cursors


classificacoes_bp = Blueprint('classificacoes', __name__)


@classificacoes_bp.route('/classificacao/geral/<int:corrida_id>', methods=['GET'])
def get_classificacao_geral(corrida_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("""
            SELECT i.atleta_id, a.nome, a.sexo, c.prova_id, p.nome AS prova_nome, i.numero, TIME_FORMAT(i.hora_chegada, '%%H:%%i:%%s') as hora_chegada,
                   ROW_NUMBER() OVER (PARTITION BY c.prova_id, a.sexo ORDER BY i.hora_chegada) AS classificacao
            FROM Inscricao AS i
            JOIN Atleta AS a ON i.atleta_id = a.id
            JOIN Categoria AS c ON i.categoria_id = c.id
            JOIN Provas AS p ON c.prova_id = p.id
            WHERE c.corrida_id = %s AND i.status = 'ENCERRADA'
            ORDER BY c.prova_id, a.sexo, i.hora_chegada;
        """, (corrida_id,))

        dados = cursor.fetchall()
        cursor.close()

        if not dados:
            return jsonify({"message": "Nenhuma inscrição encerrada encontrada para esta corrida. Corrida não finalizada"}), 404

        # 🔹 Organizando os dados no formato correto
        provas = {}
        for row in dados:
            prova_id = row['prova_id']
            sexo = row['sexo']

            if prova_id not in provas:
                provas[prova_id] = {
                    "prova_id": prova_id,
                    "prova_nome": row['prova_nome'],
                    "classificacao_masculino": [],
                    "classificacao_feminino": []
                }

            atleta_info = {
                "atleta_id": row['atleta_id'],
                "nome": row['nome'],
                "numero": row['numero'],
                "hora_chegada": row['hora_chegada'],
                "classificacao": row['classificacao']
            }

            if sexo == 'M':
                provas[prova_id]["classificacao_masculino"].append(atleta_info)
            else:
                provas[prova_id]["classificacao_feminino"].append(atleta_info)

        return jsonify({"provas": list(provas.values())}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar classificação geral por sexo: {str(e)}"}), 500


@classificacoes_bp.route('/classificacao/por_categoria/<int:corrida_id>', methods=['GET'])
def get_classificacao_por_categoria(corrida_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("""
            SELECT i.atleta_id, a.nome, a.sexo, i.numero, 
                   c.id AS categoria_id, c.nome AS categoria_nome, TIME_FORMAT(i.hora_chegada, '%%H:%%i:%%s') as hora_chegada,
                   ROW_NUMBER() OVER (PARTITION BY c.id, a.sexo ORDER BY i.hora_chegada) AS classificacao
            FROM Inscricao AS i
            JOIN Atleta AS a ON i.atleta_id = a.id
            JOIN Categoria AS c ON i.categoria_id = c.id
            WHERE c.corrida_id = %s AND i.status = 'ENCERRADA'
            ORDER BY c.id, a.sexo, i.hora_chegada;
        """, (corrida_id,))

        dados = cursor.fetchall()
        cursor.close()

        if not dados:
            return jsonify({"message": "Nenhuma inscrição encerrada encontrada para esta corrida. Corrida não finalizada"}), 404

        # 🔹 Organizando os dados no formato correto
        categorias = {}
        for row in dados:
            categoria_id = row['categoria_id']
            sexo = row['sexo']

            if categoria_id not in categorias:
                categorias[categoria_id] = {
                    "categoria_id": categoria_id,
                    "categoria_nome": row['categoria_nome'],
                    "classificacao_masculino": [],
                    "classificacao_feminino": []
                }

            atleta_info = {
                "atleta_id": row['atleta_id'],
                "nome": row['nome'],
                "numero": row['numero'],
                "hora_chegada": row['hora_chegada'],
                "classificacao": row['classificacao']
            }

            if sexo == 'M':
                categorias[categoria_id]["classificacao_masculino"].append(atleta_info)
            else:
                categorias[categoria_id]["classificacao_feminino"].append(atleta_info)

        return jsonify({"categorias": list(categorias.values())}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar classificação por categoria: {str(e)}"}), 500
