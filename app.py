from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/receipt')
def receipt():
    return render_template('receipt.html')

if __name__ == '__main__':
    app.run(debug=True)
