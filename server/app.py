#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response, abort
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, UnprocessableEntity

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):

        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):

    def find_plant ( self, id ) :
        plant = Plant.query.filter_by(id=id).first()
        if plant :
            return plant
        else : abort( 404, 'Could not find plant.' )

    def get(self, id):
        plant = self.find_plant( id ).to_dict()
        return make_response( jsonify( plant ) , 200 )
    
    def patch( self, id ) :
        plant = self.find_plant( id )
        updates = request.get_json()
        for key in updates :
            setattr( plant, key, updates[ key ] )
        
        db.session.add( plant )
        db.session.commit()
        return make_response( jsonify( plant.to_dict() ), 200 )
        

api.add_resource(PlantByID, '/plants/<int:id>')

@app.errorhandler( NotFound )
def handle_not_found ( e ) :
    return make_response( 'Resource could not be located. Check the url and try again.', 404 )



if __name__ == '__main__':
    app.run(port=5555, debug=True)
