import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime

# Function to fill the Word template with form inputs
def fill_word_template(template_path, data):
    doc = Document(template_path)

    # Replace placeholders in the document with form data
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if f'{{{{{key}}}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{{{key}}}}}', str(value))

    # Save the updated document in memory
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

# Streamlit form for the Airway Bundle Checklist
st.title("Airway Bundle Checklist")

# Create a form
with st.form("airway_form"):
    # Front Page Section
    st.markdown(box_section("Front Page Completed"), unsafe_allow_html=True)
    front_page_completed = st.selectbox(
        "Select when the front page was completed",
        ['On admission', 'During rounds', 'After rounds', 'Just prior to intubation', 'After intubation', 'Prior to extubation'],
        key="front_page_completed"
    )

    # Person who completed the form
    completed_by = st.text_input("Who completed the form? (Name or Role)")

    # Room Number selection
    room_number = st.selectbox(
        "Select Room Number",
        ['4102', '4104', '4106', '4108', '4110', '4112', '4114', '4116', '4201', '4203', '4209', 
         '4211', '4213', '4215', '4217', '4219', '4221', '4223'],
        key="room_number"
    )

    # Patient Information Section
    st.markdown(box_section("Patient Information"), unsafe_allow_html=True)
    
    cols = st.columns(2)

    with cols[0]:
        date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())

        # Replace number input with dropdown for age
        age_options = [
            "Premature", "Newborn", "1 month old", "2 month old", "3 month old", "4 month old", "5 month old", 
            "6 month old", "7 month old", "8 month old", "9 month old", "10 month old", "11 month old", 
            "12 month old", "1 year old", "2 year old", "3 year old", "4 year old", "5 year old", 
            "6 year old", "7 year old", "8 year old", "9 year old", "10 year old", "11 year old", 
            "12 year old", "13 year old", "14 year old", "15 year old", "16 year old", "17 year old", 
            "18 year old"
        ]
        age = st.selectbox("Select Patient Age", age_options, key="age")

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())

        # Weight input with text input validation
        weight_str = st.text_input("Enter Patient Weight (Kilograms)", value="")

        # Validate the weight input
        if weight_str and not validate_weight(weight_str):
            st.error("Please enter a valid number for the weight (e.g., 12.5 or 12).")

    # Intubation Risk Assessment Section
    st.markdown(box_section("Intubation Risk Assessment"), unsafe_allow_html=True)

    # Create a table-like layout with YES/NO dropdowns in the same row using st.columns
    st.write("#### Difficult Airway:")
    
    cols = st.columns([4, 1])  # Adjust column widths (make dropdown narrower)
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("History of difficult airway?")
    
    with cols[1]:
        difficult_airway_history = st.selectbox(
            label="",  # Set label to empty string
            options=['YES', 'NO'],
            key="difficult_airway_history"
        )

    cols = st.columns([4, 1])  # Reset columns for next question
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Physical (e.g. small mouth, small jaw, large tongue, or short neck)?")
    
    with cols[1]:
        physical_risk = st.selectbox(
            label="",  # Set label to empty string
            options=['YES', 'NO'],
            key="physical_risk"
        )

    st.write("#### At Risk For:")
    
    cols = st.columns([4, 1])  # Adjust column widths (make dropdown narrower)
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("High risk for rapid desaturation during intubation?")
    
    with cols[1]:
        high_risk_desaturation = st.selectbox(
            label="",  # Set label to empty string
            options=['YES', 'NO'],
            key="high_risk_desaturation"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Increased ICP, pulmonary hypertension, need to avoid hypercarbia?")
    
    with cols[1]:
        high_risk_ICP = st.selectbox(
            label="",  # Set label to empty string
            options=['YES', 'NO'],
            key="high_risk_ICP"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Unstable hemodynamics (e.g., hypovolemia, potential need for fluid bolus, vasopressor, CPR)?")
    
    with cols[1]:
        unstable_hemodynamics = st.selectbox(
            label="",  # Set label to empty string
            options=['YES', 'NO'],
            key="unstable_hemodynamics"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Other risk factors?")
    
    with cols[1]:
        other_risk_factors = st.text_input(
            "",
            key="other_risk_factors"
        )

    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("")
        st.markdown("")
        st.write("Is there another risk factor?")
    
    with cols[1]:
        other_risk_yes_no = st.selectbox(
            label="",  # Set label to empty string
            options=['YES', 'NO'],
            key="other_risk_yes_no"
        )

    # Intubation plan section
    st.markdown(box_section("Intubation Plan"), unsafe_allow_html=True)

    # Multi-select for "Who will intubate?" and "Who will bag-mask?"
    who_intubate = st.multiselect("Who will intubate?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other'],
                                   key="who_intubate")

    who_bag_mask = st.multiselect("Who will bag-mask?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'RT', 'Other'],
                                   key="who_bag_mask")

    # Create a layout for intubation method
    intubation_method = st.selectbox("How will we intubate? (Method)", ["Oral", "Nasal"], key="intubation_method")

    # Create a layout for ETT Type and ETT Size
    cols = st.columns(2)

    with cols[0]:
        ett_type = st.selectbox("ETT Type", ["", "Cuffed", "Uncuffed"], key="ett_type")

    with cols[1]:
        # ETT Size Selection
        ett_options = ['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0']
        ett_size = st.selectbox("ETT Size", ett_options, key="ett_size")
    
    st.write("Device:")
    
    # Create columns layout for checkboxes and text inputs to appear inline
    cols = st.columns([3, 1, 3, 1, 3, 1, 3, 1])  # Adjust column sizes
    
    # Laryngoscope
    with cols[0]:
        st.checkbox("Laryngoscope", key="laryngoscope")
    
    with cols[1]:
        st.text_input("", key="laryngoscope_text")
    
    # Glidescope
    with cols[2]:
        st.checkbox("Glidescope", key="glidescope")
    
    with cols[3]:
        st.text_input("", key="glidescope_text")
    
    # LMA
    with cols[4]:
        st.checkbox("LMA", key="lma")
    
    with cols[5]:
        st.text_input("", key="lma_text")
    
    # Other Device
    with cols[6]:
        st.checkbox("Other Device", key="other_device")
    
    with cols[7]:
        st.text_input("", key="other_device_text")

        
    # Timing of Intubation section
    st.markdown(box_section("Timing of Intubation"), unsafe_allow_html=True)
    intubation_timing = st.text_input("Describe timing of airway management", key="intubation_timing")

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
        "other_device_text": other_device_text  
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


