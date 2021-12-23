from .models import Product
from app import db
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from app.api_restfull import api_restfull_bp
from flask import jsonify, request, make_response
import datetime


api = Api(api_restfull_bp)
resource_fields = {
    'id' : fields.Integer,
    'codeOfProduct': fields.Integer,
    'name' : fields.String,
    'typeOfProduct': fields.String,
    'is_product' : fields.Boolean,
    'count' : fields.Integer,
    'price' : fields.Integer,
    'description' : fields.String,
}

product_create = reqparse.RequestParser()
product_create.add_argument('codeOfProduct', type=int, help='code is required!', required=True)
product_create.add_argument('name', type=str, help='name is required!', required=True)
product_create.add_argument('typeOfProduct', type=str, help='typeOfProduct is required!', required=True)
product_create.add_argument('is_product', type=str, help='is_product is required!', required=True)
product_create.add_argument('count', type=int, help='count is required!', required=True)
product_create.add_argument('price', type=int, help='price is required!', required=True)
product_create.add_argument('description', type=str, help='description is required!', required=True)


product_update = reqparse.RequestParser()
product_update.add_argument('codeOfProduct', type=int, help='code is required!', required=True)
product_update.add_argument('name', type=str, help='name is required!', required=True)
product_update.add_argument('typeOfProduct', type=str, help='typeOfProduct is required!', required=True)
product_update.add_argument('is_product', type=str, help='is_product is required!', required=True)
product_update.add_argument('count', type=int, help='count is required!', required=True)
product_update.add_argument('price', type=int, help='price is required!', required=True)
product_update.add_argument('description', type=str, help='description is required!', required=True)


class ProductItem(Resource):

    def post(self):
        args = product_create.parse_args()
        try:
            product = Product(codeOfProduct=args['codeOfProduct'], name=args['name'], typeOfProduct=args['typeOfProduct'],
             is_product=bool(args['is_product']), count=args['count'], price=args['price'], description=args['description'])
           
            db.session.add(product)
            db.session.commit()
            # return jsonify({'message': 'Data add in db!'}), 201 777   ?????
            return make_response(jsonify({'message': 'Data add in db!'}))
        except:
            db.session.rollback()
            # return jsonify({'message': 'Error when adding data!'}) ?????
            return make_response(jsonify({'message': 'Error when adding data!'}), 201)



    @marshal_with(resource_fields, envelope='resource')
    def get(self, id=None):
        if id is None:
            product_all = Product.query.all()
            return product_all
        else:
            product = Product.query.filter_by(id=id).first()
            if not product:
                return make_response(jsonify({'message': 'Product not found!'}))
            return product

    # @marshal_with(resource_fields, envelope='resource')
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            return make_response(jsonify({'message': 'Product not found!'}), 404)
        db.session.delete(product)
        db.session.commit()
        return  make_response(jsonify({'message': 'The task has been deleted'}))

    # @marshal_with(resource_fields, envelope='resource')
    def put(self, id):
        product = Product.query.filter_by(id=id).first()
        print(product)
        if not product:
            return make_response(jsonify({'message': 'Product not found!'}), 404)
        args = product_update.parse_args()
        
        product.codeOfProduct = args['codeOfProduct']
        product.name = args['name']
        product.typeOfProduct = args['typeOfProduct']
        if args['is_product']=='True':
            product.is_product = True
        elif args['is_product']=='False':
            product.is_product = False
        product.count = args['count']
        product.price = args['price']
        product.description = args['description']
        try:
            db.session.commit()
            return make_response(jsonify({"message": "Product succesfully update!"}))
        except:
            db.session.rollback()
            return make_response(jsonify({'message': 'Error when updating data!'}), 201)


api.add_resource(ProductItem, '/product', '/product/<int:id>')
