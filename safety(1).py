import streamlit as st
import time
import random


def get_sensor_data():
    temperature = round(random.uniform(10, 50), 2) 
    pressure = round(random.uniform(0.5, 2.5), 2)  
    h2o2_concentration = round(random.uniform(20, 60), 2)  
    return temperature, pressure, h2o2_concentration


def check_safety(temperature, pressure, h2o2_concentration):
    if temperature > 30:
        st.warning(f"High Temperature Alert! Current Temperature: {temperature}°C")
    if pressure > 2.0:
        st.warning(f"High Pressure Alert! Current Pressure: {pressure} atm")
    if h2o2_concentration > 50:
        st.warning(f"High H₂O₂ Concentration Alert! Current Concentration: {h2o2_concentration}%")
    if temperature <= 30 and pressure <= 2.0 and h2o2_concentration <= 50:
        st.success("All systems are within safe limits.")

st.title("Hydrogen Peroxide Storage Tank Safety System")

st.write(f"Current Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")


temperature, pressure, h2o2_concentration = get_sensor_data()

st.subheader("Current Sensor Readings:")
st.write(f"Temperature: {temperature}°C")
st.write(f"Pressure: {pressure} atm")
st.write(f"H₂O₂ Concentration: {h2o2_concentration}%")


check_safety(temperature, pressure, h2o2_concentration)


if st.button('Refresh Readings'):
    st.experimental_rerun()
