from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for

from models.lead_model import STATUS_LEAD
from services.company_service import CompanyService
from services.lead_service import LeadService
from utils.auth import login_required


company_bp = Blueprint("companies", __name__)


@company_bp.route("/")
@login_required
def dashboard():
    filters = {
        "cnae": request.args.get("cnae", "").strip(),
        "capital_min": request.args.get("capital_min", "").strip(),
        "porte": request.args.get("porte", "").strip(),
        "uf": request.args.get("uf", "").strip(),
        "municipio": request.args.get("municipio", "").strip(),
        "situacao": request.args.get("situacao", "ATIVA").strip(),
        "busca": request.args.get("busca", "").strip(),
    }
    empresas = CompanyService.listar_empresas(
        filters,
        g.user["id"],
        current_app.config["PAGE_SIZE"],
    )
    return render_template(
        "index.html",
        empresas=empresas,
        filtros=filters,
        status_lead=STATUS_LEAD,
    )


@company_bp.route("/empresas/consultar", methods=["POST"])
@login_required
def consultar_cnpj():
    try:
        empresa = CompanyService.consultar_cnpj(request.form.get("cnpj", ""))
        flash(f"Empresa {empresa['razao_social']} salva no catalogo.", "success")
    except Exception as exc:
        flash(str(exc), "error")
    return redirect(url_for("companies.dashboard"))


@company_bp.route("/leads/criar", methods=["POST"])
@login_required
def criar_lead():
    try:
        LeadService.criar_lead(
            request.form.get("cnpj", ""),
            g.user["id"],
            request.form.get("observacoes", ""),
        )
        flash("Lead adicionado ao funil.", "success")
    except Exception as exc:
        flash(str(exc), "error")
    return redirect(request.referrer or url_for("companies.dashboard"))


@company_bp.route("/privacidade")
def privacidade():
    return render_template("privacy.html")
