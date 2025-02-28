import pymysql.cursors
from flask import Blueprint, request, jsonify
from db import mysql

inscricao_bp = Blueprint('inscricao', __name__)

@inscricao_bp.route('/corrida/<int:corrida_id>/inscricao/createInscricao', methods=['POST'])
def createInscricao(corrida_id):
    data = request.get_json()

    # Validação dos campos obrigatórios
    if not all(k in data for k in ('atleta_id', 'categoria_id')):
        return jsonify({"error": "Campos obrigatórios: atleta_id, categoria_id"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Inscricao (atleta_id, corrida_id, categoria_id, status) VALUES (%s, %s, %s, %s, 'ATIVA')",
                       (data['atleta_id'], corrida_id, data['categoria_id'],))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Inscrição realizada com sucesso!"}), 201


    except pymysql.err.IntegrityError as e:
        if "foreign key constraint fails" in str(e):
            return jsonify({"error": "Atleta, corrida ou categoria não encontrados"}), 409  # HTTP 409 - Conflito
        elif "Duplicate entry" in str(e):
            return jsonify({"error": "Inscrição já realizada"}), 409  # Violação da chave única composta
        return jsonify({"error": f"Erro ao realizar inscrição: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Erro inesperado ao criar inscrição: {str(e)}"}), 500


@inscricao_bp.route('/inscricao/getAll', methods=['GET'])
def getAll():
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, atleta_id, corrida_id, categoria_id, numero, TIME_FORMAT(hora_largada, '%H:%i:%s') as hora_largada, TIME_FORMAT(hora_chegada, '%H:%i:%s') as hora_chegada, classificacao, status  FROM Inscricao")
        inscricoes = cursor.fetchall()
        cursor.close()
        return jsonify(inscricoes), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inscrições: {str(e)}"}), 500

@inscricao_bp.route('/inscricao/getById/<int:id>', methods=['GET'])
def getById(id):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, atleta_id, corrida_id, categoria_id, numero, TIME_FORMAT(hora_largada, '%%H:%%i:%%s') as hora_largada, TIME_FORMAT(hora_chegada, '%%H:%%i:%%s') as hora_chegada, classificacao, status FROM Inscricao WHERE id=%s", (id,))
        inscricao = cursor.fetchone()
        cursor.close()

        if inscricao:
            return jsonify(inscricao), 200
        else:
            return jsonify({"error": "Inscrição não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inscrição: {str(e)}"}), 500

@inscricao_bp.route('/inscricao/getAllByCategoria/<int:categoria_id>', methods=['GET'])
def getAllByCategoria(categoria_id):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, atleta_id, corrida_id, categoria_id, numero, TIME_FORMAT(hora_largada, '%%H:%%i:%%s') as hora_largada, TIME_FORMAT(hora_chegada, '%%H:%%i:%%s') as hora_chegada, classificacao, status FROM Inscricao WHERE categoria_id=%s", (categoria_id,))
        inscricao = cursor.fetchall()
        cursor.close()

        if inscricao:
            return jsonify(inscricao), 200
        else:
            return jsonify({"error": "Inscrição não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inscrição: {str(e)}"}), 500

@inscricao_bp.route('/corrida/<int:corrida_id>/inscricao/getAllByCorrida', methods=['GET'])
def getAllByCorrida(corrida_id):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, atleta_id, corrida_id, categoria_id, numero, TIME_FORMAT(hora_largada, '%%H:%%i:%%s') as hora_largada, TIME_FORMAT(hora_chegada, '%%H:%%i:%%s') as hora_chegada, classificacao, status FROM Inscricao WHERE corrida_id = %s", (corrida_id,))

        inscricao = cursor.fetchall()
        cursor.close()

        if inscricao:
            return jsonify(inscricao), 200
        else:
            return jsonify({"error": "Inscrição não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inscrição: {str(e)}"}), 500

@inscricao_bp.route('/corrida/<int:corrida_id>/inscricao/getByNumero/<int:numero>', methods=['GET'])
def getByNumero(corrida_id, numero):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, atleta_id, corrida_id, categoria_id, numero, TIME_FORMAT(hora_largada, '%%H:%%i:%%s') as hora_largada, TIME_FORMAT(hora_chegada, '%%H:%%i:%%s') as hora_chegada, classificacao, status FROM Inscricao WHERE corrida_id = %s AND numero = %s", (corrida_id, numero,))

        inscricao = cursor.fetchone()
        cursor.close()

        if inscricao:
            return jsonify(inscricao), 200
        else:
            return jsonify({"error": "Inscrição não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inscrição: {str(e)}"}), 500

@inscricao_bp.route('/corrida/<int:corrida_id>/inscricao/getByCpf/<string:cpf>', methods=['GET'])
def getByCpf(corrida_id, cpf):
    try:
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT i.id, i.atleta_id, i.corrida_id, i.categoria_id, i.numero, TIME_FORMAT(i.hora_largada, '%%H:%%i:%%s') as hora_largada, TIME_FORMAT(i.hora_chegada, '%%H:%%i:%%s') as hora_chegada, i.classificacao, i.status FROM Inscricao AS i JOIN Atleta as a ON a.id = i.atleta_id WHERE i.corrida_id = %s AND a.cpf = %s", (corrida_id, cpf,))

        inscricao = cursor.fetchone()
        cursor.close()

        if inscricao:
            return jsonify(inscricao), 200
        else:
            return jsonify({"error": "Inscrição não encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inscrição: {str(e)}"}), 500


@inscricao_bp.route('/inscricao/cancelarInscricao/<int:id>', methods=['PUT'])
def cancelarInscricao(id):

    try:
        cursor = mysql.connection.cursor()

        # Atualiza diretamente e verifica se algo foi alterado
        cursor.execute("UPDATE Inscricao SET status = 'CANCELADA' WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Inscrição não encontrada ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Inscrição cancelada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao cancelar inscrição: {str(e)}"}), 500

