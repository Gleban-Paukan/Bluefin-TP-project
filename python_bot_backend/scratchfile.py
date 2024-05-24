from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
