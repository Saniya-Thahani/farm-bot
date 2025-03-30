"""
Chatbot functionality for crop recommendations and climate remedial measures.
This module simulates the existing chatbot functionality.
"""

import logging
import random
from crop_data import crop_data, climate_remedies

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_crop_recommendation(user_input, filters=None):
    """
    Process user input and return crop recommendations
    
    Args:
        user_input (str): The user's query about crops
        filters (dict): Optional climate filters to apply
        
    Returns:
        str: Formatted crop recommendations
    """
    logger.debug(f"Processing crop recommendation query: {user_input}")
    
    # Extract key information from user input
    # This is a simplified version - in a real system, you would use 
    # more sophisticated NLP techniques or your existing chatbot logic
    user_input = user_input.lower()
    
    # Extract soil type, if mentioned
    soil_type = None
    for crop_info in crop_data:
        if crop_info['suitable_soil'].lower() in user_input:
            soil_type = crop_info['suitable_soil']
            break
    
    # Extract other conditions like temperature or rainfall if mentioned
    temperature_mentioned = any(word in user_input for word in ['hot', 'cold', 'warm', 'cool', 'temperature'])
    rainfall_mentioned = any(word in user_input for word in ['dry', 'wet', 'rain', 'rainfall', 'humid'])
    
    # Apply filters if provided
    filtered_crops = crop_data
    if filters:
        if 'temperature' in filters and filters['temperature']:
            temp_range = filters['temperature']
            filtered_crops = [crop for crop in filtered_crops 
                             if temp_range in crop['temperature_range']]
        
        if 'rainfall' in filters and filters['rainfall']:
            rain_range = filters['rainfall']
            filtered_crops = [crop for crop in filtered_crops 
                             if rain_range in crop['rainfall_requirements']]
        
        if 'soil' in filters and filters['soil']:
            soil = filters['soil']
            filtered_crops = [crop for crop in filtered_crops 
                             if soil.lower() in crop['suitable_soil'].lower()]
    
    # If soil type was mentioned in the query, filter by that
    elif soil_type:
        filtered_crops = [crop for crop in crop_data 
                         if soil_type.lower() in crop['suitable_soil'].lower()]
    
    # If no specific filters, but user mentioned temperature or rainfall
    # provide recommendations that include that information
    elif temperature_mentioned or rainfall_mentioned:
        filtered_crops = crop_data[:5]  # Just take a few samples in this case
    
    # Format the response
    if not filtered_crops:
        return "I couldn't find any crop recommendations matching your criteria. Please try with different parameters."
    
    response = "Based on your query, here are some crop recommendations:\n\n"
    
    for crop in filtered_crops[:5]:  # Limit to 5 recommendations
        response += f"🌱 **{crop['name']}**\n"
        response += f"   - Soil: {crop['suitable_soil']}\n"
        response += f"   - Temperature: {crop['temperature_range']}\n"
        response += f"   - Rainfall: {crop['rainfall_requirements']}\n"
        response += f"   - Growing Season: {crop['growing_season']}\n\n"
    
    return response

def get_climate_remedial_measures(user_input, filters=None):
    """
    Process user input and return climate remedial measures
    
    Args:
        user_input (str): The user's query about climate remedies
        filters (dict): Optional climate filters to apply
        
    Returns:
        str: Formatted climate remedial measures
    """
    logger.debug(f"Processing climate remedial measures query: {user_input}")
    
    # Extract climate condition from user input
    user_input = user_input.lower()
    climate_condition = None
    
    for condition in climate_remedies.keys():
        if condition.lower() in user_input:
            climate_condition = condition
            break
    
    # Apply filters if provided
    if filters and 'climate_condition' in filters and filters['climate_condition']:
        climate_condition = filters['climate_condition']
    
    # If no specific condition found or specified, provide general remedies
    if not climate_condition:
        response = "Here are some general remedial measures for extreme climate conditions:\n\n"
        # Select a few random remedies from different conditions
        selected_remedies = []
        for condition, remedies in climate_remedies.items():
            selected_remedies.append(f"For {condition}:\n- {random.choice(remedies)}")
        
        response += "\n\n".join(selected_remedies[:3])
        return response
    
    # If specific condition found, provide specific remedies
    if climate_condition in climate_remedies:
        remedies = climate_remedies[climate_condition]
        response = f"Remedial measures for {climate_condition}:\n\n"
        
        for remedy in remedies:
            response += f"• {remedy}\n"
        
        return response
    else:
        return "I couldn't find specific remedial measures for that climate condition. Please try asking about drought, flooding, extreme heat, or frost."
