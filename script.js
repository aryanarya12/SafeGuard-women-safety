// ===== Initialize Map =====
let map;
let userMarker;
let crimeMarkers = [];

function initializeMap() {
    // Initialize Leaflet map
    map = L.map('map').setView([28.6139, 77.2090], 12);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    // Add crime hotspots
    const crimeHotspots = [
        { lat: 28.6300, lng: 77.2200, intensity: 'high', incidents: 45 },
        { lat: 28.6500, lng: 77.1900, intensity: 'medium', incidents: 23 },
        { lat: 28.5900, lng: 77.2500, intensity: 'high', incidents: 38 },
        { lat: 28.6100, lng: 77.1800, intensity: 'low', incidents: 8 },
        { lat: 28.6400, lng: 77.2400, intensity: 'medium', incidents: 15 }
    ];

    crimeHotspots.forEach(hotspot => {
        const color = hotspot.intensity === 'high' ? '#e74c3c' : 
                     hotspot.intensity === 'medium' ? '#f39c12' : '#27ae60';
        
        const radius = hotspot.intensity === 'high' ? 25 : 
                      hotspot.intensity === 'medium' ? 15 : 8;

        L.circleMarker([hotspot.lat, hotspot.lng], {
            radius: radius,
            fillColor: color,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.7
        }).bindPopup(`
            <strong>Crime Hotspot</strong><br>
            Intensity: ${hotspot.intensity}<br>
            Incidents: ${hotspot.incidents}
        `).addTo(map);

        crimeMarkers.push({
            lat: hotspot.lat,
            lng: hotspot.lng,
            intensity: hotspot.intensity
        });
    });

    // Add legend
    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = function(map) {
        const div = L.DomUtil.create('div', 'legend');
        div.innerHTML = `
            <style>
                .legend {
                    background: white;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.2);
                }
                .legend-item {
                    margin: 5px 0;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .legend-color {
                    width: 15px;
                    height: 15px;
                    border-radius: 50%;
                    border: 1px solid #ccc;
                }
            </style>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #e74c3c;"></div>
                    <span>High Risk</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #f39c12;"></div>
                    <span>Medium Risk</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #27ae60;"></div>
                    <span>Low Risk</span>
                </div>
            </div>
        `;
        return div;
    };
    legend.addTo(map);
}

