from flask import Blueprint, request, jsonify
from db import mysql
import pymysql.cursors

faixa_etaria_bp = Blueprint('faixa_etaria', __name__)

@faixa_etaria_bp.route('/faixa_etaria/getAll', methods=['GET'])
def getAll():
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM FaixaEtaria")
        faixas = cursor.fetchall()
        cursor.close()
        return jsonify(faixas), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar faixas etárias: {str(e)}"}), 500

@faixa_etaria_bp.route('/faixa_etaria/getById/<int:id>', methods=['GET'])
def getById(id):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM FaixaEtaria WHERE id=%s", (id,))
        faixa = cursor.fetchone()  # Usa fetchone() pois ID é único
        cursor.close()

        if faixa:
            return jsonify(faixa), 200
        else:
            return jsonify({"error": "Faixa etária não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar faixa etária: {str(e)}"}), 500

@faixa_etaria_bp.route('/faixa_etaria/createFaixaEtaria', methods=['POST'])
def createFaixaEtaria():
    data = request.get_json()

    # Validação dos campos obrigatórios
    if 'faixa_etaria' not in data:
        return jsonify({"error": "O campo faixa_etaria é obrigatório"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO FaixaEtaria (faixa_etaria) VALUES (%s)",
                       (data['faixa_etaria'],))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Faixa etária criada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao cadastrar faixa etária: {str(e)}"}), 500

@faixa_etaria_bp.route('/faixa_etaria/updateFaixaEtaria/<int:id>', methods=['PUT'])
def updateFaixaEtaria(id):
    data = request.get_json()

    if 'faixa_etaria' not in data:
        return jsonify({"error": "O campo faixa_etaria é obrigatório"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Atualiza diretamente e verifica se algo foi alterado
        cursor.execute("UPDATE FaixaEtaria SET faixa_etaria = %s WHERE id = %s",
                       (data['faixa_etaria'], id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Faixa etária não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Faixa etária atualizada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar faixa etária: {str(e)}"}), 500

@faixa_etaria_bp.route('/faixa_etaria/deleteFaixaEtaria/<int:id>', methods=['DELETE'])
def deleteFaixaEtaria(id):
    try:
        cursor = mysql.connection.cursor()

        # Deleta diretamente e verifica se algo foi removido
        cursor.execute("DELETE FROM FaixaEtaria WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Faixa etária não encontrada"}), 404

        cursor.close()
        return jsonify({"message": "Faixa etária removida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao deletar faixa etária: {str(e)}"}), 500
