import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def reset_input(default_value, key):
    # If the key does not exist in session state, initialize it with the default value
    if key not in st.session_state:
        st.session_state[key] = default_value  # Set the default value only once

    # Display the text input without a default value, since it is already handled by session state
    current_value = st.text_input("", key=key)

    # If the current input differs from the session state, update the session state
    if current_value != st.session_state[key]:
        st.session_state[key] = current_value

    return current_value


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

    room_number = st.selectbox(
        "Select Room Number",
        ['4102', '4104', '4106', '4108', '4110', '4112', '4114', '4116', '4201', '4203', '4209', 
         '4211', '4213', '4215', '4217', '4219', '4221', '4223'],
        key="room_number"
    )
    
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

    st.write("#### Difficult Airway:")
    
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("History of difficult airway?")
    
    with cols[1]:
        difficult_airway_history = st.selectbox(
            label="",  
            options=['','YES', 'NO'],
            key="difficult_airway_history"
        )

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
    if st.button("Next", key="next_button_2"):
        next_section()
      
    if st.button("Previous", key="prev_button_2"):
        prev_section()
        
elif st.session_state.section == 3:
    st.title("Intubation Plan")

    # Multi-select for "Who will intubate?" and "Who will bag-mask?"
    who_intubate = st.multiselect("Who will intubate?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other'],
                                   key="who_intubate")

    who_bag_mask = st.multiselect("Who will bag-mask?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'RT', 'Other'],
                                   key="who_bag_mask")

    # Create a layout for intubation method
    intubation_method = st.selectbox("How will we intubate? (Method)", ["","Oral", "Nasal"], key="intubation_method")

    # Create a layout for ETT Type and ETT Size
    cols = st.columns(2)

    with cols[0]:
        ett_type = st.selectbox("ETT Type", ["", "Cuffed", "Uncuffed"], key="ett_type")

    with cols[1]:
        # Initialize 'ett_size' in session_state if it's not already set
        if 'ett_size' not in st.session_state:
            st.session_state['ett_size'] = ''  # Default value for ETT size
    
        ett_size = st.selectbox(
        "Select ETT Size",
        options=['','3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'],
        key="ett_size",
        index=['','3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'].index(st.session_state['ett_size'])
    )
        if ett_size != st.session_state['ett_size']:
            st.session_state['ett_size'] = ett_size

    st.write("Device:")
    
    cols = st.columns(3)

    # Column 1: Dropdowns for "X" or empty
    with cols[0]:
        # Dropdowns to choose if devices are selected or not (X = selected)
        device_1_selection = st.selectbox("Select Device", options=["", "X"], key="dropdown_1")
        device_2_selection = st.selectbox("Select Device", options=["", "X"], key="dropdown_2")
        device_3_selection = st.selectbox("Select Device", options=["", "X"], key="dropdown_3")
        device_4_selection = st.selectbox("Select Device", options=["", "X"], key="dropdown_4")
    
    # Column 2: Editable text inputs (reverts to the original value after the user moves away)
    with cols[1]:
        # These text inputs will reset to their default value if changed and the user moves away
        device_1_text = reset_input("Laryngoscope", key="laryngoscope_textx")
        device_2_text = reset_input("Glidescope", key="glidescope_textx")
        device_3_text = reset_input("LMA", key="lma_textx")
        device_4_text = reset_input("Other Device", key="other_device_textx")
    
    # Column 3: Additional details for each device (uneditable placeholders)
    with cols[2]:
        # Text Inputs with uneditable placeholders (details of each device)
        st.text_input("Laryngoscope details:", key="laryngoscope_details", disabled=False)
        st.text_input("Glidescope details:", key="glidescope_details", disabled=False)
        st.text_input("LMA details:", key="lma_details", disabled=False)
        st.text_input("Other Device details:", key="other_device_details", disabled=False)

    st.write("Blade:")
    
    cols = st.columns(3)

    # Column 1: Dropdowns for "X" or empty
    with cols[0]:
        # Dropdowns to choose if devices are selected or not (X = selected)
        blade_1_selection = st.selectbox("Select Device", options=["", "X"], key="dropdown_5")
        blade_2_selection = st.selectbox("Select Device", options=["", "X"], key="dropdown_6")
        blade_3_selection = st.selectbox("Select Device", options=["", "X"], key="dropdown_7")
    
    # Column 2: Editable text inputs (reverts to the original value after the user moves away)
    with cols[1]:
        # These text inputs will reset to their default value if changed and the user moves away
        blade_1_text = reset_input("Mac", key="macx")
        blade_2_text = reset_input("Miller", key="millerx")
        blade_3_text = reset_input("Wis-Hipple", key="wis_hipplex")
    
    # Column 3: Additional details for each device (uneditable placeholders)
    with cols[2]:
        # Text Inputs with uneditable placeholders (details of each device)
        st.text_input("Mac Details:", key="mac_details", disabled=False)
        st.text_input("Miller Details:", key="miller_details", disabled=False)
        st.text_input("Wis-Hipple Details:", key="wis_hipple_details", disabled=False)
    
    st.write("Medications:")
    
    cols = st.columns(3)

    # Column 1: Dropdowns for "X" or empty
    with cols[0]:
        # Dropdowns to choose if devices are selected or not (X = selected)
        med_1_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_8")
        med_2_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_9")
        med_3_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_10")
        med_4_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_11")
        med_5_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_12")
        med_6_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_13")
        med_7_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_14")
        med_8_selection = st.selectbox("Select Medication", options=["", "X"], key="dropdown_15")
    
    # Column 2: Editable text inputs (reverts to the original value after the user moves away)
    with cols[1]:
        # These text inputs will reset to their default value if changed and the user moves away
        med_1_text = reset_input("Atropine", key="atropinex")
        med_2_text = reset_input("Glycopyrrolate", key="glycox")
        med_3_text = reset_input("Fentanyl", key="fentanylx")
        med_4_text = reset_input("Midazolam", key="midazolamx")
        med_5_text = reset_input("Ketamine", key="ketaminex")
        med_6_text = reset_input("Propofol", key="propofolx")
        med_7_text = reset_input("Rocuronium", key="rocx")
        med_8_text = reset_input("Vecuronium", key="vecx")

    # Column 3: Additional details for each device (uneditable placeholders)
    with cols[2]:
        # Text Inputs with uneditable placeholders (details of each device)
        st.text_input("Atropine Dosage:", key="atropine_dosage", disabled=False)
        st.text_input("Glycopyrrolate Dosage:", key="glyco_dosage", disabled=False)
        st.text_input("Fentanyl Dosage:", key="fentanyl_dosage", disabled=False)
        st.text_input("Midazolam Dosage:", key="midazolam_dosage", disabled=False)
        st.text_input("Ketamine Dosage:", key="ketamine_dosage", disabled=False)
        st.text_input("Propofol Dosage:", key="propofol_dosage", disabled=False)
        st.text_input("Rocuronium Dosage:", key="roc_dosage", disabled=False)
        st.text_input("Vecuronium Dosage:", key="vec_dosage", disabled=False)

    st.write("Apneic Oxygenation:")
    
    cols = st.columns(3)

    # Column 1: Dropdowns for "X" or empty
    with cols[0]:
        # Dropdowns to choose if devices are selected or not (X = selected)
        ao_selection = st.selectbox("Select Use", options=["", "Yes", "No"], key="dropdown_16")
    
    # Column 2: Editable text inputs (reverts to the original value after the user moves away)
    with cols[1]:
        # These text inputs will reset to their default value if changed and the user moves away
        ao_text = reset_input("Apneic Oxygenation", key="aox")
    
    # Column 3: Additional details for each device (uneditable placeholders)
    with cols[2]:
        # Text Inputs with uneditable placeholders (details of each device)
        st.text_input("Apneic Oxygenation Details:", key="ao_details", disabled=False)

    other_planning = st.text_input("Other Intubation Planning Details:", key="other_planning")
    

    # Your existing markdown for the section
    st.markdown(box_section("Timing of Intubation"), unsafe_allow_html=True)

    # Multi-select for timing of intubation
    when_intubate = st.multiselect(
        "When will we intubate? (Describe timing of airway management):",
        ['Prior to procedure', 'Mental Status Changes', 
         'Hypoxemia Refractory to CPAP', 'Ventilation failure refractory to NIV', 
         'Loss of Airway Protection', 'Other'],
        key="when_intubate"
    )
    
    # Check if "Hypoxemia Refractory to CPAP" is selected
    if "Hypoxemia Refractory to CPAP" in when_intubate:
        spo2_input = st.text_input("SPO2 Less Than?:", key="spo2_input")
    
    
    st.markdown(box_section("Backup"), unsafe_allow_html=True)
    advance_airway_provider = st.multiselect("Advance Airway Provider:", 
                                   ['Attending','Anesthesia','ENT','Fellow','Other'],
                                   key="advance_airway_provider")

    advance_airway_provider = st.multiselect("Difficult Airway Procedure:", 
                                   ['Difficult Airway Cart','Difficult Airway Emergency Page', 'Other'],
                                   key="difficult_airway")

    if st.button("Next", key="next_button_3"):
        next_section()
    if st.button("Previous", key="prev_button_3"):
        prev_section()
        
# Display navigation
#if st.session_state.section > 0:
#    st.button("Previous", key="prev_button", on_click=prev_section)

