"""
This module contains data for crop recommendations and climate remedial measures.
This data would typically come from a database or external API in a production environment.
"""

# Sample crop data
crop_data = [
    {
        "name": "Rice",
        "suitable_soil": "Clay or Clay loam",
        "temperature_range": "20-35°C",
        "rainfall_requirements": "High (>150cm annually)",
        "growing_season": "Kharif (monsoon)",
        "description": "Staple food crop that grows well in waterlogged soils"
    },
    {
        "name": "Wheat",
        "suitable_soil": "Loam or Clay loam",
        "temperature_range": "15-25°C",
        "rainfall_requirements": "Moderate (75-100cm annually)",
        "growing_season": "Rabi (winter)",
        "description": "Important grain crop that requires well-drained soils"
    },
    {
        "name": "Maize (Corn)",
        "suitable_soil": "Sandy loam",
        "temperature_range": "18-30°C",
        "rainfall_requirements": "Moderate (50-75cm annually)",
        "growing_season": "Kharif and Rabi",
        "description": "Versatile crop used for food, feed, and industrial purposes"
    },
    {
        "name": "Cotton",
        "suitable_soil": "Black soil (regur)",
        "temperature_range": "20-30°C",
        "rainfall_requirements": "Moderate (50-100cm annually)",
        "growing_season": "Kharif",
        "description": "Important fiber crop that requires well-drained black soils"
    },
    {
        "name": "Sugarcane",
        "suitable_soil": "Loam or Clay loam",
        "temperature_range": "20-35°C",
        "rainfall_requirements": "High (100-150cm annually)",
        "growing_season": "Year-round (12-18 months)",
        "description": "Perennial crop requiring good moisture and fertile soils"
    },
    {
        "name": "Pulses (Lentils)",
        "suitable_soil": "Sandy loam",
        "temperature_range": "18-25°C",
        "rainfall_requirements": "Low to Moderate (40-75cm annually)",
        "growing_season": "Rabi",
        "description": "Nitrogen-fixing crops that improve soil fertility"
    },
    {
        "name": "Groundnut",
        "suitable_soil": "Sandy loam",
        "temperature_range": "25-30°C",
        "rainfall_requirements": "Moderate (50-75cm annually)",
        "growing_season": "Kharif",
        "description": "Important oilseed crop that grows well in well-drained soils"
    },
    {
        "name": "Soybeans",
        "suitable_soil": "Loam to Clay loam",
        "temperature_range": "20-30°C",
        "rainfall_requirements": "Moderate (60-100cm annually)",
        "growing_season": "Kharif",
        "description": "Protein-rich crop that adapts to various soil conditions"
    },
    {
        "name": "Potato",
        "suitable_soil": "Sandy loam",
        "temperature_range": "15-20°C",
        "rainfall_requirements": "Moderate (50-75cm annually)",
        "growing_season": "Rabi",
        "description": "Cool-season crop requiring well-drained, loose soils"
    },
    {
        "name": "Tomato",
        "suitable_soil": "Loam",
        "temperature_range": "20-27°C",
        "rainfall_requirements": "Moderate (50-75cm annually)",
        "growing_season": "Year-round with irrigation",
        "description": "Popular vegetable crop sensitive to frost and excess moisture"
    },
    {
        "name": "Onion",
        "suitable_soil": "Sandy loam",
        "temperature_range": "15-25°C",
        "rainfall_requirements": "Low to Moderate (40-60cm annually)",
        "growing_season": "Rabi",
        "description": "Root crop that requires well-drained soils and moderate moisture"
    },
    {
        "name": "Mustard",
        "suitable_soil": "Loam",
        "temperature_range": "10-20°C",
        "rainfall_requirements": "Low (40-60cm annually)",
        "growing_season": "Rabi",
        "description": "Oilseed crop that grows well in cooler conditions"
    },
    {
        "name": "Mango",
        "suitable_soil": "Loam to Sandy loam",
        "temperature_range": "24-30°C",
        "rainfall_requirements": "Moderate (75-100cm annually)",
        "growing_season": "Perennial",
        "description": "Tropical fruit tree sensitive to frost and waterlogging"
    },
    {
        "name": "Banana",
        "suitable_soil": "Loam to Clay loam",
        "temperature_range": "20-35°C",
        "rainfall_requirements": "High (>120cm annually)",
        "growing_season": "Year-round",
        "description": "Fast-growing fruit crop requiring good moisture and drainage"
    },
    {
        "name": "Coffee",
        "suitable_soil": "Well-drained loam",
        "temperature_range": "15-25°C",
        "rainfall_requirements": "High (150-200cm annually)",
        "growing_season": "Perennial",
        "description": "Shade-loving crop that grows well at higher elevations"
    }
]

# Climate remedial measures
climate_remedies = {
    "Drought": [
        "Implement drip irrigation systems to maximize water efficiency",
        "Use mulching to reduce soil water evaporation",
        "Plant drought-resistant crop varieties",
        "Practice rainwater harvesting and storage",
        "Implement crop rotation with drought-tolerant species",
        "Reduce plant density to decrease water competition",
        "Apply organic matter to improve soil water retention"
    ],
    "Flooding": [
        "Create proper drainage channels in fields",
        "Build raised beds for crops sensitive to waterlogging",
        "Plant flood-tolerant crop varieties like rice",
        "Implement contour farming to reduce runoff",
        "Maintain vegetative buffers along waterways",
        "Practice early or late planting to avoid flood seasons",
        "Construct small earthen embankments around vulnerable fields"
    ],
    "Extreme Heat": [
        "Provide shade using shade nets or intercropping",
        "Increase irrigation frequency with smaller amounts",
        "Apply mulch to keep soil temperatures lower",
        "Plant heat-tolerant crop varieties",
        "Use evaporative cooling systems in extreme conditions",
        "Implement night-time irrigation to reduce heat stress",
        "Adjust planting dates to avoid peak summer heat"
    ],
    "Frost": [
        "Use overhead sprinkler irrigation during frost events",
        "Install frost protection fans to mix air layers",
        "Apply row covers or tunnels for sensitive crops",
        "Plant cold-hardy varieties in frost-prone areas",
        "Create smoke screens to reduce radiative cooling",
        "Choose proper field locations with good air drainage",
        "Maintain soil moisture which helps retain heat"
    ],
    "Erratic Rainfall": [
        "Implement water conservation techniques like micro-irrigation",
        "Build water harvesting structures like farm ponds",
        "Practice conservation tillage to improve soil moisture retention",
        "Use climate-smart crop varieties with flexible growing seasons",
        "Diversify crops to spread rainfall utilization",
        "Implement agroforestry systems for climate buffering",
        "Use weather forecasting services for better planning"
    ]
}
