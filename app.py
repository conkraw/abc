import streamlit as st
from docx import Document

# Function to create a Word document from form input
def create_word_document(data):
    doc = Document()
    doc.add_heading('Airway Bundle Checklist', 0)

    doc.add_heading('Assessment for Anticipated Airway Management', level=1)
    doc.add_paragraph(f'Difficult Airway History: {data["difficult_airway"]}')
    doc.add_paragraph(f'Physical (small mouth, short neck, etc.): {data["physical_assessment"]}')
    doc.add_paragraph(f'High risk for rapid desaturation: {data["high_risk_desaturation"]}')
    doc.add_paragraph(f'Increased ICP/pulmonary hypertension: {data["increased_icp"]}')
    doc.add_paragraph(f'Unstable hemodynamics: {data["unstable_hemodynamics"]}')
    doc.add_paragraph(f'Other risk factors: {data["other_risks"]}')

    doc.add_heading('Intubation Plan', level=1)
    doc.add_paragraph(f'Who will intubate: {data["who_intubate"]}')
    doc.add_paragraph(f'Who will bag-mask: {data["who_bag_mask"]}')
    doc.add_paragraph(f'ETT Size: {data["ett_size"]}')
    doc.add_paragraph(f'Device: {data["device"]}')
    doc.add_paragraph(f'Blade: {data["blade"]}')
    doc.add_paragraph(f'Meds: {data["medications"]}')
    doc.add_paragraph(f'Apneic Oxygenation: {data["apneic_oxygenation"]}')
    doc.add_paragraph(f'Other: {data["other_details"]}')

    doc.add_heading('Timing of Intubation', level=1)
    doc.add_paragraph(f'Timing of intubation: {data["intubation_timing"]}')

    doc.add_heading('Pre-Intubation TIME OUT', level=1)
    doc.add_paragraph(f'Date: {data["date"]}')
    doc.add_paragraph(f'Time: {data["time"]}')
    doc.add_paragraph(f'Right Patient: {data["right_patient"]}')
    doc.add_paragraph(f'Right Plan: {data["right_plan"]}')
    doc.add_paragraph(f'Right Prep: {data["right_prep"]}')
    doc.add_paragraph(f'Right Equipment: {data["right_equipment"]}')
    doc.add_paragraph(f'Right Monitoring: {data["right_monitoring"]}')
    doc.add_paragraph(f'Right Rescue Plan: {data["right_rescue_plan"]}')
    doc.add_paragraph(f'Right Attitude: {data["right_attitude"]}')

    doc.add_heading('Post-Procedure TIME OUT', level=1)
    doc.add_paragraph(f'Feedback (What we did well): {data["feedback_well"]}')
    doc.add_paragraph(f'Feedback (Improvements): {data["feedback_improve"]}')
    doc.add_paragraph(f'Was the patient difficult to ventilate? {data["difficult_ventilate"]}')
    doc.add_paragraph(f'Was the patient difficult to intubate? {data["difficult_intubate"]}')

    return doc


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
        "right_patient": right_patient,
        "right_plan": right_plan,
        "right_prep": right_prep,
        "right_equipment": right_equipment,
        "right_monitoring": right_monitoring,
        "right_rescue_plan": right_rescue_plan,
        "right_attitude": right_attitude,
        "feedback_well": feedback_well,
        "feedback_improve": feedback_improve,
        "difficult_ventilate": difficult_ventilate,
        "difficult_intubate": difficult_intubate,
    }
    
    # Create Word document
    doc = create_word_document(form_data)
    doc_name = "Airway_Bundle_Checklist_Filled.docx"
    doc.save(doc_name)
    
    # Provide download link for the Word document
    st.success("Form submitted successfully!")
    st.download_button("Download Word Document", open(doc_name, 'rb'), file_name=doc_name)