@inscricao_bp.route('/inscricao/updateLargada/<int:categoria_id>', methods=['PUT'])
def updateLargada(categoria_id):
    data = request.get_json()

    if 'hora_largada' not in data:
        return jsonify({"error": "Campos obrigatórios: hora_largada"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Atualiza diretamente e verifica se algo foi alterado
        cursor.execute("UPDATE Inscricao SET hora_largada = %s WHERE categoria_id = %s",
                       (data['hora_largada'], categoria_id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Inscrições não encontradas ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Hora_largada atualizada com sucesso!"}), 200

    except pymysql.err.IntegrityError as e:
        if "foreign key constraint fails" in str(e):
            return jsonify({"error": "Atleta ou Categoria não encontrados"}), 409  # HTTP 409 - Conflito
        elif "Duplicate entry" in str(e):
            return jsonify({"error": "Inscrição já realizada"}), 409  # Violação da chave única composta
        return jsonify({"error": f"Erro ao atualizar inscrição: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar inscrição: {str(e)}"}), 500


@inscricao_bp.route('/inscricao/updateNumero/<int:id>', methods=['PUT'])
def updateNumero(id):
    data = request.get_json()

    if 'numero' not in data:
        return jsonify({"error": "Campos obrigatórios: numero"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Atualiza diretamente e verifica se algo foi alterado
        cursor.execute("UPDATE Inscricao SET numero = %s WHERE id = %s",
                       (data['numero'], id))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Inscrições não encontradas ou dados idênticos"}), 404

        cursor.close()
        return jsonify({"message": "Número atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar número da inscrição: {str(e)}"}), 500

@inscricao_bp.route('/corrida/<int:corrida_id>/inscricao/updateChegada/<int:numero>', methods=['PUT'])
def updateChegada(corrida_id, numero):
    data = request.get_json()

    if 'hora_chegada' not in data:
        return jsonify({"error": "O campo 'hora_chegada' é obrigatório"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Atualiza a inscrição apenas se ela pertencer à corrida especificada
        cursor.execute("""
            UPDATE Inscricao AS i
            SET i.hora_chegada = %s, i.status = 'ENCERRADA'
            WHERE i.numero = %s AND i.corrida_id = %s
        """, (data['hora_chegada'], numero, corrida_id))

        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Inscrição não encontrada para esta corrida ou hora de chegada já cadastrada"}), 404

        cursor.close()
        return jsonify({"message": "Hora de chegada atualizada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar hora de chegada: {str(e)}"}), 500


@inscricao_bp.route('/inscricao/updateClassificacao/<int:categoria_id>', methods=['PUT'])
def updateClassificacao(categoria_id):
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT id 
            FROM Inscricao 
            WHERE categoria_id = %s AND status = 'ENCERRADA'
            ORDER BY hora_chegada ASC;
        """, (categoria_id,))

        inscricoes = cursor.fetchall()

        posicao = 1

        for inscricao in inscricoes:
            cursor.execute("""
                UPDATE Inscricao
                SET classificacao = %s
                WHERE id = %s;
            """, (posicao, inscricao[0]))
            posicao += 1  # Incrementa a posição

        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Nenhuma inscrição encontrada para esta categoria"}), 404

        cursor.close()
        return jsonify({"message": "Classificações atualizadas com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar classificações: {str(e)}"}), 500


@inscricao_bp.route('/inscricao/deleteInscricao/<int:id>', methods=['DELETE'])
def deleteInscricao(id):
    try:
        cursor = mysql.connection.cursor()

        # Deleta diretamente e verifica se algo foi removido
        cursor.execute("DELETE FROM Inscricao WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Inscrição não encontrada"}), 404

        cursor.close()
        return jsonify({"message": "Inscrição removida com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao deletar inscrição: {str(e)}"}), 500
