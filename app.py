
import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hola'


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")), debug=True)
