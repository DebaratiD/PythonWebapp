from dataclasses import dataclass
from flask import Flask, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from producer import publish
from sqlalchemy import UniqueConstraint
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image:str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    # this product is  different from the Product in main app since there is no Likes here
    # Also, the id is different 

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/api/products')
def index():
    #return 'Hello'
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    # use docker.for.mac.localhost to tell the app to use internal http call,
    # not an external one
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        productUser = ProductUser(user_id = json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        #event
        # - copy the producer file from admin and paste it in main
        publish('product_liked', id)
    except:
        # throw error incase user tries to like again, since user is a unique constraint
        abort(400, 'You already liked this product')

    return jsonify({
        'message':'success'
    })

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0') 