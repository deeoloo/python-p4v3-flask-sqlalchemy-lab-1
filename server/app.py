# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get_or_404(id)
    return jsonify({
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year
    })


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    quakes = [{
        "id": eq.id,
        "magnitude": eq.magnitude,
        "location": eq.location,
        "year": eq.year
    } for eq in earthquakes]
    
    return jsonify({
        "count": count,
        "quakes": quakes
    })

@app.errorhandler(404)
def not_found(error):
    earthquake_id = request.view_args.get('id') if request.view_args else None
    if earthquake_id is not None:
        return jsonify({"message": f"Earthquake {earthquake_id} not found."}), 404
    return jsonify({"message": "Resource not found."}), 404
# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
