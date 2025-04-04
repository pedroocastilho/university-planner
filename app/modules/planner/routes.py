from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Estudo
from datetime import datetime, date

planner_bp = Blueprint("planner", __name__, url_prefix="/planner")

CORES_CATEGORIAS = {
    "Prova": "#f28b82",        # vermelho claro
    "Aula": "#aecbfa",         # azul pastel
    "Atendimento": "#b7e1cd",  # verde suave
    "Academia": "#ffd6a5",     # laranja pastel
    "Pessoal": "#f4b6c2"       # rosa médio
}

@planner_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        categoria = request.form["categoria"]
        data = request.form["data"]
        materia = request.form.get("materia", "")

        if categoria in ["Prova", "Aula"] and not materia:
            return redirect(url_for("planner.index"))

        if categoria not in ["Prova", "Aula"]:
            materia = ""

        novo_estudo = Estudo(materia=materia, data=data, categoria=categoria)
        db.session.add(novo_estudo)
        db.session.commit()
        return redirect(url_for("planner.index"))

    materia_filtro = request.args.get("materia")
    data_filtro = request.args.get("data")

    estudos_query = Estudo.query
    if materia_filtro:
        estudos_query = estudos_query.filter_by(materia=materia_filtro)
    if data_filtro:
        try:
            data_obj = datetime.strptime(data_filtro, "%Y-%m-%d").date()
            estudos_query = estudos_query.filter_by(data=data_obj)
        except ValueError:
            pass

    estudos = estudos_query.order_by(Estudo.data).all()

    dados = []
    for e in estudos:
        try:
            data_formatada = e.data.strftime("%Y-%m-%d")
        except AttributeError:
            data_formatada = e.data

        dados.append({
            "id": e.id,
            "materia": e.materia,
            "data": data_formatada,
            "categoria": e.categoria,
            "cor": CORES_CATEGORIAS.get(e.categoria, "gray"),
            "passado": datetime.strptime(data_formatada, "%Y-%m-%d").date() < date.today()
        })

    materias_unicas = sorted(set(e.materia for e in estudos if e.materia))

    return render_template("planner/index.html", dados=dados, materias=materias_unicas)

@planner_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    estudo = Estudo.query.get_or_404(id)

    if request.method == "POST":
        if "deletar" in request.form:
            db.session.delete(estudo)
            db.session.commit()
            return redirect(url_for("planner.index"))

        estudo.materia = request.form["materia"]
        estudo.data = request.form["data"]
        estudo.categoria = request.form["categoria"]
        db.session.commit()
        return redirect(url_for("planner.index"))

    return render_template("planner/editar.html", estudo=estudo)
