from flask import Blueprint, render_template, request, redirect, url_for, session
from .data import (
    casos_terapeutica, casos_semiologia_medica, casos_semiologia_quirurgica,
    casos_trauma, casos_patologia, casos_gineco
)
import random

casos_bp = Blueprint('casos', __name__, template_folder='../../../templates/casos_clinicos')

materias_casos_clinicos = {
    "Terapéutica y Toxicología": casos_terapeutica,
    "Semiología Médica": casos_semiologia_medica,
    "Semiología Quirúrgica": casos_semiologia_quirurgica,
    "Traumatología": casos_trauma,
    "Patología Quirúrgica": casos_patologia,
    "Ginecología y Obstetricia": casos_gineco
}

@casos_bp.route('/')
def selecionar_materia():
    return render_template('casos_clinicos/materias.html', materias=materias_casos_clinicos.keys())

@casos_bp.route('/casos/')
def iniciar_simulado():
    materia = request.args.get('materia')
    if materia not in materias_casos_clinicos:
        return redirect(url_for('casos.selecionar_materia'))

    casos = list(materias_casos_clinicos[materia])
    random.shuffle(casos)

    session['casos'] = casos
    session['materia'] = materia
    session['acertos'] = 0
    session['erros'] = 0

    return redirect(url_for('casos.caso', idx=0))

@casos_bp.route('/casos/<int:idx>', methods=['GET', 'POST'])
def caso(idx):
    casos = session.get('casos')
    materia = session.get('materia')

    if not casos or idx >= len(casos):
        return redirect(url_for('casos.selecionar_materia'))

    caso_atual = casos[idx]

    if request.method == 'POST':
        resposta_usuario = int(request.form.get('resposta'))
        correta = caso_atual['correta']
        explicacao = caso_atual['explicacao']
        acertou = (resposta_usuario == correta)

        if acertou:
            session['acertos'] += 1
        else:
            session['erros'] += 1

        return render_template(
            'casos_clinicos/caso.html',
            caso=caso_atual,
            idx=idx,
            materia=materia,
            mostrar_explicacao=True,
            resposta=resposta_usuario,
            correta=correta,
            explicacao=explicacao,
            acertou=acertou,
            tem_mais=(idx + 1 < len(casos))
        )

    return render_template('casos_clinicos/caso.html', caso=caso_atual, idx=idx, materia=materia)

@casos_bp.route('/casos/resultado')
def resultado_final():
    acertos = session.pop('acertos', 0)
    erros = session.pop('erros', 0)
    materia = session.pop('materia', '')
    session.pop('casos', None)

    return render_template(
        'casos_clinicos/resultado.html',
        acertos=acertos,
        erros=erros,
        materia=materia
    )
