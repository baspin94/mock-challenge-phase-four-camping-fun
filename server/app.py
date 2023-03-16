from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource


from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Campers(Resource):
    
    def get(self):
        campers = [camper.to_dict() for camper in Camper.query.all()]

        response = make_response(
            jsonify(campers),
            200
        )

        return response
    
    def post(self):
        new_camper = Camper(
            name = request.get_json()['name'],
            age = request.get_json()['age']
        )
        db.session.add(new_camper)
        db.session.commit()

        response = make_response(
            new_camper.to_dict(),
            201
        )

        return response

api.add_resource(Campers, '/campers')

class CampersById(Resource):

    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).first().to_dict()

        response = make_response(
            camper,
            200
        )
        return response
        

api.add_resource(CampersById, "/campers/<int:id>")




class Activities(Resource):
    def get(self):
        activities = [activity.to_dict() for activity in Activity.query.all()]
        response = make_response(
            activities,
            200
        )
        return response
    
    
api.add_resource(Activities, "/activities")




if __name__ == '__main__':
    app.run(port=5555, debug=True)
