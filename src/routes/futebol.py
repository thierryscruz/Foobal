from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.futebol import SessaoFutebol, db
from datetime import datetime
import random

futebol_bp = Blueprint('futebol', __name__)

def algoritmo_balanceamento(jogadores):
    """
    Algoritmo para balancear times baseado nos níveis dos jogadores
    """
    # Filtrar apenas jogadores com nome preenchido e pegar os 12 primeiros
    jogadores_validos = [j for j in jogadores if j.get('nome', '').strip()][:12]
    
    if len(jogadores_validos) < 12:
        return {
            'erro': f'Necessário pelo menos 12 jogadores. Encontrados apenas {len(jogadores_validos)}.'
        }
    
    # Separar por níveis
    nivel_1 = [j for j in jogadores_validos if j['nivel'] == 1]
    nivel_2 = [j for j in jogadores_validos if j['nivel'] == 2]
    nivel_3 = [j for j in jogadores_validos if j['nivel'] == 3]
    
    # Embaralhar para randomizar
    random.shuffle(nivel_1)
    random.shuffle(nivel_2)
    random.shuffle(nivel_3)
    
    time_a = []
    time_b = []
    reservas = []
    
    # Distribuir níveis 1 (nunca no mesmo time)
    if len(nivel_1) >= 2:
        time_a.append(nivel_1[0])
        time_b.append(nivel_1[1])
        if len(nivel_1) >= 3:
            # Se tem 3 ou mais, o terceiro vai para o time com menos jogadores nível 1
            time_a.append(nivel_1[2])
        # Resto vai para reserva
        reservas.extend(nivel_1[3:])
    elif len(nivel_1) == 1:
        time_a.append(nivel_1[0])
    
    # Distribuir níveis 2 e 3 alternadamente para equilibrar
    todos_outros = nivel_2 + nivel_3
    random.shuffle(todos_outros)
    
    for i, jogador in enumerate(todos_outros):
        if len(time_a) < 6 and len(time_b) < 6:
            if len(time_a) <= len(time_b):
                time_a.append(jogador)
            else:
                time_b.append(jogador)
        elif len(time_a) < 6:
            time_a.append(jogador)
        elif len(time_b) < 6:
            time_b.append(jogador)
        else:
            reservas.append(jogador)
    
    # Adicionar jogadores restantes (se houver mais de 12) às reservas
    if len(jogadores_validos) > 12:
        reservas.extend(jogadores_validos[12:])
    
    return {
        'time_a': time_a,
        'time_b': time_b,
        'reservas': reservas,
        'estatisticas': {
            'time_a_niveis': {
                '1': len([j for j in time_a if j['nivel'] == 1]),
                '2': len([j for j in time_a if j['nivel'] == 2]),
                '3': len([j for j in time_a if j['nivel'] == 3])
            },
            'time_b_niveis': {
                '1': len([j for j in time_b if j['nivel'] == 1]),
                '2': len([j for j in time_b if j['nivel'] == 2]),
                '3': len([j for j in time_b if j['nivel'] == 3])
            }
        }
    }

@futebol_bp.route('/sessoes', methods=['GET'])
@cross_origin()
def get_sessoes():
    """Listar todas as sessões"""
    sessoes = SessaoFutebol.query.order_by(SessaoFutebol.data_sessao.desc()).all()
    return jsonify([sessao.to_dict() for sessao in sessoes])

@futebol_bp.route('/sessoes', methods=['POST'])
@cross_origin()
def create_sessao():
    """Criar nova sessão"""
    data = request.json
    
    try:
        data_sessao = datetime.strptime(data['data_sessao'], '%Y-%m-%d').date()
        jogadores = data['jogadores']
        
        sessao = SessaoFutebol(data_sessao=data_sessao, jogadores=jogadores)
        db.session.add(sessao)
        db.session.commit()
        
        return jsonify(sessao.to_dict()), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@futebol_bp.route('/sessoes/<int:sessao_id>', methods=['GET'])
@cross_origin()
def get_sessao(sessao_id):
    """Obter sessão específica"""
    sessao = SessaoFutebol.query.get_or_404(sessao_id)
    return jsonify(sessao.to_dict())

@futebol_bp.route('/sessoes/<int:sessao_id>', methods=['PUT'])
@cross_origin()
def update_sessao(sessao_id):
    """Atualizar sessão"""
    sessao = SessaoFutebol.query.get_or_404(sessao_id)
    data = request.json
    
    try:
        if 'data_sessao' in data:
            sessao.data_sessao = datetime.strptime(data['data_sessao'], '%Y-%m-%d').date()
        if 'jogadores' in data:
            sessao.set_jogadores(data['jogadores'])
        
        db.session.commit()
        return jsonify(sessao.to_dict())
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@futebol_bp.route('/sessoes/<int:sessao_id>/sortear', methods=['POST'])
@cross_origin()
def sortear_times(sessao_id):
    """Sortear times para uma sessão"""
    sessao = SessaoFutebol.query.get_or_404(sessao_id)
    
    try:
        jogadores = sessao.get_jogadores()
        resultado = algoritmo_balanceamento(jogadores)
        
        if 'erro' in resultado:
            return jsonify(resultado), 400
        
        sessao.set_resultado(resultado)
        db.session.commit()
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@futebol_bp.route('/sessoes/por-data/<data_sessao>', methods=['GET'])
@cross_origin()
def get_sessao_por_data(data_sessao):
    """Obter sessão por data específica"""
    try:
        data_obj = datetime.strptime(data_sessao, '%Y-%m-%d').date()
        sessao = SessaoFutebol.query.filter_by(data_sessao=data_obj).first()
        
        if sessao:
            return jsonify(sessao.to_dict())
        else:
            # Retorna estrutura vazia para a data
            return jsonify({
                'data_sessao': data_sessao,
                'jogadores': [{'id': i+1, 'nome': '', 'nivel': 2} for i in range(20)],
                'resultado': None
            })
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@futebol_bp.route('/sessoes/salvar-automatico', methods=['POST'])
@cross_origin()
def salvar_automatico():
    """Salvar ou atualizar sessão automaticamente"""
    data = request.json
    
    try:
        data_obj = datetime.strptime(data['data_sessao'], '%Y-%m-%d').date()
        jogadores = data['jogadores']
        
        # Buscar sessão existente para a data
        sessao = SessaoFutebol.query.filter_by(data_sessao=data_obj).first()
        
        if sessao:
            # Atualizar sessão existente
            sessao.set_jogadores(jogadores)
            sessao.updated_at = datetime.utcnow()
        else:
            # Criar nova sessão
            sessao = SessaoFutebol(data_sessao=data_obj, jogadores=jogadores)
            db.session.add(sessao)
        
        db.session.commit()
        return jsonify(sessao.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@futebol_bp.route('/sortear-rapido', methods=['POST'])
@cross_origin()
def sortear_rapido():
    """Sortear times sem salvar sessão"""
    data = request.json
    
    try:
        jogadores = data['jogadores']
        resultado = algoritmo_balanceamento(jogadores)
        
        if 'erro' in resultado:
            return jsonify(resultado), 400
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

