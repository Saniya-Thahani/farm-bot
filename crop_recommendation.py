"""
Crop recommendation module for web application. 
This module provides crop recommendations and climate remedial measures
based on user input criteria.
"""

import json
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Month order for sorting
MONTH_ORDER = ["Chithirai", "Vaikasi", "Aani", "Aadi", "Aavani", "Purattasi", 
               "Aippasi", "Karthigai", "Margazhi", "Thai", "Maasi", "Panguni"]

def load_data():
    """Load crop data from the JSON file."""
    try:
        data_path = Path(__file__).parent / "static" / "data" / "csvjson.json"
        with open(data_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading crop data: {e}")
        return []

# Load data once when module is imported
crop_data = load_data()

def get_options(key):
    """Retrieve unique options from dataset for a specific field."""
    if key == "MONTH":
        # Extract unique month values and sort by Tamil month order
        months = set(entry.get(key, "Unknown") for entry in crop_data if key in entry)
        # Sort months based on the Tamil month order
        return sorted(months, 
                     key=lambda x: MONTH_ORDER.index(x.split("(")[0].strip()) 
                     if x.split("(")[0].strip() in MONTH_ORDER else float('inf'))
    
    # For other keys, just return sorted unique values
    return sorted(set(entry.get(key, "Unknown") for entry in crop_data if key in entry))

def find_crop_recommendations(soil_type=None, month=None, season=None, land_type=None, land_size=1.0):
    """
    Find suitable crops based on input criteria.
    
    Args:
        soil_type (str): Type of soil (e.g., "Red Soil", "Black Soil")
        month (str): Month for planting (e.g., "Aippasi(Mid October-Mid November)")
        season (str): Season (e.g., "Summer", "Winter") 
        land_type (str): Type of land (e.g., "Dry Land", "Wet Land")
        land_size (float): Size of land in acres
        
    Returns:
        list: List of suitable crop recommendations with details
    """
    logger.debug(f"Finding crops with soil={soil_type}, month={month}, season={season}, land_type={land_type}")
    
    filtered_data = crop_data
    
    # Apply filters if provided
    if soil_type:
        filtered_data = [entry for entry in filtered_data if entry.get("SOIL TYPE") == soil_type]
    
    if month:
        filtered_data = [entry for entry in filtered_data if entry.get("MONTH") == month]
    
    if season:
        filtered_data = [entry for entry in filtered_data if entry.get("SEASON") == season]
    
    if land_type:
        filtered_data = [entry for entry in filtered_data if entry.get("LAND TYPE") == land_type]
    
    # Prepare recommendations
    recommendations = []
    for entry in filtered_data:
        crop_name = entry.get("CROP NAME", "Unknown Crop")
        expected_yield = float(entry.get("YIELD", 0)) * land_size * 2.471 / 1000  # Convert to tons
        
        # Get remedial measures
        drought_measures = entry.get("REMEDIAL MEASURES - DROUGHT", "Information not available")
        flood_measures = entry.get("REMEDIAL MEASURE - FLOOD", "Information not available")
        
        # Format measures for better readability
        drought_measures = format_measures(drought_measures)
        flood_measures = format_measures(flood_measures)
        
        # Create recommendation object
        recommendation = {
            "crop_name": crop_name,
            "soil_type": entry.get("SOIL TYPE", "Unknown"),
            "month": entry.get("MONTH", "Unknown"),
            "season": entry.get("SEASON", "Unknown"),
            "land_type": entry.get("LAND TYPE", "Unknown"),
            "expected_yield": round(expected_yield, 2),
            "drought_measures": drought_measures,
            "flood_measures": flood_measures
        }
        
        recommendations.append(recommendation)
    
    return recommendations

def format_measures(measures_text):
    """Format remedial measures text for better readability."""
    # Split by periods or line breaks
    if not measures_text:
        return ["Information not available"]
        
    # Split by periods followed by space or newlines
    parts = []
    current_part = ""
    
    for char in measures_text:
        current_part += char
        if char == '.' and len(current_part.strip()) > 0:
            parts.append(current_part.strip())
            current_part = ""
    
    # Add any remaining text
    if current_part.strip():
        parts.append(current_part.strip())
    
    return parts if parts else ["Information not available"]

def format_recommendations_for_chat(recommendations, land_size=1.0):
    """
    Format crop recommendations for chat display.
    
    Args:
        recommendations (list): List of crop recommendation objects
        land_size (float): Size of land in acres
        
    Returns:
        str: Formatted string with recommendations
    """
    if not recommendations:
        return "I couldn't find any crop recommendations matching your criteria. Please try with different parameters."
    
    response = f"Based on your criteria, here are {len(recommendations)} crop recommendations:\n\n"
    
    # Limit to top 5 recommendations to avoid overwhelming the user
    for rec in recommendations[:5]:
        response += f"🌾 **{rec['crop_name']}**\n"
        response += f"   - Soil: {rec['soil_type']}\n"
        response += f"   - Planting Month: {rec['month']}\n"
        response += f"   - Season: {rec['season']}\n"
        response += f"   - Land Type: {rec['land_type']}\n"
        response += f"   - Expected Yield: {rec['expected_yield']} tons/year\n\n"
        
        # Add drought measures (limited to 3 for readability)
        response += "🏜️ **Drought Measures**:\n"
        for measure in rec['drought_measures'][:3]:
            response += f"   - {measure}\n"
        
        # Add flood measures (limited to 3 for readability)
        response += "\n🌊 **Flood Measures**:\n"
        for measure in rec['flood_measures'][:3]:
            response += f"   - {measure}\n"
        
        response += "\n" + "-" * 40 + "\n\n"
    
    # If there are more recommendations than shown
    if len(recommendations) > 5:
        response += f"\nThere are {len(recommendations) - 5} more recommendations matching your criteria."
    
    return response

def format_recommendations_for_chart(recommendations):
    """
    Format recommendations data for chart visualization.
    
    Args:
        recommendations (list): List of crop recommendation objects
        
    Returns:
        dict: Data formatted for chart visualization
    """
    if not recommendations:
        return {
            "labels": ["No matching crops"],
            "values": [0]
        }
    
    # Sort recommendations by expected yield
    sorted_recs = sorted(recommendations, key=lambda x: x['expected_yield'], reverse=True)
    
    # Limit to top 8 for better visualization
    top_recs = sorted_recs[:8]
    
    return {
        "labels": [rec['crop_name'] for rec in top_recs],
        "values": [rec['expected_yield'] * 100 / max(rec['expected_yield'] for rec in top_recs) for rec in top_recs]
    }

def get_climate_remedial_measures(climate_condition, recommendations=None):
    """
    Get climate remedial measures based on condition and available recommendations.
    
    Args:
        climate_condition (str): Climate condition (e.g., "drought", "flood")
        recommendations (list): Optional list of crop recommendations to extract measures from
        
    Returns:
        str: Formatted climate remedial measures
    """
    climate_condition = climate_condition.lower()
    
    if not recommendations:
        # If no specific recommendations, provide general measures from the first matching entries
        if "drought" in climate_condition:
            measures = []
            # Get unique drought measures from the first 3 entries that have them
            for entry in crop_data[:20]:
                drought_measures = entry.get("REMEDIAL MEASURES - DROUGHT")
                if drought_measures and drought_measures not in measures:
                    measures.append(drought_measures)
                if len(measures) >= 5:
                    break
            
            response = "Here are general remedial measures for drought conditions:\n\n"
            for i, measure in enumerate(measures, 1):
                response += f"{i}. {measure}\n\n"
            
            return response
            
        elif "flood" in climate_condition:
            measures = []
            # Get unique flood measures from the first 3 entries that have them
            for entry in crop_data[:20]:
                flood_measures = entry.get("REMEDIAL MEASURE - FLOOD")
                if flood_measures and flood_measures not in measures:
                    measures.append(flood_measures)
                if len(measures) >= 5:
                    break
            
            response = "Here are general remedial measures for flood conditions:\n\n"
            for i, measure in enumerate(measures, 1):
                response += f"{i}. {measure}\n\n"
            
            return response
        
        else:
            return "Please specify 'drought' or 'flood' to get climate remedial measures."
    
    # If recommendations are provided, extract measures from them
    response = f"Remedial measures for {climate_condition} conditions:\n\n"
    
    if "drought" in climate_condition:
        all_measures = []
        for rec in recommendations:
            all_measures.extend(rec['drought_measures'])
        
        # Get unique measures
        unique_measures = []
        for measure in all_measures:
            if measure not in unique_measures and measure != "Information not available":
                unique_measures.append(measure)
        
        for i, measure in enumerate(unique_measures[:7], 1):
            response += f"{i}. {measure}\n\n"
            
    elif "flood" in climate_condition:
        all_measures = []
        for rec in recommendations:
            all_measures.extend(rec['flood_measures'])
        
        # Get unique measures
        unique_measures = []
        for measure in all_measures:
            if measure not in unique_measures and measure != "Information not available":
                unique_measures.append(measure)
        
        for i, measure in enumerate(unique_measures[:7], 1):
            response += f"{i}. {measure}\n\n"
    
    else:
        response = "Please specify 'drought' or 'flood' to get climate remedial measures."
    
    return response