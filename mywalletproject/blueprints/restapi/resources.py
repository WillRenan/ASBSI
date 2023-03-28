from flask import jsonify, abort
from flask_restful import Resource
from mywalletproject.ext.database import  Acoes, User, FundosImobiliarios

class UserResource(Resource):
    def get(self):
        user = User.query.all() or abort(204)
        return jsonify(
            {'puser':[ 
                {
                    'id':user.id,
                    'name':user.name,
                    'email':user.email
                }
                for user in user
            ]}
        )

class UserItemResource(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=id).first() or abort(
            404
        )
        
        return jsonify(user.to_dict())