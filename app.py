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

# Function to determine ETT size based on age and unit
def calculate_ett_size(age, age_unit):
    if age_unit == "Days":
        return '3.0' if age <= 30 else '3.5'
    elif age_unit == "Weeks":
        return '3.5' if age <= 6 else '4.0'
    elif age_unit == "Months":
        return '4.0' if age <= 12 else '4.5'
    elif age_unit == "Years":
        return '4.5' if age <= 2 else '5.0' if age <= 10 else '6.0'
    return '4.0'  # Default if no valid input

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
        date = st.date_input("Select Date (MM-DD-YYYY)", value=datetime.today())
        age = st.number_input("Enter Patient Age", min_value=0, value=0)
        weight = st.number_input("Enter Patient Weight (Kilograms)", min_value=0.0, format="%.2f")

    with cols[1]:
        time = st.time_input("Select Time", value=datetime.now().time())
        age_unit = st.selectbox("Select Age Unit", ["Days", "Weeks", "Months", "Years"])

    # Initialize ETT Type based on age
    if 'ett_type' not in st.session_state:
        st.session_state.ett_type = ""

    # Change ETT Type based on age input
    if age > 0 and age_unit in ["Months", "Years"]:
        st.session_state.ett_type = "Cuffed"
    else:
        st.session_state.ett_type = ""

    # Calculate default ETT Size based on age and unit
    default_ett_size = calculate_ett_size(age, age_unit)

    # Intubation plan section
    st.markdown(box_section("Intubation Plan"), unsafe_allow_html=True)

    # Multi-select for "Who will intubate?" and "Who will bag-mask?"
    who_intubate = st.multiselect("Who will intubate?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'Anesthesiologist', 'ENT physician', 'RT', 'Other'])

    who_bag_mask = st.multiselect("Who will bag-mask?", 
                                   ['Resident', 'Fellow', 'NP', 'Attending', 'RT', 'Other'])

    # Create a layout for intubation method
    intubation_method = st.selectbox("How will we intubate? (Method)", ["Oral", "Nasal"])

    # Create a layout for ETT Type and ETT Size
    cols = st.columns(2)  # Create two columns

    with cols[0]:
        ett_type = st.selectbox("ETT Type", ["", "Cuffed", "Uncuffed"], index=["", "Cuffed", "Uncuffed"].index(st.session_state.ett_type))

    with cols[1]:
        # ETT Size Selection
        ett_options = ['3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0', '6.5', '7.0', '7.5', '8.0']
        
        ett_size = st.selectbox("ETT Size", ett_options, index=ett_options.index(default_ett_size))

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
            "age": f"{age} {age_unit}",
            "ett_type": st.session_state.ett_type,  # Get the updated ETT Type
            "who_intubate": ", ".join(who_intubate),  # Convert list to string
            "who_bag_mask": ", ".join(who_bag_mask),  # Convert list to string
            "ett_size": ett_size,
            "intubation_timing": intubation_timing,
        }
        
        # Path to the provided Word template
        template_path = 'AirwayBundleChecklist_7-2020.docx'

        # Fill the Word template with form data
        filled_doc = fill_word_template(template_path, form_data)
        
        # Provide download link for the filled Word document
        st.success("Form submitted successfully!")
        st.download_button("Download Word Document", data=filled_doc, file_name="Filled_Airway_Bundle_Checklist.docx")


