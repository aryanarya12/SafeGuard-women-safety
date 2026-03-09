# Women Safety Application

A comprehensive women safety system that combines crime mapping, facial recognition, safe route planning, and emergency SOS features to enhance women's security in urban areas.

## 🌟 Features

### 1. **Crime Mapping & Hotspot Analysis**
- Visualizes crime data on interactive maps
- Identifies high-risk areas using hotspot mapping algorithms
- Uses Delhi Accident Data for analysis

### 2. **CCTV & Facial Recognition**
- Real-time CCTV monitoring and face detection
- Stores and matches face embeddings against a database
- Tracks and identifies potential threats using facial recognition

### 3. **Safe Route Planning**
- Generates safest routes between locations
- Avoids high-crime areas and hotspots
- Multiple route maps for different Delhi regions:
  - Central Delhi routes
  - Keshavpuram to Rani Bagh
  - Punjabi Bagh to Mayur Vihar

### 4. **GPS Speed Tracking**
- Real-time GPS location monitoring
- Speed tracking for enhanced safety features

### 5. **Emergency SOS System**
- Quick emergency alert functionality
- Immediate notification system

## 📁 Project Structure

```
women-safety/
├── app.py.py                    # Main Flask application
├── flask.py                     # Flask server configuration
├── cctv recognition.py          # CCTV facial recognition module
├── combined.py                  # Combined functionality module
├── crimemapping.py              # Crime data visualization
├── cv.py                        # Computer vision utilities
├── hot spot mapping.py          # Crime hotspot analysis
├── gps speed.py                 # GPS tracking module
├── sos.py                       # Emergency SOS system
├── frontend.html                # Web interface
├── face_embeddings.npy          # Stored face embeddings database
├── rapist_embeddings.npy        # Criminal face embeddings database
├── Delhi Accident Data.csv      # Historical crime/accident data
├── safe_route_*.html            # Pre-generated safe route maps
└── mapping/                     # Mapping resources
```

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Computer Vision**: OpenCV (cv2)
- **Face Recognition**: Face embeddings with NumPy
- **Mapping**: Geocoding, Interactive maps
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML, JavaScript
- **Mobile**: Kivy framework

## 📋 Prerequisites

```bash
Python 3.7+
pip (Python package manager)
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd women-safety
```

2. **Install required packages**
```bash
pip install flask opencv-python numpy pandas geocoder folium scikit-learn
```

3. **Ensure data files are present**
- `Delhi Accident Data.csv`
- `face_embeddings.npy`
- `rapist_embeddings.npy`

## 💻 Usage

### Running the Main Application
```bash
python app.py.py
```

### Running Individual Modules

**Crime Mapping:**
```bash
python crimemapping.py
```

**CCTV Recognition:**
```bash
python "cctv recognition.py"
```

**Hotspot Mapping:**
```bash
python "hot spot mapping.py"
```

**GPS Tracking:**
```bash
python "gps speed.py"
```

**SOS System:**
```bash
python sos.py
```

### Accessing the Web Interface
Open `frontend.html` in a web browser or access via Flask server at `http://localhost:5000`

## 📊 Data Files

- **Delhi Accident Data.csv**: Contains historical crime and accident records for Delhi
- **face_embeddings.npy**: Database of known face embeddings for identification
- **rapist_embeddings.npy**: Database of criminal face embeddings for threat detection

## 🗺️ Safe Route Maps

The application generates and stores safe route maps for various Delhi regions:
- General Delhi safe routes
- Central Delhi specific routes  
- Keshavpuram to Rani Bagh routes
- Punjabi Bagh to Mayur Vihar routes

## ⚠️ Important Notes

- Ensure camera access permissions for CCTV recognition features
- GPS location permissions required for tracking features
- Keep face embeddings database updated for accurate recognition
- Crime data should be regularly updated for accurate hotspot analysis

## 🔒 Privacy & Security

- All face embeddings are stored locally
- GPS data is processed in real-time and not permanently stored
- User data is handled with strict privacy protocols

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is intended for research and educational purposes.

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Note**: This is a research project aimed at improving women's safety through technology. Always ensure compliance with local privacy laws and regulations when deploying such systems.
