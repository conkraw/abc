import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Initialize Firebase
def initialize_firebase():
    global FIREBASE_COLLECTION_NAME  # Use the global variable
    FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')
    FIREBASE_COLLECTION_NAME = os.getenv('FIREBASE_COLLECTION_NAME')
    
    if FIREBASE_KEY_JSON is None:
        raise ValueError("FIREBASE_KEY environment variable not set.")

    try:
        firebase_credentials = json.loads(FIREBASE_KEY_JSON)

        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        return firestore.client()
    except Exception as e:
        raise Exception(f"Error initializing Firebase: {e}")

db = initialize_firebase()

# Function to load the age to ETT mapping from the text file
def load_age_to_ett_mapping(filename):
    with open(filename, 'r') as file:
        content = file.read()
    # Safely evaluate the content to get the dictionary
    return eval(content)

# Load the mapping
age_to_ett_mapping = load_age_to_ett_mapping('age_to_ett_mapping.txt')

# Function to fill the Word template with form inputs
def fill_word_template(template_path, data):
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if f'{{{{{key}}}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{{{key}}}}}', str(value))
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Initialize session state
if 'section' not in st.session_state:
    st.session_state.section = 0
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Navigation function
def next_section():
    st.session_state.section += 1
    save_data()

def prev_section():
    st.session_state.section -= 1

def save_data():
    # Save current section data to Firestore
    data = {key: st.session_state.form_data.get(key, '') for key in st.session_state.form_data.keys()}
    db.collection('airway_checklists').add(data)

# Front Page Completed Section
if st.session_state.section == 0:
    st.title("Front Page Completed")
    
    front_page_completed = st.selectbox(
        "Select when the front page was completed",
        ['On admission', 'During rounds', 'After rounds', 'Just prior to intubation', 'After intubation', 'Prior to extubation'],
        key="front_page_completed"
    )
    
    completed_by = st.text_input("Who completed the form? (Name or Role)", key="completed_by")

    if st.button("Next", key="next_button_0"):
        next_section()

# Patient Information Section
elif st.session_state.section == 1:
    st.title("Patient Information")

    cols = st.columns(2)

    with cols[0]:
        date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today(), key="date")
        age = st.selectbox("Select Patient Age", list(age_to_ett_mapping.keys()), key="age_select")

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time(), key="time")
        weight_str = st.text_input("Enter Patient Weight (Kilograms)", value="", key="weight")
        
        if weight_str and not weight_str.replace('.', '', 1).isdigit():
            st.error("Please enter a valid number for the weight (e.g., 12.5 or 12).")

    if st.button("Next", key="next_button_1"):
        next_section()
    if st.button("Previous", key="prev_button_1"):
        prev_section()

# Intubation Risk Assessment Section
elif st.session_state.section == 2:
    st.title("Intubation Risk Assessment")

    risk_assessment = st.text_area("Intubation Risk Assessment Details", key="risk_assessment")

    if st.button("Submit", key="submit_button"):
        save_data()
        st.success("Form submitted successfully!")
    if st.button("Previous", key="prev_button_2"):
        prev_section()

# Display navigation
if st.session_state.section > 0:
    st.button("Previous", key="prev_button", on_click=prev_section)

