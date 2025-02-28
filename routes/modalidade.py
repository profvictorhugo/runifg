from flask import Blueprint, request, jsonify
from db import mysql
import pymysql.cursors

modalidade_bp = Blueprint('modalidade', __name__)

@modalidade_bp.route('/modalidade/getAll', methods=['GET'])
def getAll():

    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Modalidade")
        modalidades = cursor.fetchall()
        cursor.close()
        return jsonify(modalidades), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar modalidades: {str(e)}"}), 500

@modalidade_bp.route('/modalidade/getById/<int:id>', methods=['GET'])
def getById(id):

    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Modalidade WHERE id=%s", (id,))
        modalidades = cursor.fetchall()
        cursor.close()

        if modalidades:
            return jsonify(modalidades), 200
        else:
            return jsonify({"error": "Modalidade não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar modalidades: {str(e)}"}), 500

@modalidade_bp.route('/modalidades/createModalidade', methods=['POST'])
def createModalidade():
    data = request.get_json()

    # Validação básica dos campos obrigatórios
    if 'nome' not in data:
        return jsonify({"error": "O campo nome é obrigatório"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Modalidade (nome) VALUES (%s)",
                       (data['nome'],))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Modalidade criada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao cadastrar modalidade: {str(e)}"}), 500

@modalidade_bp.route('/modalidade/updateModalidade/<int:id>', methods=['PUT'])
def updateModalidade(id):
    data = request.get_json()

    if 'nome' not in data:
        return jsonify({"error": "O campo nome é obrigatório"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Atualiza diretamente e verifica se algo foi alterado
        cursor.execute("UPDATE Modalidade SET nome = %s WHERE id = %s",
                       (data['nome'], id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Modalidade não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Modalidade atualizada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar modalidade: {str(e)}"}), 500

@modalidade_bp.route('/modalidade/deleteModalidade/<int:id>', methods=['DELETE'])
def deleteModalidade(id):
    try:
        cursor = mysql.connection.cursor()

        # Deleta diretamente e verifica se algo foi removido
        cursor.execute("DELETE FROM Modalidade WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Modalidade não encontrada"}), 404

        cursor.close()
        return jsonify({"message": "Modalidade removida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao deletar modalidade: {str(e)}"}), 500


