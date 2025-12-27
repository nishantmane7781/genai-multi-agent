from flask import Flask
from src.api.routes import bp
from src.config.settings import HOST, PORT

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        debug=False,       
        use_reloader=False 
    )
