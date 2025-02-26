from flask import Blueprint
from routes.atleta import atleta_bp
from .inscricao import inscricao_bp
from .corrida import corrida_bp
from routes.prova import prova_bp
from .modalidade import modalidade_bp
from .faixaEtaria import faixa_etaria_bp
from routes.categoria import categoria_bp
from .classificacoes import classificacoes_bp

bp = Blueprint('runIFG', __name__)

bp.register_blueprint(atleta_bp)
bp.register_blueprint(inscricao_bp)
bp.register_blueprint(corrida_bp)
bp.register_blueprint(prova_bp)
bp.register_blueprint(modalidade_bp)
bp.register_blueprint(faixa_etaria_bp)
bp.register_blueprint(categoria_bp)
bp.register_blueprint(classificacoes_bp)
