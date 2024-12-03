from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Planet data
planets = {
    'mercury': {
        'name': 'Mercury',
        'type': 'Terrestrial planet',
        'distance': '57.9 million kilometers',
        'diameter': '4,879 km',
        'day_length': '176 Earth days',
        'year_length': '88 Earth days',
        'description': 'The smallest and innermost planet in the Solar System'
    },
    'venus': {
        'name': 'Venus',
        'type': 'Terrestrial planet',
        'distance': '108.2 million kilometers',
        'diameter': '12,104 km',
        'day_length': '243 Earth days',
        'year_length': '225 Earth days',
        'description': 'Often called Earth\'s sister planet due to similar size'
    },
    'earth': {
        'name': 'Earth',
        'type': 'Terrestrial planet',
        'distance': '149.6 million kilometers',
        'diameter': '12,742 km',
        'day_length': '24 hours',
        'year_length': '365.25 days',
        'description': 'Our home planet and the only known planet with life'
    },
    'mars': {
        'name': 'Mars',
        'type': 'Terrestrial planet',
        'distance': '227.9 million kilometers',
        'diameter': '6,779 km',
        'day_length': '24 hours 37 minutes',
        'year_length': '687 Earth days',
        'description': 'Known as the Red Planet due to its reddish appearance'
    },
    'jupiter': {
        'name': 'Jupiter',
        'type': 'Gas giant',
        'distance': '778.5 million kilometers',
        'diameter': '139,820 km',
        'day_length': '10 hours',
        'year_length': '12 Earth years',
        'description': 'The largest planet in our Solar System'
    },
    'saturn': {
        'name': 'Saturn',
        'type': 'Gas giant',
        'distance': '1.4 billion kilometers',
        'diameter': '116,460 km',
        'day_length': '10.7 hours',
        'year_length': '29.5 Earth years',
        'description': 'Famous for its prominent ring system'
    },
    'uranus': {
        'name': 'Uranus',
        'type': 'Ice giant',
        'distance': '2.9 billion kilometers',
        'diameter': '50,724 km',
        'day_length': '17 hours',
        'year_length': '84 Earth years',
        'description': 'The coldest planetary atmosphere in the Solar System'
    },
    'neptune': {
        'name': 'Neptune',
        'type': 'Ice giant',
        'distance': '4.5 billion kilometers',
        'diameter': '49,244 km',
        'day_length': '16 hours',
        'year_length': '165 Earth years',
        'description': 'The windiest planet, with speeds reaching 2,100 km/h'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/planets', methods=['GET'])
def get_all_planets():
    return jsonify(planets)

@app.route('/api/planets/<planet_name>', methods=['GET'])
def get_planet(planet_name):
    planet = planets.get(planet_name.lower())
    if planet:
        # Emit a socket event to all connected clients
        socketio.emit('focus_planet', {'planet': planet_name.lower()})
        return jsonify(planet)
    return jsonify({'error': 'Planet not found'}), 404

if __name__ == '__main__':
    socketio.run(app, debug=True)
