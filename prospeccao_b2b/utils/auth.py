from functools import wraps

from flask import abort, flash, g, redirect, request, url_for


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.user:
            flash("Faca login para acessar o sistema.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.user:
            flash("Faca login para acessar o sistema.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        if g.user["perfil"] != "ADMIN":
            abort(403)
        return view(*args, **kwargs)

    return wrapped
