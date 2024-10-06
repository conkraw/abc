import streamlit as st
from docx import Document
from io import BytesIO
from docx.shared import Pt
#from docx2pdf import convert  # Optional for PDF conversion

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

    st.subheader("Pre-Intubation TIME OUT")
    date = st.date_input("Date")
    time = st.time_input("Time")
    right_patient = st.checkbox("Right Patient: Confirm 2 identifiers and allergy status")
    right_plan = st.checkbox("Right Plan: Review and revise the plan")
    right_prep = st.checkbox("Right Prep: Patient positioned correctly, IV working, etc.")
    right_equipment = st.checkbox("Right Equipment: SOAP (Suction, Oxygen, etc.) ready")
    right_monitoring = st.checkbox("Right Monitoring: BP cycling, pulse ox in place")
    right_rescue_plan = st.checkbox("Right Rescue Plan: Difficult Airway Cart, etc.")
    right_attitude = st.checkbox("Right Attitude: State out loud if any concerns")

    st.subheader("Post-Procedure TIME OUT")
    feedback_well = st.text_input("What did we do well?")
    feedback_improve = st.text_input("What can we improve upon?")
    difficult_ventilate = st.radio("Was the patient difficult to ventilate?", ['Yes', 'No'])
    difficult_intubate = st.radio("Was the patient difficult to intubate?", ['Yes', 'No'])

    submit = st.form_submit_button("Submit")

# Process submission
if submit:
    # Store form data into a dictionary to replace placeholders
    form_data = {
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
        "date": date,
        "time": time,
        "right_patient": "Yes" if right_patient else "No",
        "right_plan": "Yes" if right_plan else "No",
        "right_prep": "Yes" if right_prep else "No",
        "right_equipment": "Yes" if right_equipment else "No",
        "right_monitoring": "Yes" if right_monitoring else "No",
        "right_rescue_plan": "Yes" if right_rescue_plan else "No",
        "right_attitude": "Yes" if right_attitude else "No",
        "feedback_well": feedback_well,
        "feedback_improve": feedback_improve,
        "difficult_ventilate": difficult_ventilate,
        "difficult_intubate": difficult_intubate,
    }
    
    # Path to the provided Word template
    template_path = '/mnt/data/AirwayBundleChecklist_7-2020.doc'

    # Fill the Word template with form data
    filled_doc = fill_word_template(template_path, form_data)
    
    # Provide download link for the filled Word document
    st.success("Form submitted successfully!")
    st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")
    
    # Optionally convert to PDF and provide PDF download link (requires docx2pdf or similar)
    # pdf = convert(filled_doc)
    # st.download_button("Download PDF Document", data=pdf, file_name="Filled_Airway_Bundle_Checklist.pdf")
