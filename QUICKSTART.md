# SafeGuard Quick Start Guide

Get SafeGuard running in 5 minutes!

---

## ⚡ Ultra-Quick Start (5 minutes)

### For Windows Users

```powershell
# Step 1: Open PowerShell in the project folder
cd C:\path\to\women-safety

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate it
.\venv\Scripts\Activate.ps1

# Step 4: Install packages
pip install -r requirements.txt

# Step 5: Run!
python app.py
```

**Then open browser:** http://127.0.0.1:5000

### For Mac/Linux Users

```bash
# Step 1: Navigate to project
cd /path/to/women-safety

# Step 2: Create virtual environment
python3 -m venv venv

# Step 3: Activate it
source venv/bin/activate

# Step 4: Install packages
pip install -r requirements.txt

# Step 5: Run!
python app.py
```

**Then open browser:** http://127.0.0.1:5000

---

## 📋 Complete Checklist

- [ ] Python 3.7+ installed
- [ ] Project folder downloaded
- [ ] Virtual environment created
- [ ] Packages installed
- [ ] App running on http://127.0.0.1:5000
- [ ] Location permission granted
- [ ] Tested one feature

---

## 🎮 First Steps After Launch

1. **Homepage loads** ✓
   - See SafeGuard branding
   - View feature overview

2. **Go to Dashboard**
   - Click "Dashboard" in menu
   - Allow location permission

3. **Try Features**
   - Click "Get My Location"
   - View the crime map
   - Try "Find Safe Route"
   - Test buttons

4. **View Documentation**
   - Open USER_GUIDE.md
   - Read about each feature
   - Learn safety tips

---

## 🧪 Quick Test Commands

```bash
# Test API is running
curl http://127.0.0.1:5000/api/health

# Get crime hotspots
curl http://127.0.0.1:5000/api/crime_hotspots

# Calculate safe route
curl -X POST http://127.0.0.1:5000/api/find_safe_route \
  -H "Content-Type: application/json" \
  -d '{"start": 0, "end": 3, "destination": "Delhi"}'
```

---

## 🆘 Troubleshooting

### App won't start?
```bash
# Check Python version
python --version  # Should be 3.7+

# Reinstall packages
pip install --upgrade -r requirements.txt

# Run again
python app.py
```

### "Address already in use"?
```bash
# Find what's using port 5000
# Windows:
netstat -ano | findstr :5000

# Mac/Linux:
lsof -i :5000

# Kill process (Windows):
taskkill /PID <PID> /F

# Then try again
python app.py
```

### Location not working?
- Browser may need HTTPS
- Try http://localhost:5000 (not 127.0.0.1)
- Check browser location permissions
- Use manual coordinates

### Map not showing?
- Check internet connection
- Try different browser
- Clear browser cache
- Refresh page

---

## 📱 Access on Phone

To access from your phone on same network:

### Find your computer IP
**Windows:**
```powershell
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.1.100)
```

**Mac/Linux:**
```bash
ifconfig
# Look for inet address
```

### On your phone
Open browser and go to:
```
http://YOUR_COMPUTER_IP:5000
```

Example: `http://192.168.1.100:5000`

**Same network requirement:** Phone and computer must be on same WiFi

---

## 🚀 What's Running?

Your SafeGuard app is now running with:

✅ **Frontend**
- Modern web interface
- Crime mapping
- Safe route planning

✅ **Backend API**
- Crime data endpoints
- GPS tracking
- Emergency SOS
- Statistics

✅ **Interactive Map**
- Leaflet.js powered
- Crime hotspot visualization
- Real-time updates

✅ **Logging**
- Console output
- Performance metrics
- Error tracking

---

## 📚 Next Steps

1. **Read Documents**
   - [README.md](README.md) - Overview
   - [USER_GUIDE.md](USER_GUIDE.md) - Feature guide
   - [TECHNICAL_FIXES.md](TECHNICAL_FIXES.md) - Technical details

2. **Explore Features**
   - Test all buttons
   - Try different destinations
   - Check mobile view

3. **For Deployment**
   - Read [DEPLOYMENT.md](DEPLOYMENT.md)
   - Choose hosting platform
   - Follow setup steps

4. **For Development**
   - Review app.py
   - Add features
   - Contribute improvements

---

## ⚙️ Common Commands

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Deactivate virtual environment
deactivate

# View installed packages
pip list

# Update packages
pip install -r requirements.txt --upgrade

# Stop the app
# Ctrl+C in terminal

# View logs
# Check terminal output
```

---

## 🆘 Stuck?

1. **Check the error message** - Often describes the problem
2. **Check browser console** - Press F12, look at Console tab
3. **Read relevant documentation**:
   - General issues → README.md
   - User questions → USER_GUIDE.md
   - Technical problems → TECHNICAL_FIXES.md
   - Deployment problems → DEPLOYMENT.md
4. **Google the error** - Often has solutions
5. **Contact support** - support@safeguard.com

---

## ✅ You're Ready!

You now have:
- ✓ SafeGuard running locally
- ✓ Full access to features
- ✓ Crime mapping and routing
- ✓ Emergency SOS capability
- ✓ All documentation

**Happy using SafeGuard!**

---

## 💡 Pro Tips

1. **Bookmark the site** - Add to favorites
2. **Test on mobile** - Use same WiFi
3. **Check logs** - See what's happening
4. **Ask questions** - Refer to guides
5. **Give feedback** - Help us improve

---

**Version:** 2.0 (March 2026)  
**Time to Setup:** ~5 minutes  
**Difficulty:** Beginner-friendly ⭐
