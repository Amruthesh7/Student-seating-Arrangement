# Deploy to Heroku

## Steps to Deploy:

1. **Install Heroku CLI**
   - Download from: https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create student-seating-portal
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open Your App**
   ```bash
   heroku open
   ```

## Note:
- Requires credit card for verification (but free tier available)
- URL will be: `https://student-seating-portal.herokuapp.com`
