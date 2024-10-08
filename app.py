import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("path/to/your/firebase/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Mapping of age to ETT size
age_to_ett_mapping = {
    "": "",
    "Premature": "3.0",
    "Newborn": "3.5",
    "1 month old": "3.5",
    "2 month old": "3.5",
    "3 month old": "3.5",
    "4 month old": "3.5",
    "5 month old": "3.5",
    "6 month old": "4.0",
    "7 month old": "4.0",
    "8 month old": "4.0",
    "9 month old": "4.0",
    "10 month old": "4.0",
    "11 month old": "4.0",
    "1 year old": "4.5",
    "2 year old": "4.5",
    "3 year old": "4.5",
    "4 year old": "5.0",
    "5 year old": "5.0",
    "6 year old": "5.0",
    "7 year old": "6.0",
    "8 year old": "6.0",
    "9 year old": "6.0",
    "10 year old": "6.0",
    "11 year old": "6.5",
    "12 year old": "6.5",
    "13 year old": "6.5",
    "14 year old": "6.5",
    "15 year old": "6.5",
    "16 year old": "7.0",
    "17 year old": "7.0",
    "18 year old": "7.0"
}

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

    if st.button("Next"):
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

    if st.button("Next"):
        next_section()
    if st.button("Previous"):
        prev_section()

# Intubation Risk Assessment Section
elif st.session_state.section == 2:
    st.title("Intubation Risk Assessment")

    # Here you can add fields for the risk assessment
    risk_assessment = st.text_area("Intubation Risk Assessment Details", key="risk_assessment")

    if st.button("Submit"):
        save_data()
        st.success("Form submitted successfully!")
    if st.button("Previous"):
        prev_section()

# Display navigation
if st.session_state.section > 0:
    st.button("Previous", on_click=prev_section)


