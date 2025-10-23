# Deploy to Render (Free Hosting)

## Steps to Deploy:

1. **Go to Render.com**
   - Visit: https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select: `Amruthesh7/Student-seating-Arrangement`

3. **Configure Settings**
   - **Name**: `student-seating-portal`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app
   - You'll get a URL like: `https://student-seating-portal.onrender.com`

5. **Access Your App**
   - Your app will be live at the provided URL
   - Free tier includes 750 hours/month

## Benefits:
- ✅ Free tier available
- ✅ Automatic SSL certificates
- ✅ Custom domain support
- ✅ Easy GitHub integration
