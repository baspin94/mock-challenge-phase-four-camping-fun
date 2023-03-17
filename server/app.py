from flask import Flask, request, make_response, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound


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

        try:
            new_camper = Camper(
                name = request.get_json()['name'],
                age = request.get_json()['age']
            )

        except ValueError as e:
            abort(422, e.args[0])
            

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
        camper = Camper.query.filter(Camper.id == id).first()

        if not camper:
            abort(404, description="Camper not found.")

        response = make_response(
            camper.to_dict(),
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

class ActivityById(Resource):
    
    def get(self, id):

        activity = Activity.query.filter(Activity.id == id).first().to_dict()

        response = make_response(
            activity,
            200
        )

        return response

    def delete(self, id):

        activity = Activity.query.filter(Activity.id == id).first()

        db.session.delete(activity)
        db.session.commit()

        response_body = ""

        response = make_response(
            response_body,
            200
        )

        return response

        

api.add_resource(ActivityById, '/activities/<int:id>')




class Signups(Resource):
    
    def get(self):
        signups = [signup.to_dict() for signup in Signup.query.all()]

        response = make_response(
            signups,
            200
        )
        return response


    
    def post(self):
        data = request.get_json()

        try:
            new_signup = Signup(
                time = data["time"],
                camper_id = data["camper_id"],
                activity_id = data["activity_id"]
            )
        
        except ValueError as e:
            abort(422, e.args[0])

        db.session.add(new_signup)
        db.session.commit()

        response_body = {
            "id": new_signup.activity.id,
            "name": new_signup.activity.name,
            "difficulty": new_signup.activity.difficulty
        }

        response = make_response(
            response_body,
            201
        )
        return response
    


api.add_resource(Signups, "/signups")

@app.errorhandler(404)
def handle_not_found(e):
    response = jsonify(error=str(e)), 404
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
