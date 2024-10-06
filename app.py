import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime
from docx.shared import Pt

# Function to fill the Word template with form inputs
def fill_word_template(template_path, data):
    doc = Document(template_path)

    # Replace placeholders in the document with form data
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if f'{{{{{key}}}}}' in paragraph.text:  # Looks for {{key}} in the template
                paragraph.text = paragraph.text.replace(f'{{{{{key}}}}}', str(value))

    # Save the updated document in memory
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer

# Streamlit form for the Airway Bundle Checklist
st.title("Airway Bundle Checklist")

with st.form("airway_form"):
    # Patient Information
    st.subheader("Patient Information")
    date = st.date_input("Select Date", value=datetime.today())
    time = st.time_input("Select Time", value=datetime.now().time())
    weight = st.number_input("Enter Patient Weight (in kg)", min_value=0.0, format="%.2f")
    age = st.number_input("Enter Patient Age (in years)", min_value=0, max_value=120)

    st.subheader("Assessment for Anticipated Airway Management")
    difficult_airway = st.radio("History of difficult airway?", ('Yes', 'No'))
    physical_assessment = st.radio("Physical assessment (small mouth, large tongue, etc.)?", ('Yes', 'No'))
    high_risk_desaturation = st.radio("High risk for rapid desaturation during intubation?", ('Yes', 'No'))
    increased_icp = st.radio("Increased ICP/pulmonary hypertension?", ('Yes', 'No'))
    unstable_hemodynamics = st.radio("Unstable hemodynamics?", ('Yes', 'No'))
    other_risks = st.text_input("Other risk factors?")

    st.subheader("Intubation Plan")
    who_intubate = st.selectbox("Who will intubate?", ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other'])
    who_bag_mask = st.selectbox("Who will bag-mask?", ['Resident', 'Fellow', 'NP', 'Attending', 'RT', 'Other'])
    ett_size = st.selectbox("ETT Size", ['3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'])
    device = st.selectbox("Device", ['Laryngoscope', 'LMA', 'Glidescope', 'Other'])
    blade = st.selectbox("Blade", ['Mac', 'Miller', 'Wis-Hipple'])
    medications = st.text_input("Meds (e.g., Atropine, Fentanyl, etc.)")
    apneic_oxygenation = st.radio("Apneic Oxygenation", ['Yes', 'No'])
    other_details = st.text_input("Other details?")

    st.subheader("Timing of Intubation")
    intubation_timing = st.text_input("Describe timing of airway management")
    
    submit = st.form_submit_button("Submit")

# Process submission
if submit:
    # Store form data into a dictionary to replace placeholders
    form_data = {
        "date": date,
        "time": time,
        "weight": weight,
        "age": age,
        "difficult_airway": difficult_airway,
        "physical_assessment": physical_assessment,
        "high_risk_desaturation": high_risk_desaturation,
        "increased_icp": increased_icp,
        "unstable_hemodynamics": unstable_hemodynamics,
        "other_risks": other_risks,
        "who_intubate": who_intubate,
        "who_bag_mask": who_bag_mask,
        "ett_size": ett_size,
        "device": device,
        "blade": blade,
        "medications": medications,
        "apneic_oxygenation": apneic_oxygenation,
        "other_details": other_details,
        "intubation_timing": intubation_timing,
    }
    
    # Path to the provided Word template
    template_path = 'AirwayBundleChecklist_7-2020.docx'

    # Fill the Word template with form data
    filled_doc = fill_word_template(template_path, form_data)
    
    # Provide download link for the filled Word document
    st.success("Form submitted successfully!")
    st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")

