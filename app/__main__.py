from app import create_app

from app.server import app

if __name__ == '__main__':
    create_app()
    app.run(debug=True)

