import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime

# Age to ETT size mapping
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

def update_ett_size_based_on_age():
    selected_age = st.session_state.get("age_select")
    if selected_age:
        st.session_state['ett_size'] = age_to_ett_mapping.get(selected_age, '4.0')  # Use age_to_ett_mapping

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
        age = st.selectbox("Select Patient Age", list(age_to_ett_mapping.keys()), key="age_select")

        # Update the ETT size when the age is selected
        update_ett_size_based_on_age()
        
    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())

        # Weight input with text input validation
        weight_str = st.text_input("Enter Patient Weight (Kilograms)", value="")

        # Validate the weight input
        if weight_str and not validate_weight(weight_str):
            st.error("Please enter a valid number for the weight (e.g., 12.5 or 12).")

    # ETT Size Section: Use session state value dynamically
    st.markdown("### ETT Size Based on Age")
    ett_size = st.selectbox(
        "Select ETT Size",
        options=['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'],
        key="ett_size",
        index=['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'].index(st.session_state['ett_size']) if st.session_state['ett_size'] else 0
    )

    # Intubation Risk Assessment Section
    st.markdown(box_section("Intubation Risk Assessment"), unsafe_allow_html=True)
    # More sections here...

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
        "ett_size": ett_size,
        "who_intubate": ", ".join(who_intubate),
        "who_bag_mask": ", ".join(who_bag_mask),
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
        "laryngoscope": laryngoscope,
        "laryngoscope_text": laryngoscope_text,
        "lma": lma,
        "lma_text": lma_text,
        "glidescope": glidescope,
        "glidescope_text": glidescope_text,
        "other_device": other_device,
        "other_device_text": other_device_text,
        "laryngoscope_textx": laryngoscope_text,
        "lma_textx": lma_text,
        "glidescope_textx": glidescope_text,
        "other_device_textx": other_device_text
    }

    # Path to the provided Word template
    template_path = 'AirwayBundleChecklist_7-2020.docx'

    # Fill the Word template with form data
    filled_doc = fill_word_template(template_path, form_data)

    # Provide download link for the filled Word document
    st.success("Form submitted successfully!")
    st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")


