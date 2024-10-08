import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime

# Mapping of age to ETT size
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

st.title("Airway Bundle Checklist")

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
        
        # Select patient age
        age = st.selectbox("Select Patient Age", list(age_to_ett_mapping.keys()), key="age_select")
        
        # Update ETT size based on selected age
        ett_size = age_to_ett_mapping.get(age, '4.0')
        st.session_state['ett_size'] = ett_size  # Update ETT size in session state

        # Show the ETT size based on age
        st.selectbox(
            "ETT Size (Auto-Selected Based on Age)",
            options=['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'],
            index=['', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0'].index(ett_size),
            key="ett_size",
            disabled=True  # Disable the ETT size selectbox
        )

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())
        weight_str = st.text_input("Enter Patient Weight (Kilograms)", value="")
        if weight_str and not weight_str.replace('.', '', 1).isdigit():
            st.error("Please enter a valid number for the weight (e.g., 12.5 or 12).")
    
    st.markdown(box_section("Intubation Risk Assessment"), unsafe_allow_html=True)

    # Submit button
    submit = st.form_submit_button("Submit")

    # Process submission
    if submit:
        # Store form data into a dictionary to replace placeholders
        form_data = {
            "front_page_completed": front_page_completed,
            "completed_by": completed_by,
            "room_number": room_number,
            "date": date.strftime("%Y-%m-%d"),
            "time": time.strftime("%H:%M"),
            "weight": weight_str,
            "age": age,
            "ett_size": ett_size
        }

        # Path to the provided Word template
        template_path = 'AirwayBundleChecklist_7-2020.docx'

        # Fill the Word template with form data
        filled_doc = fill_word_template(template_path, form_data)

        # Provide download link for the filled Word document
        st.success("Form submitted successfully!")
        st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")


