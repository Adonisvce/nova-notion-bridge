from flask import Flask
from core.bootstrap import bootstrap

app = Flask(__name__)
bootstrap(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
