# URL Shortener - Deployment Guide

## 🚀 Quick Deploy to Heroku (Recommended)

### Prerequisites
- Heroku account (free at heroku.com)
- Git installed
- Heroku CLI installed

### Steps

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   cd 06_shorturl
   heroku create your-app-name-here
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Open your app**
   ```bash
   heroku open
   ```

## 🔧 Alternative: Railway Deployment

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select this project folder
4. Deploy automatically

## 📝 Environment Variables (Optional)

For production, set these environment variables:

```bash
# In Heroku dashboard or via CLI
heroku config:set SECRET_KEY=your-super-secret-key-here
heroku config:set FLASK_ENV=production
```

## 🛠️ Local Testing

```bash
cd 06_shorturl
python app.py
```

Visit: http://localhost:5000

## ✅ Features

- ✅ URL shortening with unique codes
- ✅ Click tracking
- ✅ Modern, responsive UI
- ✅ URL validation
- ✅ Error handling
- ✅ Delete functionality
- ✅ Flash messages

## 🔒 Security Notes

- Change the secret key in production
- Consider adding rate limiting
- Add HTTPS redirect
- Consider adding user authentication for advanced features

## 📊 Database

- Uses SQLite (included in deployment)
- No additional database setup required
- Data persists between deployments
