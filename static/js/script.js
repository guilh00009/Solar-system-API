document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const planets = document.querySelectorAll('.planet');
    const planetInfo = document.getElementById('planetInfo');
    const closeBtn = document.querySelector('.close-btn');
    const solarSystem = document.querySelector('.solar-system');
    
    // Planet info elements
    const planetNameEl = document.getElementById('planetName');
    const planetTypeEl = document.getElementById('planetType');
    const planetDistanceEl = document.getElementById('planetDistance');
    const planetDiameterEl = document.getElementById('planetDiameter');
    const planetDayEl = document.getElementById('planetDay');
    const planetYearEl = document.getElementById('planetYear');
    const planetDescriptionEl = document.getElementById('planetDescription');

    let currentPlanet = null;
    let isTransitioning = false;
    let lastFocusTime = 0;
    const TRANSITION_COOLDOWN = 1000; // 1 second cooldown

    // Socket event listener for real-time updates
    socket.on('focus_planet', (data) => {
        const now = Date.now();
        if (now - lastFocusTime < TRANSITION_COOLDOWN) {
            return; // Ignore rapid consecutive calls
        }
        
        if (!isTransitioning && (!currentPlanet || currentPlanet.getAttribute('data-planet') !== data.planet)) {
            focusOnPlanet(data.planet);
        }
    });

    async function focusOnPlanet(planetName) {
        if (isTransitioning) return;
        
        const planet = document.querySelector(`.${planetName}`);
        if (!planet) return;

        isTransitioning = true;
        lastFocusTime = Date.now();

        // Clear any existing zoom
        resetZoom();
        
        // Add zoom class to solar system
        solarSystem.classList.add('zoomed');
        
        // Add focus class to the planet
        planet.classList.add('focused');
        currentPlanet = planet;
        
        // Fetch and display planet data
        const data = await fetchPlanetInfo(planetName);
        if (data) {
            showPlanetInfo(data);
        }

        // Reset transition flag after animation completes
        setTimeout(() => {
            isTransitioning = false;
        }, 1000); // Match this with CSS transition duration
    }

    function resetZoom() {
        if (currentPlanet) {
            currentPlanet.classList.remove('focused');
        }
        solarSystem.classList.remove('zoomed');
        planetInfo.classList.remove('active');
        currentPlanet = null;
    }

    async function fetchPlanetInfo(planetName) {
        try {
            const response = await fetch(`/api/planets/${planetName}`);
            const data = await response.json();
            // Extract the result from the Vapi format response
            if (data.results && data.results[0] && data.results[0].result) {
                return data.results[0].result;
            }
            return null;
        } catch (error) {
            console.error('Error fetching planet data:', error);
            return null;
        }
    }

    function showPlanetInfo(data) {
        planetNameEl.textContent = data.name;
        planetTypeEl.textContent = data.type;
        planetDistanceEl.textContent = data.distance;
        planetDiameterEl.textContent = data.diameter;
        planetDayEl.textContent = data.day_length;
        planetYearEl.textContent = data.year_length;
        planetDescriptionEl.textContent = data.description;
        
        planetInfo.classList.add('active');
    }

    // Event Listeners
    planets.forEach(planet => {
        planet.addEventListener('click', () => {
            const planetName = planet.getAttribute('data-planet');
            if (!isTransitioning) {
                focusOnPlanet(planetName);
            }
        });
    });

    closeBtn.addEventListener('click', () => {
        if (!isTransitioning) {
            resetZoom();
        }
    });

    // Listen for API calls
    async function checkForApiCalls() {
        const urlParams = new URLSearchParams(window.location.search);
        const focusPlanet = urlParams.get('focus');
        if (focusPlanet) {
            await focusOnPlanet(focusPlanet);
            // Clear the URL parameter
            window.history.replaceState({}, '', window.location.pathname);
        }
    }

    // Check for API calls on page load
    checkForApiCalls();
});
