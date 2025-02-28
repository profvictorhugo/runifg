import pymysql.cursors
from flask import Blueprint, request, jsonify
from db import mysql

categoria_bp = Blueprint('categoria', __name__)

@categoria_bp.route('/categoria/getAll', methods=['GET'])
def getAll():
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, corrida_id, prova_id, nome, TIME_FORMAT(previsao_hora_largada, '%H:%i:%s') as previsao_hora_largada, faixa_etaria_id FROM Categoria")
        categorias = cursor.fetchall()
        cursor.close()
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar categorias: {str(e)}"}), 500

@categoria_bp.route('/categoria/getById/<int:id>', methods=['GET'])
def getById(id):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, corrida_id, prova_id, nome, TIME_FORMAT(previsao_hora_largada, '%%H:%%i:%%s') as previsao_hora_largada, faixa_etaria_id FROM Categoria WHERE id=%s", (id,))
        categoria = cursor.fetchone()  # Usa fetchone() pois ID é único
        cursor.close()

        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({"error": "Categoria não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar categoria: {str(e)}"}), 500

@categoria_bp.route('/categoria/getAllByCorrida/<int:corrida_id>', methods=['GET'])
def getAllByCorrida(corrida_id):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, nome, prova_id, corrida_id, TIME_FORMAT(previsao_hora_largada, '%%H:%%i:%%s') as previsao_hora_largada, faixa_etaria_id FROM Categoria WHERE corrida_id=%s", (corrida_id,))
        categoria = cursor.fetchall()
        cursor.close()

        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({"error": "Categoria não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar categoria: {str(e)}"}), 500

@categoria_bp.route('/categoria/createCategoria', methods=['POST'])
def createCategoria():
    data = request.get_json()

    # Validação dos campos obrigatórios
    if not all(k in data for k in ('corrida_id', 'prova_id', 'nome', 'previsao_hora_largada', 'faixa_etaria_id')):
        return jsonify({"error": "Os campos corrida_id, prova_id, nome, previsao_hora_largada e faixa_etaria_id são obrigatórios"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Categoria (corrida_id, prova_id, nome, previsao_hora_largada, faixa_etaria_id) VALUES (%s, %s, %s, %s, %s)",
                       (data['corrida_id'], data['prova_id'], data['nome'], data['previsao_hora_largada'], data['faixa_etaria_id']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Categoria criada com sucesso!"}), 201

    except pymysql.err.IntegrityError as e:
        if "foreign key constraint fails" in str(e):
            return jsonify({"error": "Corrida, Prova ou Faixa Etária não encontrada"}), 409  # HTTP 409 - Conflito
        elif "Duplicate entry" in str(e):
            return jsonify({"error": "Categoria já cadastrada"}), 409  # Violação da chave única composta
        return jsonify({"error": f"Erro ao cadastrar categoria: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao cadastrar categoria: {str(e)}"}), 500

@categoria_bp.route('/categoria/updateCategoria/<int:id>', methods=['PUT'])
def updateCategoria(id):
    data = request.get_json()

    if not all(k in data for k in ('corrida_id', 'prova_id', 'nome', 'previsao_hora_largada', 'faixa_etaria_id')):
        return jsonify({"error": "Os campos corrida_id, prova_id, nome, previsao_hora_largada e faixa_etaria_id são obrigatórios"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Categoria SET corrida_id = %s, prova_id = %s, nome = %s, previsao_hora_largada = %s, faixa_etaria_id = %s WHERE id = %s",
                       (data['corrida_id'], data['prova_id'], data['nome'], data['previsao_hora_largada'], data['faixa_etaria_id'], id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Categoria não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Categoria atualizada com sucesso!"}), 200


    except pymysql.err.IntegrityError as e:
        if "foreign key constraint fails" in str(e):
            return jsonify({"error": "Corrida, Prova ou Faixa Etária não encontrada"}), 409  # HTTP 409 - Conflito
        elif "Duplicate entry" in str(e):
            return jsonify({"error": "Categoria já cadastrada"}), 409  # Violação da chave única composta
        return jsonify({"error": f"Erro ao atualizar categoria: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao atualizar categoria: {str(e)}"}), 500

@categoria_bp.route('/categoria/deleteCategoria/<int:id>', methods=['DELETE'])
def deleteCategoria(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM Categoria WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Categoria não encontrada"}), 404

        cursor.close()
        return jsonify({"message": "Categoria removida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao deletar categoria: {str(e)}"}), 500
