from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init flask navigating class for our app

app=Flask(__name__)

#configuring our app so that server can know about database and all

#Creating Base dir for db URI

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQL_TRACK_MODIFICATIONS']=False

#INIT db

db=SQLAlchemy(app)

#init marshmallow

ma=Marshmallow(app)

#We have to make class for representing each table

class Product(db.Model):
    id1 = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__ (self,name,description,price,qty):
        self.name=name
        self.description=description
        self.price=price
        self.qty=qty

# Creating Schema For Fetching and Inserting

class ProductSchema1(ma.Schema):
    class Meta:
        fields=('id1','name','description','price','qty')

#creating two instances one for handling single and another for multiple

product_schema=ProductSchema1()
products_schema=ProductSchema1(many=True)

# Create Route to add data

@app.route('/add_product',methods=['POST'])
def add_product():
    name=request.json['name']
    description=request.json['description']
    price=request.json['price']
    qty=request.json['qty']

    # Creating New Product

    new_Product=Product(name,description,price,qty)

    # Adding product to DB

    db.session.add(new_Product)
    db.session.commit()

    return product_schema.jsonify(new_Product)

# Get All Products

@app.route('/product',methods=['GET'])
def get_all_products():
    all_products=Product.query.all()
    return products_schema.jsonify(all_products)

#Get Single Product

@app.route('/product/<int:id>',methods=['GET'])
def get_product(id):
    product=Product.query.get(id)
    return product_schema.jsonify(product)

# Update Product

@app.route('/update_product/<int:id>',methods=['PUT'])
def update_Product(id):

    # Fetching that Product

    product=Product.query.get(id)

    if product :

        # Getting Values after Update

        name=request.json['name']
        description=request.json['description']
        price=request.json['price']
        qty=request.json['qty']

        #Changing Value Of Product

        product.name=name
        product.description=description
        product.price=price
        product.qty=qty

        #Commiting change to DB

        db.session.commit()

        return product_schema.jsonify(product)

#Delete Product

@app.route('/delete_product/<int:id>',methods=['DELETE'])
def delete_product(id):

    # Fetching Product to be deleted

    product=Product.query.get(id)

    # Deleteing 
    if product:
        db.session.delete(product)
        db.session.commit()

        # Returning Remaining Product

        all_products=Product.query.all()
        return products_schema.jsonify(all_products)



#Run Server

if(__name__=="__main__"):
    app.run(debug=True)