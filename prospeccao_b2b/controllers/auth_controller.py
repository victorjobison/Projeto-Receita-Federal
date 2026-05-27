from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from services.auth_service import AuthService
from services.token_service import TokenService


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = AuthService.authenticate(
            request.form.get("email", ""),
            request.form.get("senha", ""),
        )
        if user:
            session.clear()
            session["user_id"] = user["id"]
            flash("Login realizado com sucesso.", "success")
            return redirect(request.args.get("next") or url_for("companies.dashboard"))

        flash("E-mail ou senha invalidos.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sessao encerrada.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    user = AuthService.authenticate(data.get("email", ""), data.get("senha", ""))
    if not user:
        return jsonify({"status": False, "mensagem": "E-mail ou senha invalidos."}), 401

    return jsonify(
        {
            "status": True,
            "access_token": TokenService.create_access_token(user),
            "refresh_token": TokenService.create_refresh_token(user["id"]),
            "token_type": "bearer",
        }
    )


@auth_bp.route("/api/auth/refresh", methods=["POST"])
def api_refresh():
    data = request.get_json(silent=True) or {}
    access_token = TokenService.refresh_access_token(data.get("refresh_token", ""))
    if not access_token:
        return jsonify({"status": False, "mensagem": "Refresh token invalido ou expirado."}), 401

    return jsonify({"status": True, "access_token": access_token, "token_type": "bearer"})


@auth_bp.route("/api/auth/revoke", methods=["POST"])
def api_revoke():
    data = request.get_json(silent=True) or {}
    TokenService.revoke_refresh_token(data.get("refresh_token", ""))
    return jsonify({"status": True, "mensagem": "Refresh token revogado."})


@auth_bp.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    reset_link = None
    if request.method == "POST":
        token = AuthService.request_password_reset(request.form.get("email", ""))
        if token:
            reset_link = url_for("auth.resetar_senha", token=token, _external=True)

        flash(
            "Se o e-mail existir, um link de recuperacao sera disponibilizado/enviado.",
            "success",
        )

    return render_template("auth/forgot_password.html", reset_link=reset_link)


@auth_bp.route("/resetar-senha/<token>", methods=["GET", "POST"])
def resetar_senha(token):
    if request.method == "POST":
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")
        if senha != confirmar:
            flash("As senhas nao conferem.", "error")
        elif len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres.", "error")
        elif AuthService.reset_password(token, senha):
            flash("Senha redefinida com sucesso.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Token expirado ou invalido.", "error")

    return render_template("auth/reset_password.html", token=token)
