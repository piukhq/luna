from app import create_app

app = create_app()

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    from app.settings import DEBUG, LUNA_PORT

    run_simple(
        hostname="localhost",
        port=LUNA_PORT,
        application=app,
        use_reloader=DEBUG,
        use_debugger=DEBUG,
    )
