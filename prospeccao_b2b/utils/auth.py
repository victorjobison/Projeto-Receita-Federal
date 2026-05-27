"""Decoradores que protegem rotas por login e perfil."""

from functools import wraps

from flask import abort, flash, g, redirect, request, url_for


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        # 1. Se nao houver usuario carregado em g.user, manda para o login.
        if not g.user:
            flash("Faca login para acessar o sistema.", "warning")
            return redirect(url_for("auth.login", next=request.path))

        # 2. Usuario autenticado segue para a rota original.
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        # 3. Primeiro exige login, igual ao decorator login_required.
        if not g.user:
            flash("Faca login para acessar o sistema.", "warning")
            return redirect(url_for("auth.login", next=request.path))

        # 4. Depois exige perfil ADMIN; caso contrario retorna HTTP 403.
        if g.user["perfil"] != "ADMIN":
            abort(403)

        # 5. Admin autenticado segue para a rota protegida.
        return view(*args, **kwargs)

    return wrapped
