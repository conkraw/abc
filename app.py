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
    }
    
    # Create Word document
    doc = create_word_document(form_data)
    doc_name = "Airway_Bundle_Checklist_Filled.docx"
    doc.save(doc_name)
    
    # Provide download link for the Word document
    st.success("Form submitted successfully!")
    st.download_button("Download Word Document", open(doc_name, 'rb'), file_name=doc_name)
