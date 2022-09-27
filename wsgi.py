from werkzeug.serving import run_simple

from luna import create_app
from luna.settings import DEBUG, LUNA_PORT

app = create_app()

if __name__ == "__main__":
    run_simple(
        hostname="localhost",
        port=LUNA_PORT,
        application=app,
        use_reloader=DEBUG,
        use_debugger=DEBUG,
    )
