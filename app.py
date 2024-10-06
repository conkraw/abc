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
            if f'{{{{{key}}}}}' in paragraph.text:  # Looks for {{key}} in the template
                paragraph.text = paragraph.text.replace(f'{{{{{key}}}}}', str(value))

    # Save the updated document in memory
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer

# Streamlit form for the Airway Bundle Checklist
st.title("Airway Bundle Checklist")

# Function to create a boxed section
def box_section(title):
    return f"""
    <div style="border: 1px solid #0072B8; border-radius: 5px; padding: 10px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #0072B8;">{title}</h4>
    </div>
    """

# Create a form
with st.form("airway_form"):
    # Patient Information
    st.markdown(box_section("Patient Information"), unsafe_allow_html=True)
    cols = st.columns(2)  # Create two columns

    with cols[0]:
        date = st.date_input("Select Date", value=datetime.today())
        weight = st.number_input("Enter Patient Weight (in kg)", min_value=0.0, format="%.2f")

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())
        age = st.number_input("Enter Patient Age (in years)", min_value=0, max_value=120)

    # Input for who completed the form
    completed_by = st.text_input("Who completed the form?")

    # Front page completion options
    st.markdown(box_section("Front Page Completion"), unsafe_allow_html=True)
    cols = st.columns(3)  # Create three columns

    with cols[0]:
        on_admission = st.checkbox("On admission")
        during_rounds = st.checkbox("During rounds")

    with cols[1]:
        after_rounds = st.checkbox("After rounds")
        just_prior_intubation = st.checkbox("Just prior to intubation")

    with cols[2]:
        after_intubation = st.checkbox("After intubation")
        prior_to_extubation = st.checkbox("Prior to extubation")

    # Collect completion options in a list
    completion_options = {
        "on_admission": on_admission,
        "during_rounds": during_rounds,
        "after_rounds": after_rounds,
        "just_prior_intubation": just_prior_intubation,
        "after_intubation": after_intubation,
        "prior_to_extubation": prior_to_extubation,
    }

    # Assessment section
    st.markdown(box_section("Assessment for Anticipated Airway Management"), unsafe_allow_html=True)

    # Create a layout for assessment questions
    assessment_questions = [
        "History of difficult airway?",
        "Physical assessment (small mouth, large tongue, etc.)?",
        "High risk for rapid desaturation during intubation?",
        "Increased ICP/pulmonary hypertension?",
        "Unstable hemodynamics?"
    ]

    # Collect responses for assessment questions
    assessment_answers = {}
    for question in assessment_questions:
        cols = st.columns([3, 1])  # Create two columns: 3 parts for question, 1 part for Yes/No dropdown
        with cols[0]:
            st.markdown(f"**{question}**")  # Display question prominently
        with cols[1]:
            answer = st.selectbox("Response", ['Yes', 'No'], key=f"{question}_response")  # Yes/No dropdown
            assessment_answers[question] = answer

    # Intubation plan section
    st.markdown(box_section("Intubation Plan"), unsafe_allow_html=True)

    # Checkboxes for "Who will intubate" and "Who will bag-mask"
    st.subheader("Who will intubate?")    
    intubators = ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other']
    intubator_selection = []
    for intubator in intubators:
        selected = st.checkbox(intubator)
        if selected:
            intubator_selection.append(intubator)

    st.subheader("Who will bag-mask?")
    bag_maskers = ['Resident', 'Fellow', 'NP', 'Attending', 'RT', 'Other']
    bag_masker_selection = []
    for bag_masker in bag_maskers:
        selected = st.checkbox(bag_masker)
        if selected:
            bag_masker_selection.append(bag_masker)

    ett_size = st.selectbox("ETT Size", ['3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'])
    device = st.selectbox("Device", ['Laryngoscope', 'LMA', 'Glidescope', 'Other'])
    blade = st.selectbox("Blade", ['Mac', 'Miller', 'Wis-Hipple'])
    medications = st.text_input("Meds (e.g., Atropine, Fentanyl, etc.)")
    apneic_oxygenation = st.radio("Apneic Oxygenation", ['Yes', 'No'])
    other_details = st.text_input("Other details?")

    # Timing of Intubation section
    st.markdown(box_section("Timing of Intubation"), unsafe_allow_html=True)
    intubation_timing = st.text_input("Describe timing of airway management")

    # Submit button
    submit = st.form_submit_button("Submit")

    # Process submission
    if submit:
        # Store form data into a dictionary to replace placeholders
        form_data = {
            "date": date,
            "time": time,
            "weight": weight,
            "age": age,
            "completed_by": completed_by,
            "completion_options": ", ".join([key.replace('_', ' ').capitalize() for key, value in completion_options.items() if value]),  # Format checked options
            **assessment_answers,  # Include all assessment answers
            "who_intubate": ", ".join(intubator_selection),  # Convert list to string
            "who_bag_mask": ", ".join(bag_masker_selection),  # Convert list to string
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


