from flask import Flask
from routes.stt_route import stt_bp
from routes.stt_generate_route import stt_gen_bp

app = Flask(__name__)
app.register_blueprint(stt_bp)
app.register_blueprint(stt_gen_bp)

if __name__ == '__main__':
    app.run(debug=True)
