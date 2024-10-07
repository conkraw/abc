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

def reset_input(default_value, key):
    if key not in st.session_state:
        st.session_state[key] = default_value
    
    current_value = st.text_input("", key=key, value=st.session_state[key])
    
    if current_value != st.session_state[key]:
        st.session_state[key] = current_value
    
    return current_value

st.title("Airway Bundle Checklist")

# Section 1: Front Page Completed
with st.form("front_page"):
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
    
    if st.form_submit_button("Submit Front Page"):
        st.session_state['front_page_data'] = {
            "front_page_completed": front_page_completed,
            "completed_by": completed_by,
            "room_number": room_number
        }
        st.success("Front page submitted successfully!")

# Section 2: Patient Information
with st.form("patient_info"):
    st.markdown(box_section("Patient Information"), unsafe_allow_html=True)
    
    cols = st.columns(2)

    with cols[0]:
        date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())
        age_options = [f"{i} year old" for i in range(1, 19)] + ["Premature", "Newborn"]
        age = st.selectbox("Select Patient Age", age_options, key="age")

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())
        weight_str = st.text_input("Enter Patient Weight (Kilograms)", value="")
    
    if st.form_submit_button("Submit Patient Information"):
        st.session_state['patient_info_data'] = {
            "date": date,
            "time": time,
            "weight": weight_str,
            "age": age
        }
        st.success("Patient information submitted successfully!")

# Section 3: Intubation Risk Assessment
with st.form("risk_assessment"):
    st.markdown(box_section("Intubation Risk Assessment"), unsafe_allow_html=True)

    difficult_airway_history = st.selectbox("History of difficult airway?", ['YES', 'NO'], key="difficult_airway_history")
    physical_risk = st.selectbox("Physical risk factors?", ['YES', 'NO'], key="physical_risk")
    
    if st.form_submit_button("Submit Intubation Risk Assessment"):
        st.session_state['risk_assessment_data'] = {
            "difficult_airway_history": difficult_airway_history,
            "physical_risk": physical_risk
        }
        st.success("Risk assessment submitted successfully!")

# Section 4: Intubation Plan
with st.form("intubation_plan"):
    st.markdown(box_section("Intubation Plan"), unsafe_allow_html=True)

    who_intubate = st.multiselect("Who will intubate?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other'],
                                   key="who_intubate")

    when_intubate = st.multiselect(
        "When will we intubate? (Describe timing of airway management):",
        ['Prior to procedure', 'Mental Status Changes', 
         'Hypoxemia Refractory to CPAP', 'Ventilation failure refractory to NIV', 
         'Loss of Airway Protection', 'Other'],
        key="when_intubate"
    )
    
    if "Hypoxemia Refractory to CPAP" in when_intubate:
        spo2_input = st.text_input("SPO2 Less Than?:", key="spo2_input")
    
    if st.form_submit_button("Submit Intubation Plan"):
        st.session_state['intubation_plan_data'] = {
            "who_intubate": who_intubate,
            "when_intubate": when_intubate,
            "spo2_input": spo2_input
        }
        st.success("Intubation plan submitted successfully!")

# Final Submission
if st.button("Final Submit"):
    # Aggregate all data for final submission
    final_data = {
        **st.session_state.get('front_page_data', {}),
        **st.session_state.get('patient_info_data', {}),
        **st.session_state.get('risk_assessment_data', {}),
        **st.session_state.get('intubation_plan_data', {})
    }
    
    # Path to the provided Word template
    template_path = 'AirwayBundleChecklist_7-2020.docx'
    
    # Fill the Word template with final data
    filled_doc = fill_word_template(template_path, final_data)
    
    st.success("All sections submitted successfully!")
    st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")



