"""Ponto de entrada da aplicacao Flask."""

from app_factory import create_app


# 1. Cria a aplicacao usando a fabrica centralizada.
app = create_app()


if __name__ == "__main__":
    # 2. Quando o arquivo e executado diretamente, inicia o servidor local.
    app.run(debug=True)
