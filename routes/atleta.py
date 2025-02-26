from flask import Blueprint, request, jsonify
from db import mysql
import MySQLdb.cursors
import pymysql

atleta_bp = Blueprint('atleta', __name__)

@atleta_bp.route('/atleta/createAtleta', methods=['POST'])
def createAtleta():
    data = request.get_json()

    # Validação básica dos campos obrigatórios
    if not all(k in data for k in ('nome', 'cpf', 'sexo', 'data_nasc', 'email')):
        return jsonify({"error": "Todos os campos são obrigatórios (nome, cpf, sexo, data_nasc, email)"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Atleta (nome, cpf, sexo, data_nasc, email) VALUES (%s, %s, %s, %s, %s)",
                       (data['nome'], data['cpf'], data['sexo'], data['data_nasc'], data['email']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Atleta cadastrado com sucesso!"}), 201

    except pymysql.err.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "CPF já cadastrado"}), 409  # HTTP 409 - Conflito
        return jsonify({"error": f"Erro ao cadastrar atleta: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao cadastrar atleta: {str(e)}"}), 500


@atleta_bp.route('/atleta/getAll', methods=['GET'])
def getAll():

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Atleta")
        atletas = cursor.fetchall()
        cursor.close()
        return jsonify(atletas), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar atletas: {str(e)}"}), 500

@atleta_bp.route('/atleta/getById/<int:id>', methods=['GET'])
def getById(id):

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Atleta WHERE id = %s", (id,))
        atleta = cursor.fetchone()
        cursor.close()

        if atleta:
            return jsonify(atleta), 200
        else:
            return jsonify({"error": "Atleta não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar atleta: {str(e)}"}), 500

@atleta_bp.route('/atleta/getByCpf/<string:cpf>', methods=['GET'])
def getByCpf(cpf):

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Atleta WHERE cpf = %s", (cpf,))
        atleta = cursor.fetchone()
        cursor.close()

        if atleta:
            return jsonify(atleta), 200
        else:
            return jsonify({"error": "Atleta não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar atleta: {str(e)}"}), 500


@atleta_bp.route('/atleta/updateAtleta/<int:id>', methods=['PUT'])
def updateAtleta(id):
    data = request.get_json()

    if not all(k in data for k in ('nome', 'cpf', 'sexo', 'data_nasc', 'email')):
        return jsonify({"error": "Campos obrigatórios: nome, cpf, sexo, data_nasc, email"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Atualiza diretamente e verifica se algo foi alterado
        cursor.execute("UPDATE Atleta SET nome = %s, cpf = %s, sexo = %s, data_nasc = %s, email = %s WHERE id = %s",
                       (data['nome'], data['cpf'], data['sexo'], data['data_nasc'], data['email'], id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Atleta não encontrado ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Atleta atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar atleta: {str(e)}"}), 500

@atleta_bp.route('/atleta/deleteAtleta/<int:id>', methods=['DELETE'])
def deleteAtleta(id):
    try:
        cursor = mysql.connection.cursor()

        # Deleta diretamente e verifica se algo foi removido
        cursor.execute("DELETE FROM Atleta WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Atleta não encontrado"}), 404

        cursor.close()
        return jsonify({"message": "Atleta removido com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao deletar atleta: {str(e)}"}), 500
