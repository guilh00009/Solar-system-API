from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Planet data
planets_data = {
    "mercury": {
        "name": "Mercury",
        "type": "Terrestrial planet",
        "distance": "57.9 million kilometers",
        "diameter": "4,879 km",
        "day_length": "58.6 Earth days",
        "year_length": "88 Earth days",
        "description": "The smallest and innermost planet in the Solar System."
    },
    "venus": {
        "name": "Venus",
        "type": "Terrestrial planet",
        "distance": "108.2 million kilometers",
        "diameter": "12,104 km",
        "day_length": "243 Earth days",
        "year_length": "225 Earth days",
        "description": "Often called Earth's sister planet due to similar size."
    },
    "earth": {
        "name": "Earth",
        "type": "Terrestrial planet",
        "distance": "149.6 million kilometers",
        "diameter": "12,742 km",
        "day_length": "24 hours",
        "year_length": "365.25 days",
        "description": "Our home planet and the only known planet with life."
    },
    "mars": {
        "name": "Mars",
        "type": "Terrestrial planet",
        "distance": "227.9 million kilometers",
        "diameter": "6,779 km",
        "day_length": "24.6 hours",
        "year_length": "687 Earth days",
        "description": "Known as the Red Planet due to its reddish appearance."
    },
    "jupiter": {
        "name": "Jupiter",
        "type": "Gas giant",
        "distance": "778.5 million kilometers",
        "diameter": "139,820 km",
        "day_length": "9.9 hours",
        "year_length": "11.9 Earth years",
        "description": "The largest planet in our Solar System."
    },
    "saturn": {
        "name": "Saturn",
        "type": "Gas giant",
        "distance": "1.4 billion kilometers",
        "diameter": "116,460 km",
        "day_length": "10.7 hours",
        "year_length": "29.5 Earth years",
        "description": "Famous for its prominent ring system."
    },
    "uranus": {
        "name": "Uranus",
        "type": "Ice giant",
        "distance": "2.9 billion kilometers",
        "diameter": "50,724 km",
        "day_length": "17.2 hours",
        "year_length": "84 Earth years",
        "description": "Rotates on its side with extreme seasonal variations."
    },
    "neptune": {
        "name": "Neptune",
        "type": "Ice giant",
        "distance": "4.5 billion kilometers",
        "diameter": "49,244 km",
        "day_length": "16.1 hours",
        "year_length": "164.8 Earth years",
        "description": "The windiest planet with the strongest storms."
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/planets/<planet_name>')
def get_planet(planet_name):
    planet_name = planet_name.lower()
    if planet_name in planets_data:
        # Emit socket event for real-time updates
        socketio.emit('focus_planet', {'planet': planet_name})
        
        # Return in Vapi format
        return jsonify({
            "results": [
                {
                    "toolCallId": f"planet_info_{planet_name}",
                    "result": planets_data[planet_name]
                }
            ]
        })
    else:
        return jsonify({
            "results": [
                {
                    "toolCallId": "error",
                    "result": "Planet not found"
                }
            ]
        }), 404

@app.route('/api/planets')
def list_planets():
    return jsonify({
        "results": [
            {
                "toolCallId": "list_planets",
                "result": list(planets_data.keys())
            }
        ]
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)
