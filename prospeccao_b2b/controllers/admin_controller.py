from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.user_model import UserModel
from services.admin_service import AdminService
from utils.auth import admin_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/consultores")
@admin_required
def consultores():
    return render_template(
        "admin/consultores.html",
        consultores=UserModel.list_consultores(),
    )


@admin_bp.route("/consultores", methods=["POST"])
@admin_required
def criar_consultor():
    try:
        AdminService.criar_consultor(
            request.form.get("nome", ""),
            request.form.get("email", ""),
            request.form.get("senha", ""),
            request.form.get("perfil", "CONSULTOR"),
        )
        flash("Usuario cadastrado.", "success")
    except Exception as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin.consultores"))


@admin_bp.route("/consultores/<int:user_id>", methods=["POST"])
@admin_required
def editar_consultor(user_id):
    try:
        AdminService.editar_consultor(
            user_id,
            request.form.get("nome", ""),
            request.form.get("email", ""),
            request.form.get("perfil", "CONSULTOR"),
            request.form.get("ativo") == "on",
        )
        flash("Usuario atualizado.", "success")
    except Exception as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin.consultores"))


@admin_bp.route("/relatorio")
@admin_required
def relatorio():
    return render_template(
        "admin/relatorio.html",
        relatorio=AdminService.relatorio_global(),
    )
