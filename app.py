from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO
import requests
from bs4 import BeautifulSoup
import random
import json

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

# Language data
languages = {
    'pt': {
        'mercury': {
            'name': 'Mercúrio',
            'type': 'Planeta terrestre',
            'distance': '57,9 milhões de quilômetros',
            'diameter': '4.879 km',
            'day_length': '176 dias terrestres',
            'year_length': '88 dias terrestres',
            'description': 'O menor e mais interno planeta do Sistema Solar'
        },
        'venus': {
            'name': 'Vênus',
            'type': 'Planeta terrestre',
            'distance': '108,2 milhões de quilômetros',
            'diameter': '12.104 km',
            'day_length': '243 dias terrestres',
            'year_length': '225 dias terrestres',
            'description': 'Às vezes chamado de planeta irmão da Terra devido ao tamanho semelhante'
        },
        'earth': {
            'name': 'Terra',
            'type': 'Planeta terrestre',
            'distance': '149,6 milhões de quilômetros',
            'diameter': '12.742 km',
            'day_length': '24 horas',
            'year_length': '365,25 dias',
            'description': 'Nosso planeta natal e o único planeta conhecido com vida'
        },
        'mars': {
            'name': 'Marte',
            'type': 'Planeta terrestre',
            'distance': '227,9 milhões de quilômetros',
            'diameter': '6.779 km',
            'day_length': '24 horas e 37 minutos',
            'year_length': '687 dias terrestres',
            'description': 'Conhecido como o Planeta Vermelho devido à sua aparência avermelhada'
        },
        'jupiter': {
            'name': 'Júpiter',
            'type': 'Gigante gasoso',
            'distance': '778,5 milhões de quilômetros',
            'diameter': '139.820 km',
            'day_length': '10 horas',
            'year_length': '12 anos terrestres',
            'description': 'O maior planeta em nosso Sistema Solar'
        },
        'saturn': {
            'name': 'Saturno',
            'type': 'Gigante gasoso',
            'distance': '1,4 bilhão de quilômetros',
            'diameter': '116.460 km',
            'day_length': '10,7 horas',
            'year_length': '29,5 anos terrestres',
            'description': 'Famoso por seu sistema de anéis proeminente'
        },
        'uranus': {
            'name': 'Urano',
            'type': 'Gigante de gelo',
            'distance': '2,9 bilhões de quilômetros',
            'diameter': '50.724 km',
            'day_length': '17 horas',
            'year_length': '84 anos terrestres',
            'description': 'A atmosfera planetária mais fria no Sistema Solar'
        },
        'neptune': {
            'name': 'Netuno',
            'type': 'Gigante de gelo',
            'distance': '4,5 bilhões de quilômetros',
            'diameter': '49.244 km',
            'day_length': '16 horas',
            'year_length': '165 anos terrestres',
            'description': 'O planeta mais ventoso, com velocidades alcançando 2.100 km/h'
        }
    },
    'en': planets  # Original English data
}

current_language = 'en'

@app.route('/change_language/<lang>')
def change_language(lang):
    global current_language
    if lang in ['en', 'pt']:
        current_language = lang
        return jsonify({'status': 'success', 'language': lang})
    return jsonify({'status': 'error', 'message': 'Invalid language'})

def get_random_planet_images(planet_name, count=5):
    search_url = f"https://www.google.com/search?q={planet_name}+planet&tbm=isch"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = []
    for img in img_tags[1:]:  # Skip first image as it's usually a logo
        if 'src' in img.attrs and len(img_urls) < count:
            img_urls.append(img['src'])
    return img_urls

@app.route('/adentrar/<planet_name>')
def adentrar_planeta(planet_name):
    try:
        planet_data = languages[current_language].get(planet_name.lower())
        if not planet_data:
            return jsonify({'error': 'Planet not found'}), 404
        
        images = get_random_planet_images(planet_name)
        response_data = {
            'planet_info': planet_data,
            'images': images
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/planets', methods=['GET'])
def get_all_planets():
    return jsonify(languages[current_language])

@app.route('/api/planets/<planet_name>', methods=['GET'])
def get_planet(planet_name):
    planet = languages[current_language].get(planet_name.lower())
    if planet:
        # Emit a socket event to all connected clients
        socketio.emit('focus_planet', {'planet': planet_name.lower()})
        return jsonify(planet)
    return jsonify({'error': 'Planet not found'}), 404

if __name__ == '__main__':
    socketio.run(app, debug=True)
