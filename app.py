from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from currency_converter import CurrencyConverter
c = CurrencyConverter()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hvhfbhfhbdhf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xstore.db'
db = SQLAlchemy(app)
CORS(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Float, nullable=False)
  image = db.Column(db.String(100), nullable=False)
  shortcode = db.Column(db.String(100), nullable=False)

  def __repr__(self):
    return '<Product %r>' % self.id
  
class Contactform(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  message = db.Column(db.String(100), nullable=False)

  def __repr__(self):
    return '<Contactform %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def start():
  return render_template('index.html')

@app.route('/buy/<shortcode>', methods=['GET', 'POST'])
def buy(shortcode):
  product = Product.query.filter_by(shortcode=shortcode).first()
  inr_price = int(c.convert(product.price, 'USD', 'INR'))
  return render_template('buy.html', product=product, inr_price=inr_price)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  return render_template('contact.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
  return render_template('about.html')

@app.route('/submitform', methods=['POST'])
def submitform():
  name = request.form['name']
  email = request.form['email']
  message = request.form['message']
  contactform = Contactform(name=name, email=email, message=message)
  db.session.add(contactform)
  db.session.commit()
  message='Your message has been sent successfully'
  return render_template('contact.html', message=message)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)