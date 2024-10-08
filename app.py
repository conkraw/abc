import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def reset_input(default_value, key):
    if key not in st.session_state:
        st.session_state[key] = default_value
    current_value = st.text_input("", key=key)
    if current_value != st.session_state[key]:
        st.session_state[key] = current_value
    return current_value

def initialize_firebase():
    global FIREBASE_COLLECTION_NAME
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

def load_age_to_ett_mapping(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return eval(content)

age_to_ett_mapping = load_age_to_ett_mapping('age_to_ett_mapping.txt')

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

if 'section' not in st.session_state:
    st.session_state.section = 0
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

def next_section():
    if st.session_state.section < 5:
        st.session_state.section += 1
        save_data()

def prev_section():
    if st.session_state.section > 0:
        st.session_state.section -= 1

def save_data():
    data = {key: st.session_state.form_data.get(key, '') for key in st.session_state.form_data.keys()}
    db.collection('airway_checklists').add(data)

# Front Page Completed Section
if st.session_state.section == 0:
    st.title("Front Page Completed")
    front_page_completed = st.selectbox("Select when the front page was completed",
                                         ['','On admission', 'During rounds', 'After rounds', 
                                          'Just prior to intubation', 'After intubation', 
                                          'Prior to extubation'], key="front_page_completed")
    
    completed_by = st.text_input("Who completed the form? (Name or Role)", key="completed_by")
    room_number = st.selectbox("Select Room Number", 
                                ['','4102', '4104', '4106', '4108', '4110', 
                                 '4112', '4114', '4116', '4201', '4203', 
                                 '4209', '4211', '4213', '4215', '4217', 
                                 '4219', '4221', '4223'], key="room_number")
    
    if st.button("Next", on_click=next_section):
        pass

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

    # Single Next and Previous Buttons
    if st.button("Next", on_click=next_section):
        pass
    if st.button("Previous", on_click=prev_section):
        pass

# Intubation Risk Assessment Section
elif st.session_state.section == 2:
    st.title("Intubation Risk Assessment")
    st.write("#### Difficult Airway:")
    
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("History of difficult airway?")
    with cols[1]:
        difficult_airway_history = st.selectbox("", options=['', 'YES', 'NO'], key="difficult_airway_history")


    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Physical (e.g. small mouth, small jaw, large tongue, or short neck)?")
    
    with cols[1]:
        physical_risk = st.selectbox(
            label="",  
            options=['','YES', 'NO'],
            key="physical_risk"
        )

    st.write("#### At Risk For:")
    
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("High risk for rapid desaturation during intubation?")
    
    with cols[1]:
        high_risk_desaturation = st.selectbox(
            label="",  
            options=['','YES', 'NO'],
            key="high_risk_desaturation"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Increased ICP, pulmonary hypertension, need to avoid hypercarbia?")
    
    with cols[1]:
        high_risk_ICP = st.selectbox(
            label="",  
            options=['','YES', 'NO'],
            key="high_risk_ICP"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Unstable hemodynamics (e.g., hypovolemia, potential need for fluid bolus, vasopressor, CPR)?")
    
    with cols[1]:
        unstable_hemodynamics = st.selectbox(
            label="",  
            options=['','YES', 'NO'],
            key="unstable_hemodynamics"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Is there another risk factor?")
    
    with cols[1]:
        other_risk_yes_no = st.selectbox(
            label="",  
            options=['','YES', 'NO'],
            key="other_risk_yes_no"
        )
        # Single Next and Previous Buttons
    if st.button("Next", on_click=next_section):
        pass
    if st.button("Previous", on_click=prev_section):
        pass

# Intubation Plan Section
elif st.session_state.section == 3:
    st.title("Intubation Plan")
    who_intubate = st.multiselect("Who will intubate?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending'],
                                   key="who_intubate")
    # Other inputs...

    # Single Next and Previous Buttons
    if st.button("Next", on_click=next_section):
        pass
    if st.button("Previous", on_click=prev_section):
        pass

# Timing of Intubation Section
elif st.session_state.section == 4:
    st.title("Timing of Intubation")
    when_intubate = st.multiselect(
        "When will we intubate? (Describe timing of airway management):",
        ['Prior to procedure', 'Mental Status Changes', 
         'Hypoxemia Refractory to CPAP', 'Ventilation failure refractory to NIV', 
         'Loss of Airway Protection', 'Other'],
        key="when_intubate"
    )

    # Single Next and Previous Buttons
    if st.button("Next", on_click=next_section):
        pass
    if st.button("Previous", on_click=prev_section):
        pass

elif st.session_state.section == 5:
    st.title("Backup")

    # Multi-select for Advance Airway Provider
    advance_airway_provider = st.multiselect("Advance Airway Provider:", 
                                   ['Attending', 'Anesthesia', 'ENT', 'Fellow', 'Other'],
                                   key="advance_airway_provider")

    # You can add other inputs here...

    # Single Submit and Previous Buttons
    if st.button("Submit", key="submit_button"):
        # Prepare the final data for submission
        final_data = {key: st.session_state.form_data.get(key, '') for key in st.session_state.form_data.keys()}
        
        # Include the data from this section
        final_data['advance_airway_provider'] = advance_airway_provider
        
        # Submit data to Firestore
        db.collection('airway_checklists').add(final_data)
        
        st.success("Data submitted successfully!")
        
        # Optionally reset the form or redirect
        st.session_state.section = 0  # Reset to the first section if needed
        st.session_state.form_data = {}  # Clear form data

    if st.button("Previous", on_click=prev_section):
        pass
