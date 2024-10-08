import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime

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

# Function to create a boxed section
def box_section(title):
    return f"""
    <div style="border: 1px solid #0072B8; border-radius: 5px; padding: 10px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #0072B8;">{title}</h4>
    </div>
    """

def reset_input(default_value, key):
    if key not in st.session_state:
        st.session_state[key] = default_value
    current_value = st.text_input("", key=key)
    if current_value != st.session_state[key]:
        st.session_state[key] = current_value
    return current_value

st.title("Airway Bundle Checklist")

def update_ett_size_based_on_age():
    selected_age = st.session_state.get("age_select")
    if selected_age:
        st.session_state['ett_size'] = age_to_ett_mapping.get(selected_age, '4.0')

# Create a form
with st.form("airway_form"):
    st.markdown(box_section("Front Page Completed"), unsafe_allow_html=True)
    front_page_completed = st.selectbox(
        "Select when the front page was completed",
        ['On admission', 'During rounds', 'After rounds', 'Just prior to intubation', 'After intubation', 'Prior to extubation'],
        key="front_page_completed"
    )

    completed_by = st.text_input("Who completed the form? (Name or Role)")

    room_number = st.selectbox(
        "Select Room Number",
        ['4102', '4104', '4106', '4108', '4110', '4112', '4114', '4116', '4201', '4203', '4209', 
         '4211', '4213', '4215', '4217', '4219', '4221', '4223'],
        key="room_number"
    )

    st.markdown(box_section("Patient Information"), unsafe_allow_html=True)
    
    cols = st.columns(2)

    with cols[0]:
        date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())
        age = st.selectbox("Select Patient Age", list(age_to_ett_mapping.keys()), key="age_select")
        update_ett_size_based_on_age()  # Update ETT size based on selected age

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())
        weight_str = st.text_input("Enter Patient Weight (Kilograms)", value="")
        if weight_str and not weight_str.replace('.', '', 1).isdigit():
            st.error("Please enter a valid number for the weight (e.g., 12.5 or 12).")

    st.markdown(box_section("Intubation Risk Assessment"), unsafe_allow_html=True)

    # Difficult airway assessment
    st.write("#### Difficult Airway:")
    cols = st.columns([4, 1])
    with cols[0]:
        st.write("History of difficult airway?")
    with cols[1]:
        difficult_airway_history = st.selectbox("", ['YES', 'NO'], key="difficult_airway_history")

    cols = st.columns([4, 1])
    with cols[0]:
        st.write("Physical risk factors (small mouth, small jaw, etc.)?")
    with cols[1]:
        physical_risk = st.selectbox("", ['YES', 'NO'], key="physical_risk")

    # Additional risk assessments...

    st.markdown(box_section("Intubation Plan"), unsafe_allow_html=True)

    who_intubate = st.multiselect("Who will intubate?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other'],
                                   key="who_intubate")

    who_bag_mask = st.multiselect("Who will bag-mask?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'RT', 'Other'],
                                   key="who_bag_mask")

    intubation_method = st.selectbox("How will we intubate? (Method)", ["Oral", "Nasal"], key="intubation_method")

    cols = st.columns(2)
    with cols[0]:
        ett_type = st.selectbox("ETT Type", ["", "Cuffed", "Uncuffed"], key="ett_type")
    with cols[1]:
        # Initialize 'ett_size' in session_state if it's not already set
        if 'ett_size' not in st.session_state:
            st.session_state['ett_size'] = age_to_ett_mapping.get(age, '')

        ett_size = st.selectbox(
            "Select ETT Size",
            options=['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'],
            key="ett_size",
            index=['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'].index(st.session_state['ett_size'])
        )

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
    # Submit button
    submit = st.form_submit_button("Submit")

    # Process submission
if submit:
    # Store form data into a dictionary to replace placeholders
    form_data = {
        "date": date,
        "time": time,
        "weight": weight_str,  # Save the weight as the string (allowing decimal numbers if entered)
        "age": age,
        "ett_type": ett_type,
        "who_intubate": ", ".join(who_intubate),
        "who_bag_mask": ", ".join(who_bag_mask),
        "ett_size": ett_size,
        "intubation_timing": intubation_timing,
        "front_page_completed": front_page_completed,
        "completed_by": completed_by,
        "room_number": room_number,
        "difficult_airway_history": difficult_airway_history,
        "physical_risk": physical_risk,
        "high_risk_desaturation": high_risk_desaturation,
        "high_risk_ICP": high_risk_ICP,
        "unstable_hemodynamics": unstable_hemodynamics,
        "other_risk_factors": other_risk_factors,
        "other_risk_yes_no": other_risk_yes_no,
        "laryngoscope": laryngoscope,  # Checkbox value
        "laryngoscope_text": laryngoscope_text,  # Text input value
        "lma": lma,                    # Checkbox value
        "lma_text": lma_text,          # Text input value
        "glidescope": glidescope,      # Checkbox value
        "glidescope_text": glidescope_text,  # Text input value
        "other_device": other_device,  # Checkbox value
        "other_device_text": other_device_text,  
        "laryngoscope_textx": laryngoscope_text,  # Text input value
        "lma_textx": lma_text,          # Text input value
        "glidescope_textx": glidescope_text,  # Text input value
        "other_device_textx": other_device_text,  
                    "ett_type": ett_type,
            "ett_size": st.session_state['ett_size'],  # Use dynamically set ETT size
            "who_intubate": ", ".join(who_intubate),
            "who_bag_mask": ", ".join(who_bag_mask),
    }

    # Path to the provided Word template
    template_path = 'AirwayBundleChecklist_7-2020.docx'

    # Fill the Word template with form data
    filled_doc = fill_word_template(template_path, form_data)

    # Now you can save, display, or process the filled_doc


    # Path to the provided Word template
    template_path = 'AirwayBundleChecklist_7-2020.docx'

    # Fill the Word template with form data
    filled_doc = fill_word_template(template_path, form_data)
        
    # Provide download link for the filled Word document
    st.success("Form submitted successfully!")
    st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")

