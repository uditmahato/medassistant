from flask import Flask
from src.api.routes import register_routes
from src.utils.logger import logger
import sys

def create_app():
    app = Flask(__name__, template_folder="../templates")
    register_routes(app)
    logger.info("Flask application created successfully")
    return app

if __name__ == "__main__":
    import os
    app = create_app()
    env = os.getenv("FLASK_ENV", "development")
    host = "127.0.0.1" if env == "production" else "0.0.0.0"
    port = 5000
    debug = env != "production"

    print(f"\nStarting Flask server in {env} mode...")
    print(f"Attempting to run on http://{host}:{port}")
    print("Press CTRL+C to stop the server.\n")

    try:
        app.run(host=host, port=port, debug=debug)
    except OSError as e:
        logger.error(f"Failed to start server: {e}")
        print(f"\nERROR: Could not start server on port {port}: {e}", file=sys.stderr)
        print("Check if another application is using this port.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during server startup: {e}")
        print(f"\nERROR: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)