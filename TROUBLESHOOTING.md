# Deployment Troubleshooting Guide

## "Application failed to respond" Error

### Common Causes and Solutions:

#### 1. **Database Connection Issues**
- **Problem**: SQLite database not accessible in production
- **Solution**: Use PostgreSQL or MySQL for production
- **Check**: Visit `/health` endpoint to see database status

#### 2. **Port Configuration**
- **Problem**: App not listening on correct port
- **Solution**: Use PORT environment variable
- **Fixed**: Updated to use `os.environ.get('PORT', 5000)`

#### 3. **Missing Dependencies**
- **Problem**: Required packages not installed
- **Solution**: Check requirements.txt includes all dependencies
- **Fixed**: Added gunicorn and all required packages

#### 4. **WSGI Configuration**
- **Problem**: Incorrect WSGI entry point
- **Solution**: Use proper WSGI application object
- **Fixed**: Created wsgi.py with correct application object

## Debugging Steps:

### 1. **Check Health Endpoint**
Visit: `https://your-app-url.railway.app/health`
Should return:
```json
{
  "status": "healthy",
  "message": "Student Seating Arrangement Portal is running",
  "database": "connected"
}
```

### 2. **Check Deployment Logs**
Look for these messages:
- ✅ "Database tables created successfully"
- ✅ "Starting server on port XXXX"
- ❌ Any error messages

### 3. **Common Error Messages**

#### "Module not found"
- **Solution**: Check requirements.txt includes all dependencies

#### "Database locked"
- **Solution**: Use PostgreSQL instead of SQLite for production

#### "Port already in use"
- **Solution**: Use PORT environment variable

## Platform-Specific Solutions:

### Railway
1. Go to your project dashboard
2. Click on "Deployments"
3. Check the logs for error messages
4. If needed, add environment variables:
   - `SECRET_KEY`: Any random string
   - `DATABASE_URL`: Will be auto-provided

### Render
1. Go to your service dashboard
2. Click on "Logs"
3. Check for build and runtime errors
4. Ensure build command: `pip install -r requirements.txt`
5. Ensure start command: `python start.py`

### Heroku
1. Check logs: `heroku logs --tail`
2. Check config: `heroku config`
3. Add environment variables if needed

## Quick Fixes:

### If still failing, try this minimal version:
1. **Use PostgreSQL**: Most hosting platforms provide this
2. **Check logs**: Look for specific error messages
3. **Test locally**: Run `python start.py` locally first

## Environment Variables to Set:
```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://... (auto-provided by platform)
PORT=5000 (auto-provided by platform)
```

## Test Commands:
```bash
# Test locally
python start.py

# Test with gunicorn
gunicorn wsgi:application

# Check health
curl http://localhost:5000/health
```

Your app should work after these fixes! 🚀
