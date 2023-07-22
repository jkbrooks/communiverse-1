import streamlit as st
from dialogue_simulator import DialogueSimulator

# Create a Dialogue Simulator
simulator = DialogueSimulator()

# Start the conversation
simulator.start_conversation()

# Display the conversation
st.write(simulator.get_conversation())
