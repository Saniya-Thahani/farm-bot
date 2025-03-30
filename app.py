import os
import logging
from flask import Flask, render_template, request, jsonify, session
from crop_recommendation import (
    find_crop_recommendations, 
    format_recommendations_for_chat,
    format_recommendations_for_chart,
    get_climate_remedial_measures,
    get_options
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint to interact with the chatbot
    Expects: JSON with 'message' and 'filters' (optional)
    Returns: JSON with chatbot response
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        filters = data.get('filters', {})
        
        logger.debug(f"Received message: {message}")
        logger.debug(f"Filters: {filters}")
        
        # Process the message to determine what the user is asking for
        message_lower = message.lower()
        
        # Initialize parameters
        soil_type = filters.get('soil', None)
        month = None
        season = None
        land_type = filters.get('land_type', 'Dry Land')  # Default to dry land
        land_size = 1.0  # Default to 1 acre
        
        # Extract land size if mentioned
        if "acre" in message_lower:
            # Try to find a number before "acre"
            words = message_lower.split()
            for i, word in enumerate(words):
                if word == "acre" or word == "acres" and i > 0:
                    try:
                        land_size = float(words[i-1])
                    except ValueError:
                        pass
        
        # Handle climate remedial measures request
        if 'climate' in message_lower or 'remedy' in message_lower or 'drought' in message_lower or 'flood' in message_lower:
            climate_condition = "drought"  # Default
            if "flood" in message_lower:
                climate_condition = "flood"
                
            # Get any specific climate condition from filters
            if filters.get('climate_condition'):
                if "drought" in filters.get('climate_condition').lower():
                    climate_condition = "drought"
                elif "flood" in filters.get('climate_condition').lower():
                    climate_condition = "flood"
            
            # Find recommendations first to extract measures from them
            recommendations = find_crop_recommendations(soil_type, month, season, land_type, land_size)
            response = get_climate_remedial_measures(climate_condition, recommendations)
        
        # Handle crop recommendations request
        else:
            # Extract season if mentioned
            if "summer" in message_lower:
                season = "Summer"
            elif "winter" in message_lower:
                season = "Winter"
            elif "rainy" in message_lower or "monsoon" in message_lower:
                season = "Rainy"
                
            # Use filter values if provided
            if filters.get('season'):
                season = filters.get('season')
                
            if filters.get('month'):
                month = filters.get('month')
                
            # Find and format recommendations
            recommendations = find_crop_recommendations(soil_type, month, season, land_type, land_size)
            response = format_recommendations_for_chat(recommendations, land_size)
        
        return jsonify({
            'status': 'success',
            'response': response
        })
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/options', methods=['GET'])
def get_filter_options():
    """
    Get available options for dropdown filters
    """
    try:
        option_type = request.args.get('type', '')
        
        if option_type in ["SOIL TYPE", "MONTH", "SEASON", "LAND TYPE"]:
            options = get_options(option_type)
            return jsonify({
                'status': 'success',
                'options': options
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f"Invalid option type: {option_type}"
            }), 400
    
    except Exception as e:
        logger.error(f"Error getting options: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get crop recommendations based on query parameters
    Used for visualization purposes
    """
    try:
        # Get parameters from query string
        soil_type = request.args.get('soil', None)
        month = request.args.get('month', None)
        season = request.args.get('season', None)
        land_type = request.args.get('land_type', 'Dry Land')
        land_size = float(request.args.get('land_size', 1.0))
        
        # Find crop recommendations based on parameters
        recommendations = find_crop_recommendations(
            soil_type, month, season, land_type, land_size
        )
        
        # Format the recommendations for the chart
        chart_data = format_recommendations_for_chart(recommendations)
        
        return jsonify({
            'status': 'success',
            'data': chart_data
        })
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"An error occurred: {str(e)}"
        }), 500


