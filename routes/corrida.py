import pymysql.cursors
from flask import Blueprint, request, jsonify
from db import mysql

corrida_bp = Blueprint('corrida', __name__)

@corrida_bp.route('/corrida/getAll', methods=['GET'])
def getAll():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nome, modalidade_id, data, TIME_FORMAT(horario, '%%H:%%i:%%s') as horario, local, status FROM Corrida")
        corridas = cursor.fetchall()
        cursor.close()
        return jsonify(corridas), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar corridas: {str(e)}"}), 500

@corrida_bp.route('/corrida/getById/<int:id>', methods=['GET'])
def getById(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nome, modalidade_id, data, TIME_FORMAT(horario, '%%H:%%i:%%s') as horario, local, status FROM Corrida WHERE id=%s", (id,))
        corrida = cursor.fetchone()
        cursor.close()

        if corrida:
            return jsonify(corrida), 200
        else:
            return jsonify({"error": "Corrida não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar corrida: {str(e)}"}), 500

@corrida_bp.route('/corrida/createCorrida', methods=['POST'])
def createCorrida():
    data = request.get_json()

    # Validação dos campos obrigatórios
    if not all(k in data for k in ('nome', 'modalidade_id', 'data', 'horario', 'local')):
        return jsonify({"error": "Os campos nome, modalidade_id, data, horario e local são obrigatórios"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Corrida (nome, modalidade_id, data, horario, local, status) VALUES (%s, %s, %s, %s, %s, 'ATIVA')",
                       (data['nome'], data['modalidade_id'], data['data'], data['horario'], data['local']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Corrida criada com sucesso!"}), 201

    except pymysql.err.IntegrityError as e:
        if "foreign key constraint fails" in str(e):
            return jsonify({"error": "Modalidade não encontrada"}), 409  # HTTP 409 - Conflito
        return jsonify({"error": f"Erro ao cadastrar corrida: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao cadastrar corrida: {str(e)}"}), 500

@corrida_bp.route('/corrida/updateCorrida/<int:id>', methods=['PUT'])
def updateCorrida(id):
    data = request.get_json()

    if not all(k in data for k in ('nome', 'modalidade_id', 'data', 'horario', 'local')):
        return jsonify({"error": "Os campos nome, modalidade_id, data, horario e local são obrigatórios"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Corrida SET nome = %s, modalidade_id = %s, data = %s, horario = %s, local = %s WHERE id = %s",
                       (data['nome'], data['modalidade_id'], data['data'], data['horario'], data['local'], id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Corrida não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Corrida atualizada com sucesso!"}), 200

    except pymysql.err.IntegrityError as e:
        if "foreign key constraint fails" in str(e):
            return jsonify({"error": "Modalidade não encontrada"}), 409  # HTTP 409 - Conflito
        return jsonify({"error": f"Erro ao atualizar corrida: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao atualizar corrida: {str(e)}"}), 500

@corrida_bp.route('/corrida/cancelaCorrida/<int:id>', methods=['PUT'])
def cancelaCorrida(id):

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Corrida SET status = 'CANCELADA' WHERE id = %s",
                       (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Corrida não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Corrida cancelada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao cancelar corrida: {str(e)}"}), 500


@corrida_bp.route('/corrida/encerraCorrida/<int:id>', methods=['PUT'])
def encerraCorrida(id):

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Corrida SET status = 'ENCERRADA' WHERE id = %s",
                       (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Corrida não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Corrida encerrada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao encerrar corrida: {str(e)}"}), 500


@corrida_bp.route('/corrida/deleteCorrida/<int:id>', methods=['DELETE'])
def deleteCorrida(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM Corrida WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Corrida não encontrada"}), 404

        cursor.close()
        return jsonify({"message": "Corrida removida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao deletar corrida: {str(e)}"}), 500
