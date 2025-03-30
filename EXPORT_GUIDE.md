# FarmBot Application Export Guide

This guide provides instructions for exporting and deploying the FarmBot Crop Recommendation application.

## Files You Need to Export

### Python Files
- `app.py` - Main Flask application with routes and endpoints
- `main.py` - Entry point that runs the Flask app
- `crop_recommendation.py` - Core recommendation logic
- `crop_data.py` - Sample crop data (used as fallback)
- `chatbot.py` - Chatbot interaction logic

### Templates (HTML)
- `templates/layout.html` - Base template with navigation and footer
- `templates/index.html` - Main application interface
- `templates/about.html` - About page

### Static Files
- `static/css/custom.css` - Custom styling
- `static/js/app.js` - Main application JavaScript
- `static/js/charts.js` - Chart visualization code
- `static/js/translations.js` - Language translations (currently English only)
- `static/data/csvjson.json` - Dataset for crop recommendations

### Additional Files
- `export_requirements.txt` - List of Python package dependencies

## Deployment Options

### Option 1: Deploying on Replit

1. Click on the "Deploy" button at the top of the Replit interface
2. Follow the prompts to set up your deployment
3. Your app will be accessible at `[your-repl-name].replit.app`

### Option 2: Deploying on a Local Server

1. Copy all files listed above to your local machine
2. Install the required dependencies:
   ```
   pip install -r export_requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Access the application at `http://localhost:5000`

### Option 3: Deploying on a Cloud Server (e.g., AWS, Google Cloud, Heroku)

1. Copy all files to your server or repository
2. Install the required dependencies
3. Set up the appropriate web server (e.g., Gunicorn)
4. Configure your server to run: `gunicorn --bind 0.0.0.0:$PORT main:app`
5. Set up any necessary environment variables if needed

## Environment Variables

If you're deploying to a production environment, consider setting these environment variables:
- `SESSION_SECRET` - Secret key for session security (currently has a default value in app.py)

## Important Notes

1. This application does not require a database as it uses the JSON file for data
2. The app is designed to be run with Gunicorn in production
3. The application currently shows data in English only
4. Make sure your server allows traffic on port 5000 (or configure accordingly)

## Troubleshooting

- If you encounter missing files, double-check that you've exported all files listed above
- If styles are not loading, ensure that the Bootstrap CSS file URL is accessible
- For any API errors, check the browser console and server logs for more details

## Support

For any questions or issues, please refer to the about page in the application or contact the support email listed there.