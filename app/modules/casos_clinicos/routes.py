from flask import Blueprint, render_template, request, redirect, url_for, session
from .data import (
    casos_terapeutica, casos_semiologia_medica, casos_semiologia_quirurgica,
    casos_trauma, casos_patologia, casos_gineco
)

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

    session['acertos'] = 0
    session['erros'] = 0
    return redirect(url_for('casos.caso', materia=materia, idx=0))

@casos_bp.route('/casos/<materia>/<int:idx>', methods=['GET', 'POST'])
def caso(materia, idx):
    casos = materias_casos_clinicos.get(materia)
    if not casos or idx >= len(casos):
        return redirect(url_for('casos.selecionar_materia'))

    # Garante que os contadores existem
    if 'acertos' not in session:
        session['acertos'] = 0
    if 'erros' not in session:
        session['erros'] = 0

    caso_atual = casos[idx]

    if request.method == 'POST':
        resposta_usuario = int(request.form.get('resposta'))
        correta = caso_atual['correta']
        explicacao = caso_atual['explicacao']
        acertou = (resposta_usuario == correta)

        # Atualiza os contadores na sessão
        if acertou:
            session['acertos'] += 1
        else:
            session['erros'] += 1

        ultima_pergunta = (idx + 1 >= len(casos))

        if ultima_pergunta:
            total_acertos = session['acertos']
            total_erros = session['erros']
            session['acertos'] = 0
            session['erros'] = 0

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
                tem_mais=False,
                resumo_final=True,
                total_acertos=total_acertos,
                total_erros=total_erros
            )

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
            tem_mais=True
        )

    return render_template('casos_clinicos/caso.html', caso=caso_atual, idx=idx, materia=materia)
