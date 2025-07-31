from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class SessaoFutebol(db.Model):
    __tablename__ = 'sessao_futebol'
    
    id = db.Column(db.Integer, primary_key=True)
    data_sessao = db.Column(db.Date, nullable=False)
    jogadores_json = db.Column(db.Text, nullable=False)  # JSON com lista de jogadores
    resultado_json = db.Column(db.Text, nullable=True)   # JSON com resultado do sorteio
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, data_sessao, jogadores):
        self.data_sessao = data_sessao
        self.jogadores_json = json.dumps(jogadores)
    
    def get_jogadores(self):
        return json.loads(self.jogadores_json)
    
    def set_jogadores(self, jogadores):
        self.jogadores_json = json.dumps(jogadores)
    
    def get_resultado(self):
        if self.resultado_json:
            return json.loads(self.resultado_json)
        return None
    
    def set_resultado(self, resultado):
        self.resultado_json = json.dumps(resultado)
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_sessao': self.data_sessao.isoformat() if self.data_sessao else None,
            'jogadores': self.get_jogadores(),
            'resultado': self.get_resultado(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

