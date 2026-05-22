from datetime import datetime
from functools import wraps

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.services.ai_gemini_service import AIGeminiService
from app.services.calendar_service import CalendarService
from app.services.user_service import UserService

main_bp = Blueprint("main", __name__)
ai_service = AIGeminiService()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            if request.is_json:
                return jsonify({"error": "Autenticação necessária"}), 401
            flash("Por favor, faça login para acessar esta página.", "warning")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    return decorated_function


@main_bp.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("main.agenda"))
    return redirect(url_for("main.login"))


@main_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            email = data.get("email")
            password = data.get("senha") or data.get("password")
            name = data.get("nome") or data.get("name")
        else:
            email = request.form.get("email")
            password = request.form.get("senha") or request.form.get("password")
            name = request.form.get("nome") or request.form.get("name")

        if not email or not password:
            msg = "Email e senha são obrigatórios"
            if request.is_json:
                return jsonify({"error": msg}), 400
            flash(msg, "danger")
            return render_template("cadastro.html")

        success, result = UserService.register_user(email, password, name=name)
        if success:
            if request.is_json:
                return jsonify(
                    {"message": "Usuário registrado com sucesso", "user_id": result.id}
                ), 201
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for("main.login"))
        else:
            if request.is_json:
                return jsonify({"error": result}), 400
            flash(result, "danger")

    return render_template("cadastro.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            email = data.get("email")
            password = data.get("senha") or data.get("password")
        else:
            email = request.form.get("email")
            password = request.form.get("senha") or request.form.get("password")

        success, result = UserService.authenticate_user(email, password)
        if success:
            session["user_id"] = result.id
            session["user_email"] = result.email
            if request.is_json:
                return jsonify(
                    {
                        "message": "Login realizado com sucesso",
                        "user": {"id": result.id, "email": result.email},
                    }
                ), 200
            return redirect(url_for("main.agenda"))
        else:
            if request.is_json:
                return jsonify({"error": result}), 401
            flash(result, "danger")

    return render_template("login.html")


@main_bp.route("/logout")
def logout():
    session.clear()
    if request.is_json:
        return jsonify({"message": "Logout realizado com sucesso"}), 200
    flash("Sessão encerrada.", "info")
    return redirect(url_for("main.login"))


@main_bp.route('/agenda')
@login_required
def agenda():
    from app.models import db, User
    user = db.session.get(User, session['user_id'])


    # Calculate initials
    initials = ""
    if user and user.name:
        parts = user.name.split()
        if len(parts) >= 2:
            initials = (parts[0][0] + parts[-1][0]).upper()
        elif len(parts) == 1:
            initials = parts[0][0].upper()
    else:
        initials = session["user_email"][0].upper()

    events = CalendarService.get_user_events(session["user_id"])
    formatted_events = []
    for e in events:
        formatted_events.append(
            {
                "id": str(e.id),
                "title": e.title,
                "start": e.start_time.isoformat(),
                "end": e.end_time.isoformat() if e.end_time else None,
                "extendedProps": {
                    "description": e.description or "",
                    "is_ai_generated": e.is_ai_generated,
                },
                "color": "#6610f2" if e.is_ai_generated else "#0d6efd",
            }
        )
    return render_template("agenda.html", eventos=formatted_events, iniciais=initials)


@main_bp.route("/ia/prompt", methods=["POST"])
@login_required
def ia_prompt():
    prompt = request.form.get("prompt")
    if not prompt:
        flash("Prompt é obrigatório", "warning")
        return redirect(url_for("main.agenda"))

    event_data = ai_service.process_annotation_prompt(prompt)

    if "error" in event_data:
        flash(f"Erro da IA: {event_data['error']}", "danger")
        return redirect(url_for("main.agenda"))

    try:
        start_time = datetime.fromisoformat(
            event_data["start_time"].replace("Z", "+00:00")
        )
        end_time = (
            datetime.fromisoformat(event_data["end_time"].replace("Z", "+00:00"))
            if event_data.get("end_time")
            else None
        )

        CalendarService.add_event(
            session["user_id"],
            event_data["title"],
            event_data.get("description", ""),
            start_time,
            end_time,
            is_ai_generated=True,
        )
        flash("Evento agendado com sucesso pela IA!", "success")
    except Exception as e:
        flash(f"Erro ao salvar evento: {str(e)}", "danger")

    return redirect(url_for("main.agenda"))


@main_bp.route("/ia/rotina", methods=["POST"])
@login_required
def ia_rotina():
    tipo_rotina = request.form.get("tipo_rotina")
    dias = request.form.get("dias", 7)
    inicio = request.form.get("inicio", "hoje")
    contexto = request.form.get("contexto", "")

    if not tipo_rotina:
        flash("Tipo de rotina é obrigatório", "warning")
        return redirect(url_for("main.agenda"))

    success, result = ai_service.generate_routine_and_save(
        session["user_id"],
        tipo_rotina,
        contexto or f"Rotina de {tipo_rotina}",
        int(dias),
        start_reference=inicio,
    )

    if success:
        flash(f"Rotina de {tipo_rotina} gerada com sucesso!", "success")
    else:
        flash(result, "danger")

    return redirect(url_for("main.agenda"))


@main_bp.route('/evento/add', methods=['POST'])
@login_required
def add_event():
    title = request.form.get('title')
    description = request.form.get('description')
    start_time_str = request.form.get('start_time')

    if not title or not start_time_str:
        flash("Título e data são obrigatórios", "warning")
        return redirect(url_for('main.agenda'))

    try:
        start_time = datetime.fromisoformat(start_time_str)
        CalendarService.add_event(session['user_id'], title, description, start_time)
        flash("Evento adicionado com sucesso!", "success")
    except ValueError:
        flash("Formato de data inválido.", "danger")
        
    return redirect(url_for('main.agenda'))

@main_bp.route("/evento/editar/<int:evento_id>", methods=["POST"])
@login_required
def editar_evento(evento_id):
    title = request.form.get("title")
    description = request.form.get("description")
    start_time_str = request.form.get("start_time")

    if not title or not start_time_str:
        flash("Título e data são obrigatórios", "warning")
        return redirect(url_for("main.agenda"))

    try:
        start_time = datetime.fromisoformat(start_time_str)
        success, result = CalendarService.update_event(
            evento_id, session["user_id"], title, description, start_time
        )
        if success:
            flash("Evento atualizado.", "success")
        else:
            flash(result, "danger")
    except ValueError:
        flash("Formato de data inválido.", "danger")

    return redirect(url_for("main.agenda"))


@main_bp.route("/evento/deletar", methods=["POST"])
@login_required
def deletar_evento():
    evento_id = request.form.get("evento_id")
    if not evento_id:
        flash("ID do evento é obrigatório", "warning")
        return redirect(url_for("main.agenda"))

    if CalendarService.delete_event(evento_id, session["user_id"]):
        flash("Evento removido.", "success")
    else:
        flash("Evento não encontrado.", "danger")

    return redirect(url_for("main.agenda"))


@main_bp.route("/api/user/password", methods=["PUT"])
@login_required
def update_password():
    data = request.get_json()
    new_password = data.get("new_password")
    if not new_password:
        return jsonify({"error": "Nova senha é obrigatória"}), 400

    success, message = UserService.update_password(session["user_id"], new_password)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400


@main_bp.route("/api/user", methods=["DELETE"])
@login_required
def delete_user():
    success, message = UserService.delete_user(session["user_id"])
    if success:
        session.clear()
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400
