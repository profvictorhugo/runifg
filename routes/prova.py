from flask import Blueprint, request, jsonify
from db import mysql
import MySQLdb.cursors


prova_bp = Blueprint('prova', __name__)

@prova_bp.route('/prova/getAll', methods=['GET'])
def getAll():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Provas")
        provas = cursor.fetchall()
        cursor.close()
        return jsonify(provas), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar provas: {str(e)}"}), 500

@prova_bp.route('/prova/getById/<int:id>', methods=['GET'])
def getById(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Provas WHERE id=%s", (id,))
        prova = cursor.fetchone()  # Usa fetchone() pois ID é único
        cursor.close()

        if prova:
            return jsonify(prova), 200
        else:
            return jsonify({"error": "Prova não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar prova: {str(e)}"}), 500

@prova_bp.route('/prova/createProva', methods=['POST'])
def createProva():
    data = request.get_json()

    # Validação dos campos obrigatórios
    if not all(k in data for k in ('nome', 'distancia_km')):
        return jsonify({"error": "Os campos nome e distancia_km são obrigatórios"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Provas (nome, distancia_km) VALUES (%s, %s)",
                       (data['nome'], data['distancia_km']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Prova criada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao cadastrar prova: {str(e)}"}), 500

@prova_bp.route('/prova/updateProva/<int:id>', methods=['PUT'])
def updateProva(id):
    data = request.get_json()

    if not all(k in data for k in ('nome', 'distancia_km')):
        return jsonify({"error": "Os campos nome e distancia_km são obrigatórios"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Atualiza diretamente e verifica se algo foi alterado
        cursor.execute("UPDATE Provas SET nome = %s, distancia_km = %s WHERE id = %s",
                       (data['nome'], data['distancia_km'], id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Prova não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Prova atualizada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar prova: {str(e)}"}), 500

@prova_bp.route('/prova/deleteProva/<int:id>', methods=['DELETE'])
def deleteProva(id):
    try:
        cursor = mysql.connection.cursor()

        # Deleta diretamente e verifica se algo foi removido
        cursor.execute("DELETE FROM Provas WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Prova não encontrada"}), 404

        cursor.close()
        return jsonify({"message": "Prova removida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao deletar prova: {str(e)}"}), 500