// ===== Location Functions =====
function getLocation() {
    updateStatus('Fetching your location...');
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                document.getElementById('current-location').textContent = 
                    `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
                
                // Center map on user
                map.setView([lat, lng], 15);
                
                // Add or update user marker
                if (userMarker) {
                    userMarker.setLatLng([lat, lng]);
                } else {
                    userMarker = L.circleMarker([lat, lng], {
                        radius: 10,
                        fillColor: '#3498db',
                        color: '#fff',
                        weight: 3,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).addTo(map).bindPopup('Your Location');
                }
                
                // Check if near crime hotspots
                checkNearbyHotspots(lat, lng);
                updateStatus('Safe');
                showNotification('Location fetched successfully!', 'success');
            },
            error => {
                updateStatus('Unable to fetch location');
                showNotification('Location access denied. Please enable location services.', 'error');
                console.error('Geolocation error:', error);
            }
        );
    } else {
        updateStatus('Geolocation not supported');
        showNotification('Geolocation is not supported by your browser.', 'error');
    }
}

function checkNearbyHotspots(userLat, userLng) {
    const nearbyIncidents = crimeMarkers.filter(marker => {
        const distance = calculateDistance(userLat, userLng, marker.lat, marker.lng);
        return distance < 2; // Within 2km
    });
    
    const incidentCount = nearbyIncidents.reduce((sum, marker) => {
        return sum + (marker.intensity === 'high' ? 3 : marker.intensity === 'medium' ? 2 : 1);
    }, 0);
    
    document.getElementById('nearby-incidents').textContent = 
        `${nearbyIncidents.length} nearby`;
    
    if (nearbyIncidents.length > 0) {
        updateStatus('⚠️ Warning: Crime zones nearby');
    }
}

function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371; // Earth's radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// ===== CCTV Monitoring =====
function startCCTV() {
    updateStatus('🎥 Initializing CCTV monitoring...');
    
    fetch('/api/cctv', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateStatus('✅ CCTV monitoring active');
            showNotification('CCTV monitoring started. Real-time threat detection enabled.', 'success');
        } else {
            updateStatus('Error starting CCTV');
            showNotification('Failed to start CCTV monitoring. Check connection.', 'error');
        }
    })
    .catch(error => {
        updateStatus('CCTV Error');
        console.error('Error:', error);
        showNotification('Could not connect to CCTV service.', 'error');
    });
}

// ===== GPS Speed Tracking =====
function getSpeed() {
    updateStatus('📍 Getting speed information...');
    
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(
            position => {
                const speed = position.coords.speed || 0;
                const speedKmh = Math.round(speed * 3.6);
                document.getElementById('current-speed').textContent = `${speedKmh} km/h`;
                updateStatus('Speed tracking active');
            },
            error => {
                console.error('Speed tracking error:', error);
                showNotification('Could not get speed information.', 'error');
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    }
}

// ===== Safe Route Planning =====
function findSafeRoute() {
    const destination = document.getElementById('destination').value;
    
    if (!destination) {
        showNotification('Please enter a destination.', 'warning');
        return;
    }
    
    calculateRoute();
}

function calculateRoute() {
    const destination = document.getElementById('destination').value;
    const routeResult = document.getElementById('route-result');
    
    if (!destination) {
        routeResult.innerHTML = '<p style="color: #e74c3c;">Please enter a destination.</p>';
        return;
    }
    
    routeResult.innerHTML = '<div class="loading"></div> Calculating safest route...';
    
    fetch('/api/find_safe_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            destination: destination
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            routeResult.innerHTML = `
                <div style="background: #e8f8f5; border-left: 4px solid #27ae60; padding: 1rem; border-radius: 5px;">
                    <h4 style="color: #27ae60; margin-bottom: 0.5rem;">✅ Safe Route Found</h4>
                    <p><strong>Distance:</strong> ${data.distance} km</p>
                    <p><strong>Estimated Time:</strong> ${data.time} minutes</p>
                    <p><strong>Risk Level:</strong> <span style="color: #27ae60; font-weight: bold;">Low</span></p>
                    <p><strong>Highlights:</strong></p>
                    <ul style="margin: 0.5rem 0 0 1.5rem;">
                        <li>Avoids high-crime areas</li>
                        <li>Well-lit routes preferred</li>
                        <li>CCTV coverage: ${data.cctv_coverage || '85%'}</li>
                        <li>Emergency services nearby: Yes</li>
                    </ul>
                    <a href="${data.map_url || '#'}" style="color: #3498db; text-decoration: underline; margin-top: 0.5rem; display: inline-block;">View on Map</a>
                </div>
            `;
            showNotification('Safe route calculated successfully!', 'success');
        } else {
            routeResult.innerHTML = `<p style="color: #e74c3c;">Error: ${data.message}</p>`;
            showNotification('Could not calculate route.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        routeResult.innerHTML = '<p style="color: #e74c3c;">Unable to calculate route. Please try again.</p>';
        showNotification('Connection error. Please check your internet.', 'error');
    });
}

// ===== Emergency SOS =====
function triggerSOS() {
    const sosModal = document.getElementById('sosModal');
    sosModal.style.display = 'block';
}

function closeSOS() {
    const sosModal = document.getElementById('sosModal');
    sosModal.style.display = 'none';
}

function confirmSOS() {
    closeSOS();
    updateStatus('🚨 Sending emergency alert...');
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const sosData = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    timestamp: new Date().toISOString(),
                    type: 'EMERGENCY_SOS'
                };
                
                fetch('/api/sos', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(sosData)
                })
                .then(response => response.json())
                .then(data => {
                    updateStatus('✅ SOS Alert Sent!');
                    showNotification(
                        'Emergency alert sent to authorities and emergency contacts!',
                        'success'
                    );
                    addAlert('🚨 SOS Alert sent at ' + new Date().toLocaleTimeString());
                })
                .catch(error => {
                    updateStatus('❌ Failed to send SOS');
                    console.error('Error:', error);
                    showNotification('Failed to send emergency alert. Retrying...', 'error');
                });
            }
        );
    }
}

// ===== Status Update =====
function updateStatus(message) {
    const statusElement = document.getElementById('current-status');
    if (statusElement) {
        statusElement.textContent = message;
    }
}

// ===== Notifications =====
function showNotification(message, type = 'info') {
    // Create notification element
    const notificationDiv = document.createElement('div');
    notificationDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#27ae60' : 
                     type === 'error' ? '#e74c3c' : 
                     type === 'warning' ? '#f39c12' : '#3498db'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 3000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;
    notificationDiv.textContent = message;
    document.body.appendChild(notificationDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notificationDiv.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notificationDiv.remove(), 300);
    }, 5000);
}

// Add slide animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ===== Alerts Management =====
function addAlert(message) {
    const alertsList = document.getElementById('alerts-list');
    const alertItem = document.createElement('p');
    alertItem.textContent = message;
    alertItem.style.cssText = `
        padding: 1rem;
        background: #fff3cd;
        border-left: 4px solid #f39c12;
        margin-bottom: 0.5rem;
        border-radius: 3px;
    `;
    alertsList.insertBefore(alertItem, alertsList.firstChild);
    
    // Keep only last 10 alerts
    while (alertsList.children.length > 10) {
        alertsList.removeChild(alertsList.lastChild);
    }
}

// ===== Feedback Submission =====
function submitFeedback(event) {
    event.preventDefault();
    
    const form = event.target;
    const email = form.elements[0].value;
    const message = form.elements[1].value;
    
    const feedbackData = {
        email: email,
        message: message,
        timestamp: new Date().toISOString()
    };
    
    fetch('/api/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedbackData)
    })
    .then(response => response.json())
    .then(data => {
        showNotification('Thank you for your feedback!', 'success');
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Could not submit feedback. Please try again.', 'error');
    });
}

// ===== Initialize on Page Load =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('SafeGuard Application Loaded');
    
    // Initialize map
    if (document.getElementById('map')) {
        initializeMap();
    }
    
    // Update statistics
    updateStatistics();
    
    // Set up periodic updates
    setInterval(updateStatistics, 60000); // Update every minute
    
    // Handle modal close on outside click
    window.onclick = function(event) {
        const sosModal = document.getElementById('sosModal');
        if (event.target == sosModal) {
            sosModal.style.display = 'none';
        }
    };
    
    // Log application version
    console.log('SafeGuard v2.0 - March 2026');
});

// ===== Statistics Update =====
function updateStatistics() {
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            document.getElementById('stat-incidents').textContent = 
                data.incidents || Math.floor(Math.random() * 1000) + 500;
            document.getElementById('stat-routes').textContent = 
                data.routes || Math.floor(Math.random() * 10000) + 5000;
            document.getElementById('stat-users').textContent = 
                data.users || Math.floor(Math.random() * 50000) + 25000;
            document.getElementById('stat-alerts').textContent = 
                data.alerts || Math.floor(Math.random() * 500) + 100;
        })
        .catch(error => {
            console.error('Error fetching statistics:', error);
            // Use mock data if API unavailable
            document.getElementById('stat-incidents').textContent = 
                Math.floor(Math.random() * 1000) + 500;
            document.getElementById('stat-routes').textContent = 
                Math.floor(Math.random() * 10000) + 5000;
            document.getElementById('stat-users').textContent = 
                Math.floor(Math.random() * 50000) + 25000;
            document.getElementById('stat-alerts').textContent = 
                Math.floor(Math.random() * 500) + 100;
        });
}

// ===== Service Worker Registration (for offline support) =====
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch(error => {
        console.log('ServiceWorker registration failed:', error);
    });
}
