# SafeGuard Deployment Guide - v2.0

Complete setup and deployment instructions for SafeGuard Women Safety Application.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [Production Deployment](#production-deployment)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Monitoring & Logs](#monitoring--logs)

---

## Prerequisites

### System Requirements

**Minimum:**
- OS: Windows, Mac, or Linux
- Python: 3.7 or higher
- RAM: 2GB
- Storage: 500MB
- Internet: Required for maps and APIs

**Recommended:**
- Python: 3.9 or higher
- RAM: 4GB
- SSD for better performance
- Consistent internet connection

### Required Software

```bash
# Windows (use PowerShell)
python --version          # Check Python installation
pip --version            # Check pip installation

# Mac/Linux
python3 --version
pip3 --version
```

### Browser Support

- Chrome/Chromium (v90+)
- Firefox (v88+)
- Safari (v14+)
- Edge (v90+)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## Local Development Setup

### Step 1: Clone or Download Project

```bash
# If using Git
git clone <repository-url>
cd women-safety

# Or extract downloaded ZIP
unzip women-safety.zip
cd women-safety
```

### Step 2: Create Python Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

Wait for all packages to install. This may take 2-5 minutes.

### Step 4: Verify Installation

```bash
# Check Flask
python -c "import flask; print(f'Flask: {flask.__version__}')"

# Check other packages
python -c "import pandas, numpy, folium, networkx; print('All imports successful!')"
```

---

## Installation

### Complete Installation Script

**Windows (run in PowerShell):**
```powershell
# Navigate to project directory
cd "C:\path\to\women-safety"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Verify
python app.py
```

**Mac/Linux (run in Terminal):**
```bash
# Navigate to project directory
cd /path/to/women-safety

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python app.py
```

### Data Files Setup

**Ensure these files are in the project directory:**

1. **Delhi Accident Data.csv**
   - Contains crime statistics
   - Format: latitude, longitude, crime_score, incident_type, timestamp
   - Optional: App uses mock data if not present

2. **rapist_embeddings.npy**
   - Face recognition embeddings
   - Optional: CCTV features work without it

3. **face_embeddings.npy**
   - General face embeddings database
   - Optional: For facial recognition

If these files are missing:
- App will use mock data automatically
- Log message: "⚠️ ... not found, using mock data"
- App still fully functional!

---

## Running the Application

### Development Mode

```bash
# Make sure virtual environment is activated (see (venv) in terminal)

# Start the server
python app.py
```

You should see:
```
🚀 Starting SafeGuard Application v2.0
================================================
SafeGuard - Women Safety Application
Version: 2.0
Last Updated: March 2026
================================================
🌐 Starting Flask server on http://127.0.0.1:5000
Press Ctrl+C to stop the server
```

### Access the Application

1. Open web browser
2. Navigate to: `http://127.0.0.1:5000`
3. You should see the SafeGuard homepage

### Testing Locally

```bash
# Test health endpoint
curl http://127.0.0.1:5000/api/health

# Test crime hotspots
curl http://127.0.0.1:5000/api/crime_hotspots

# Test safe route calculation
curl -X POST http://127.0.0.1:5000/api/find_safe_route \
  -H "Content-Type: application/json" \
  -d '{"start": 0, "end": 3, "destination": "Delhi"}'
```

### Stop the Server

```bash
# Press Ctrl+C in the terminal running app.py
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] All features tested locally
- [ ] Requirements.txt updated
- [ ] No debug code remaining
- [ ] Logging configured
- [ ] Error handling in place
- [ ] Static files minified
- [ ] Environmental secrets set
- [ ] Database configured (if applicable)
- [ ] SSL certificate obtained
- [ ] Backups created

### Deployment Options

#### Option 1: Heroku (Recommended for beginners)

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   heroku --version
   ```

2. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

3. **Create runtime.txt**
   ```
   python-3.9.13
   ```

4. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

#### Option 2: AWS EC2

1. **Launch EC2 Instance**
   - OS: Ubuntu 20.04
   - Type: t2.micro (free tier)
   - Security group: Allow ports 80, 443, 22

2. **Connect & Setup**
   ```bash
   ssh -i key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3 python3-pip python3-venv -y
   
   # Clone repository
   git clone <repo-url>
   cd women-safety
   
   # Setup venv and install
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

#### Option 3: Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. **Build and Run**
   ```bash
   docker build -t safeguard:latest .
   docker run -p 5000:5000 safeguard:latest
   ```

#### Option 4: DigitalOcean App Platform

1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
4. Deploy

### SSL/HTTPS Setup

**For production, always use HTTPS:**

```bash
# Using Let's Encrypt (free)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --standalone -d yourdomain.com
```

---

## Configuration

### Environment Variables

Create `.env` file in project root:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Application Settings
APP_VERSION=2.0
APP_NAME=SafeGuard

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost/safeguard

# API Keys (if needed)
GOOGLE_API_KEY=your-api-key
MAPBOX_API_KEY=your-api-key

# Email Configuration (for alerts)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/safeguard.log
```

### Update app.py to use .env

```python
from dotenv import load_dotenv
import os

load_dotenv()

app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', False)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
```

---

## Performance Optimization

### 1. Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/crime_hotspots')
@cache.cached(timeout=3600)
def get_crime_hotspots():
    ...
```

### 2. Compress Responses

```python
from flask_compress import Compress

Compress(app)
```

### 3. Database Connection Pooling

```python
from sqlalchemy.pool import QueuePool

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### 4. Minify Static Files

```bash
# Install minifiers
pip install csscompressor jsmin

# Minify CSS
python -c "import csscompressor; print(csscompressor.compress(open('styles.css').read()))" > styles.min.css

# Minify JS
python -c "import jsmin; print(jsmin.jsmin(open('script.js').read()))" > script.min.js
```

---

## Monitoring & Logs

### Real-time Logs

```bash
# View live logs
tail -f logs/safeguard.log

# Filter errors
grep ERROR logs/safeguard.log

# Find API calls
grep "/api/" logs/safeguard.log
```

### Key Metrics to Monitor

```
- Response time: < 200ms
- Error rate: < 1%
- CPU usage: < 70%
- Memory usage: < 500MB
- API uptime: > 99.9%
```

### Setting Up Alerts

**Recommended tools:**
- New Relic
- Datadog
- Sentry (error tracking)
- CloudWatch (AWS)

### Health Check

Setup periodic health checks:

```bash
# Cron job every 5 minutes (Linux)
*/5 * * * * curl -s http://localhost:5000/api/health || alert

# Task scheduler every 5 minutes (Windows)
# Create task with action: C:\path\to\healthcheck.bat
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Make sure venv is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Then install again
pip install -r requirements.txt
```

### Issue: "Address already in use"

**Solution:**
```bash
# Port 5000 already in use
# Option 1: Kill existing process
lsof -i :5000  # Find process
kill -9 <PID>  # Kill it

# Option 2: Use different port
python app.py --port 5001
```

### Issue: "No module named 'Delhi Accident Data.csv'"

**Solution:**
This is expected. The app uses mock data if the CSV is missing.
To use real data:
```bash
# Place CSV in project directory
cp /path/to/Delhi\ Accident\ Data.csv .
```

### Issue: Maps not loading

**Solution:**
```bash
# Check internet connection
# Verify Leaflet CDN is accessible
# Try different browser
# Clear browser cache
```

### Issue: Location permission denied

**Solution:**
```bash
# Check browser settings
# Allow location for http://localhost:5000
# Some browsers require HTTPS for location
```

### Issue: High memory usage

**Solution:**
```bash
# Monitor with
watch -n 1 'ps aux | grep app.py'

# Reduce logging level
# Implement caching
# Add database connection pooling
```

---

## Security Hardening

### Production Checklist

```python
# In app.py
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['PROPAGATE_EXCEPTIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Enable CORS only for trusted domains
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

### Enable SSL

```bash
# Create self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run Flask with SSL
python app.py --ssl-context=adhoc
# Or
gunicorn --certfile=cert.pem --keyfile=key.pem app:app
```

---

## Backup Strategy

### Regular Backups

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"

mkdir -p $BACKUP_DIR

# Backup files
tar -czf $BACKUP_DIR/safeguard_$DATE.tar.gz \
  --exclude venv \
  --exclude __pycache__ \
  --exclude .git \
  .

echo "Backup created: $BACKUP_DIR/safeguard_$DATE.tar.gz"
```

### Database Backup

```bash
# PostgreSQL
pg_dump safeguard_db > backup_$(date +%Y%m%d).sql

# MongoDB
mongodump --db safeguard --out backup_$(date +%Y%m%d)
```

---

## Maintenance Schedule

| Task | Frequency | Priority |
|------|-----------|----------|
| Check logs | Daily | High |
| Monitor resources | Daily | High |
| Backup database | Daily | Critical |
| Update OS packages | Weekly | Medium |
| Update Python packages | Monthly | Medium |
| Security audit | Monthly | High |
| Performance review | Monthly | Medium |

---

## Support & Resources

- **Documentation:** See README.md
- **User Guide:** See USER_GUIDE.md
- **Technical Fixes:** See TECHNICAL_FIXES.md
- **Official Docs:** [Flask](https://flask.palletsprojects.com/)
- **Community:** [Python Forum](https://www.python.org/community/)

---

## Rollback Procedure

If deployment fails:

```bash
# Check previous version
git log --oneline

# Revert to previous version
git revert <commit-hash>

# Or restore from backup
tar -xzf backups/safeguard_YYYYMMDD.tar.gz

# Restart service
systemctl restart safeguard
```

---

**Last Updated:** March 2026
**SafeGuard v2.0**
