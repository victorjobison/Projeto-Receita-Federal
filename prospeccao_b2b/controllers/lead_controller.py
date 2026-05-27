"""Rotas do funil de leads e historico de interacoes."""

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for

from models.interaction_model import InteractionModel, TIPOS_INTERACAO
from models.lead_model import LeadModel, STATUS_LEAD
from models.user_model import UserModel
from services.lead_service import LeadService
from utils.auth import admin_required, login_required


lead_bp = Blueprint("leads", __name__, url_prefix="/leads")


@lead_bp.route("")
@login_required
def listar():
    # 1. Lembra os filtros enviados pela tela para refazer a consulta.
    filters = {
        "status": request.args.get("status", "").strip(),
        "busca": request.args.get("busca", "").strip(),
        "consultor_id": request.args.get("consultor_id", "").strip(),
    }

    # 2. O model aplica permissao: consultor ve so seus leads; admin ve todos.
    leads = LeadModel.list_filtered(g.user, filters, current_app.config["PAGE_SIZE"])
    consultores = UserModel.list_consultores() if g.user["perfil"] == "ADMIN" else []
    return render_template(
        "leads/index.html",
        leads=leads,
        filtros=filters,
        status_lead=STATUS_LEAD,
        consultores=consultores,
    )


@lead_bp.route("/<int:lead_id>")
@login_required
def detalhe(lead_id):
    # 3. Busca o lead completo e valida se o usuario pode abrir a tela.
    lead = LeadModel.find_by_id(lead_id)
    if not LeadService.validar_acesso(lead, g.user):
        flash("Lead nao encontrado ou sem permissao.", "error")
        return redirect(url_for("leads.listar"))

    # 4. Carrega o historico de contatos para exibir junto do detalhe.
    interacoes = InteractionModel.list_by_lead(lead_id)
    return render_template(
        "leads/detail.html",
        lead=lead,
        interacoes=interacoes,
        status_lead=STATUS_LEAD,
        tipos_interacao=TIPOS_INTERACAO,
    )


@lead_bp.route("/<int:lead_id>/status", methods=["POST"])
@login_required
def atualizar_status(lead_id):
    try:
        # 5. Atualiza status e observacoes depois das validacoes do service.
        LeadService.atualizar_status(
            lead_id,
            request.form.get("status", ""),
            request.form.get("observacoes", ""),
            g.user,
        )
        flash("Status atualizado.", "success")
    except Exception as exc:
        flash(str(exc), "error")
    return redirect(url_for("leads.detalhe", lead_id=lead_id))


@lead_bp.route("/<int:lead_id>/remover", methods=["POST"])
@login_required
def remover(lead_id):
    try:
        # 6. Remove o lead respeitando a regra de acesso do usuario atual.
        LeadService.remover(lead_id, g.user)
        flash("Lead removido do funil.", "success")
    except Exception as exc:
        flash(str(exc), "error")
    return redirect(url_for("leads.listar"))


@lead_bp.route("/<int:lead_id>/interacoes", methods=["POST"])
@login_required
def criar_interacao(lead_id):
    # 7. Antes de registrar contato, confirma que o lead pertence ao usuario.
    lead = LeadModel.find_by_id(lead_id)
    if not LeadService.validar_acesso(lead, g.user):
        flash("Sem permissao para registrar interacao.", "error")
        return redirect(url_for("leads.listar"))

    # 8. Grava tipo e descricao da interacao no historico do lead.
    InteractionModel.create(
        lead_id,
        g.user["id"],
        request.form.get("tipo", "OUTRO"),
        request.form.get("descricao", ""),
    )
    flash("Interacao registrada.", "success")
    return redirect(url_for("leads.detalhe", lead_id=lead_id))


@lead_bp.route("/interacoes/<int:interacao_id>/editar", methods=["POST"])
@login_required
def editar_interacao(interacao_id):
    # 9. Busca a interacao para descobrir de qual lead ela faz parte.
    interacao = InteractionModel.find_by_id(interacao_id)
    if not interacao:
        flash("Interacao nao encontrada.", "error")
        return redirect(url_for("leads.listar"))

    # 10. Confirma permissao no lead associado antes de editar a interacao.
    lead = LeadModel.find_by_id(interacao["lead_id"])
    if not LeadService.validar_acesso(lead, g.user):
        flash("Sem permissao para editar interacao.", "error")
        return redirect(url_for("leads.listar"))

    # 11. O model so permite atualizar interacoes feitas nas ultimas 24 horas.
    updated = InteractionModel.update(
        interacao_id,
        request.form.get("tipo", "OUTRO"),
        request.form.get("descricao", ""),
    )
    flash(
        "Interacao editada." if updated else "Edicao permitida apenas em ate 24h.",
        "success" if updated else "error",
    )
    return redirect(url_for("leads.detalhe", lead_id=interacao["lead_id"]))


@lead_bp.route("/interacoes/<int:interacao_id>/excluir", methods=["POST"])
@admin_required
def excluir_interacao(interacao_id):
    # 12. Apenas admin entra aqui; se a interacao existir, remove do banco.
    interacao = InteractionModel.find_by_id(interacao_id)
    if interacao:
        InteractionModel.delete(interacao_id)
        flash("Interacao excluida.", "success")
        return redirect(url_for("leads.detalhe", lead_id=interacao["lead_id"]))

    flash("Interacao nao encontrada.", "error")
    return redirect(url_for("leads.listar"))
