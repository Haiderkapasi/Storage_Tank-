import streamlit as st
import math

# Set page config for wide layout and remove scrollbar
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Apply custom CSS for fonts and styling
st.markdown("""
    <style>
    /* Custom fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        color: #444;
        background-color:#3C3744;
    }

    h1 {
        font-family: 'Poppins', sans-serif;
        color: '#FBFFF1';
    }
    h2, h3, h4 {
        font-family: 'Roboto', sans-serif;
        color: #B4C5E4;
        
    }

    .stButton button {
        background-color: #3D52D5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 1.2em;
        border: none;
    }

    .stButton button:hover {
        background-color: #40303E;
    }

    .stSelectbox, .stNumber_input {
        border-radius: 8px;
        background-color: #fff;
        border: 1px solid #ddd;
    }

    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
        font-size: 1em;
    }

    .stMarkdown h2 {
        color: #090C9B;
    }
            
    /* Remove scrollbar */
    ::-webkit-scrollbar {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Data for H₂O₂ concentration based on industry use cases
use_cases = {
    "Paper Industry": {"concentration": 30, "density": 1.11, "material": "Stainless Steel", "color": "Silver"},
    "Clothing Industry": {"concentration": 20, "density": 1.07, "material": "Polyethylene", "color": "White"},
    "Chemical Synthesis": {"concentration": 50, "density": 1.20, "material": "HDPE", "color": "Opaque"},
    "Water Treatment": {"concentration": 35, "density": 1.14, "material": "Fiberglass", "color": "Blue"},
    "Cosmetic Industry": {"concentration": 10, "density": 1.03, "material": "Polypropylene", "color": "White"},
    "Rocket Propellant": {"concentration": 90, "density": 1.45, "material": "Titanium", "color": "Silver"}
}

# Function to calculate tank volume
def calculate_tank_volume(production_rate, buffer_days, density):
    total_storage = (production_rate * buffer_days * 1000) / density
    return total_storage

# Function to calculate height and diameter
def calculate_height_diameter(volume):
    diameter = (volume / (math.pi * 1.5)) ** (1/3)
    height = 1.5 * diameter
    return height/10, diameter/10

# Function to calculate pressure
def calculate_pressure(density, height):
    return density * 9.8 * (height / 2)

# Function to calculate the four thicknesses
def calculate_thicknesses(pressure, diameter, height, density, yield_stress, joint_efficiency):
    # Cylindrical Shell Thickness
    shell_thickness = (pressure * diameter) / (2 * yield_stress * joint_efficiency - pressure)
    
    # Spherical Roof Thickness
    spherical_roof_thickness = (pressure * diameter) / (4 * yield_stress * joint_efficiency - pressure)
    
    # Conical Roof Thickness (assuming 45° angle for the cone)
    conical_roof_thickness = (pressure * diameter) / (4 * yield_stress * joint_efficiency * math.sin(math.radians(45)))
    
    # Flat Base Thickness
    area = math.pi * (diameter / 2) ** 2
    flat_base_thickness = math.sqrt((3 * density * height * area**2) / (4 * yield_stress * joint_efficiency))
    
    return shell_thickness, spherical_roof_thickness, conical_roof_thickness, flat_base_thickness

# Streamlit UI
st.title("🛢️ Hydrogen Peroxide Storage Tank Recommendation System")

# Step 1: Select Use Case
st.header("Step 1: Select Your Industry Use Case")
industry = st.selectbox("Select the industry", list(use_cases.keys()))

# Step 2: Input Production Rate, Buffer Storage, and Yield Stress
st.header("Step 2: Input Production, Buffer Storage, and Material Properties")
production_rate = st.number_input("Enter the daily production rate (in tons)", min_value=1, step=1, value=10)
buffer_days = st.number_input("Enter the buffer storage duration (in days)", min_value=1, step=1, value=7)
yield_stress = st.number_input("Enter the yield stress of the material (in Pascals)", min_value=1e6, step=1e6, value=150e6, format="%.0f")

# Step 3: Display Recommendations
if st.button("Get Tank Recommendations"):
    concentration = use_cases[industry]["concentration"]
    density = use_cases[industry]["density"]
    material = use_cases[industry]["material"]
    color = use_cases[industry]["color"]
    
    volume = calculate_tank_volume(production_rate, buffer_days, density)
    height, diameter = calculate_height_diameter(volume)
    pressure = calculate_pressure(density, height)
    shell_thickness, spherical_roof_thickness, conical_roof_thickness, flat_base_thickness = calculate_thicknesses(
        pressure, diameter, height, density, yield_stress, 0.85)
    
    st.subheader("🔍 Recommended Storage Tank Parameters")
    st.write(f"**Industry Use Case:** {industry}")
    st.write(f"**H₂O₂ Concentration:** {concentration}%")
    st.write(f"**Material:** {material}")
    st.write(f"**Color:** {color}")
    st.write(f"**Required Tank Volume:** {volume:.2f} cubic meters")
    st.write(f"**Calculated Tank Height:** {height:.2f} meters")
    st.write(f"**Calculated Tank Diameter:** {diameter:.2f} meters")
    st.write(f"**Calculated Internal Pressure:** {pressure:.2f} Pascals")
    
    # Display thicknesses
    st.subheader("🛠️ Calculated Tank Wall Thicknesses")
    st.write(f"**Cylindrical Shell Thickness:** {shell_thickness:.4f} meters")
    st.write(f"**Spherical Roof Thickness:** {spherical_roof_thickness:.4f} meters")
    st.write(f"**Conical Roof Thickness:** {conical_roof_thickness:.4f} meters")
    st.write(f"**Flat Base Thickness:** {flat_base_thickness:.4f} meters")

# Footer
st.markdown("<hr style='border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.9em;'>
        Designed with ❤️ 
    </div>
""", unsafe_allow_html=True)
