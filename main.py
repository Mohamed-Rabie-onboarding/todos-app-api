import os
from app.serve import load_env_if_dev, serve

if __name__ == "__main__":
    development = load_env_if_dev()

    app = serve()
    app.run(
        debug=development,
        port=int(os.getenv('PORT')),
        reloader=development,
    )
