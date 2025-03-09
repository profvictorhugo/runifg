import requests
from flask import Blueprint, request, jsonify
from config import Config  # Importa a configuração

auth_bp = Blueprint('auth', __name__)

def verificar_recaptcha(recaptcha_response):
    """Verifica a resposta do reCAPTCHA na API do Google"""
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": Config.RECAPTCHA_SECRET_KEY,
        "response": recaptcha_response
    }
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get("success", False)  # Retorna True se a verificação for bem-sucedida

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    # Verifica se usuário, senha e reCAPTCHA foram informados
    if not data or 'usuario' not in data or 'senha' not in data or 'recaptcha' not in data:
        return jsonify({"error": "Usuário, senha e reCAPTCHA são obrigatórios"}), 400

    usuario = data['usuario']
    senha = data['senha']
    recaptcha_response = data['recaptcha']

    # Verifica o reCAPTCHA
    #if not verificar_recaptcha(recaptcha_response):
    #    return jsonify({"error": "Falha na validação do reCAPTCHA"}), 403

    # Verifica se o usuário existe e a senha está correta
    if usuario in Config.USERS and Config.USERS[usuario] == senha:
        return jsonify({"message": "Login bem-sucedido!", "usuario": usuario}), 200
    else:
        return jsonify({"error": "Usuário ou senha inválidos"}), 401
