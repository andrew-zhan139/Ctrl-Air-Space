from flask import Flask
from hello import run
app = Flask(__name__)


@app.route('/hello')
def hello():
    run()
    return "Hello World!"

if __name__ == '__main__':
    app.run()